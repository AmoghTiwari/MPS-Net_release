# -*- coding: utf-8 -*-

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: ps-license@tuebingen.mpg.de

import os
import os.path as osp
from lib.core.config import BASE_DATA_DIR
from lib.models.smpl import SMPL, SMPL_MODEL_DIR
os.environ['PYOPENGL_PLATFORM'] = 'egl'

import cv2
import time
import torch
import joblib
import shutil
import colorsys
import argparse
import random
import numpy as np
from pathlib import Path
from tqdm import tqdm
from multi_person_tracker import MPT
from torch.utils.data import DataLoader

from lib.models.mpsnet import MPSnet
from lib.utils.renderer import Renderer
from lib.dataset._dataset_demo import CropDataset, FeatureDataset
from lib.utils.demo_utils import (
    download_youtube_clip,
    convert_crop_cam_to_orig_img,
    prepare_rendering_results,
    video_to_images,
    images_to_video,
    frames_from_dir,
)

MIN_NUM_FRAMES = 25
random.seed(1)
torch.manual_seed(1)
np.random.seed(1)


def main(args):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    out_dir = args.out_dir

    """ Prepare input video (images) """
    if args.file_type == "video":
        video_file = args.vid_file
        if video_file.startswith('https://www.youtube.com'):
            print(f"Donwloading YouTube video \'{video_file}\'")
            video_file = download_youtube_clip(video_file, './tmp_dir')
            if video_file is None:
                exit('Youtube url is not valid!')
            print(f"YouTube Video has been downloaded to {video_file}...")

        if not os.path.isfile(video_file):
            exit(f"Input video \'{video_file}\' does not exist!")

        # output_path = osp.join(out_dir, os.path.basename(video_file).replace('.', '_'))
        output_path = out_dir
        try:
            Path(output_path).mkdir(parents=True, exist_ok=False)
        except:
            pass
        if args.save_processed_input: # Save to a target dir
            image_folder, num_frames, img_shape = video_to_images(video_file, img_folder=output_path,return_info=True)
        else: # Save to ./tmp_dir""
            image_folder, num_frames, img_shape = video_to_images(video_file, img_folder=None,return_info=True)
        
    elif args.file_type == "frames":
        frames_dir = args.frames_dir
        output_path = out_dir
        try:
            Path(output_path).mkdir(parents=True, exist_ok=False)
        except:
            pass
        image_folder, num_frames, img_shape = frames_from_dir(frames_dir, return_info=True)

    print(f"Input number of frames {num_frames}\n")
    orig_height, orig_width = img_shape[:2]


    if not args.render_from_pkl:
        """ Run tracking """
        total_time = time.time()
        bbox_scale = 1.1    #
        # run multi object tracker
        mot = MPT(
            device=device,
            batch_size=args.tracker_batch_size,
            display=args.display,
            detector_type=args.detector,
            output_format='dict',
            yolo_img_size=args.yolo_img_size,
        )
        tracking_results = mot(image_folder)

        # remove tracklets if num_frames is less than MIN_NUM_FRAMES
        for person_id in list(tracking_results.keys()):
            if tracking_results[person_id]['frames'].shape[0] < MIN_NUM_FRAMES:
                del tracking_results[person_id]


        """ Get MPSnet model """
        seq_len = 16
        model = MPSnet(
            seqlen=seq_len,
            n_layers=2,
            hidden_size=1024
        ).to(device)

        # Load pretrained weights
        pretrained_file = args.model
        ckpt = torch.load(pretrained_file)
        print(f"Load pretrained weights from \'{pretrained_file}\'")
        ckpt = ckpt['gen_state_dict']
        model.load_state_dict(ckpt, strict=False)

        # Change mesh gender
        gender = args.gender  # 'neutral', 'male', 'female'
        model.regressor.smpl = SMPL(
            SMPL_MODEL_DIR,
            batch_size=64,
            create_transl=False,
            gender=gender
        ).cuda()

        model.eval()

        # Get feature_extractor
        from lib.models.spin import hmr
        hmr = hmr().to(device)
        checkpoint = torch.load(osp.join(BASE_DATA_DIR, 'spin_model_checkpoint.pth.tar'))
        hmr.load_state_dict(checkpoint['model'], strict=False)
        hmr.eval()

        """ Run MPSnet on each person """
        print("\nRunning MPSnet on each person tracklet...")
        running_time = time.time()
        running_results = {}
        for person_id in tqdm(list(tracking_results.keys())):
            bboxes = joints2d = None
            bboxes = tracking_results[person_id]['bbox']
            frames = tracking_results[person_id]['frames']

            # Prepare static image features
            dataset = CropDataset(
                image_folder=image_folder,
                frames=frames,
                bboxes=bboxes,
                joints2d=joints2d,
                scale=bbox_scale,
            )

            bboxes = dataset.bboxes
            frames = dataset.frames
            has_keypoints = True if joints2d is not None else False

            crop_dataloader = DataLoader(dataset, batch_size=256, num_workers=0)     #16

            with torch.no_grad():
                feature_list = []
                for i, batch in enumerate(crop_dataloader):
                    if has_keypoints:
                        batch, nj2d = batch
                        norm_joints2d.append(nj2d.numpy().reshape(-1, 21, 3))

                    batch = batch.to(device)
                    feature = hmr.feature_extractor(batch.reshape(-1,3,224,224))
                    feature_list.append(feature.cpu())

                del batch

                feature_list = torch.cat(feature_list, dim=0)

            # Encode temporal features and estimate 3D human mesh
            dataset = FeatureDataset(
                image_folder=image_folder,
                frames=frames,
                seq_len=seq_len,
            )
            dataset.feature_list = feature_list

            dataloader = DataLoader(dataset, batch_size=64, num_workers=0)     #32
            with torch.no_grad():
                pred_cam, pred_verts, pred_pose, pred_betas, pred_joints3d, norm_joints2d = [], [], [], [], [], []
                pred_joints2d = []
                for i, batch in enumerate(dataloader):
                    if has_keypoints:
                        batch, nj2d = batch
                        norm_joints2d.append(nj2d.numpy().reshape(-1, 21, 3))

                    batch = batch.to(device)
                    output = model(batch)[0][-1]

                    pred_cam.append(output['theta'][:, :3])
                    pred_verts.append(output['verts'])
                    pred_pose.append(output['theta'][:, 3:75])
                    pred_betas.append(output['theta'][:, 75:])
                    pred_joints3d.append(output['kp_3d'])
                    pred_joints2d.append(output['kp_2d'])

                pred_cam = torch.cat(pred_cam, dim=0)
                pred_verts = torch.cat(pred_verts, dim=0)
                pred_pose = torch.cat(pred_pose, dim=0)
                pred_betas = torch.cat(pred_betas, dim=0)
                pred_joints3d = torch.cat(pred_joints3d, dim=0)
                pred_joints2d = torch.cat(pred_joints2d, dim=0)

                del batch

            # ========= Save results to a pickle file ========= #
            pred_cam = pred_cam.cpu().numpy()
            pred_verts = pred_verts.cpu().numpy()
            pred_pose = pred_pose.cpu().numpy()
            pred_betas = pred_betas.cpu().numpy()
            pred_joints3d = pred_joints3d.cpu().numpy()
            pred_joints2d = pred_joints2d.cpu().numpy()

            bboxes[:, 2:] = bboxes[:, 2:] * 1.2
            if args.render_plain:
                pred_cam[:,0], pred_cam[:,1:] = 1, 0  # np.array([[1, 0, 0]])
            orig_cam = convert_crop_cam_to_orig_img(
                cam=pred_cam,
                bbox=bboxes,
                img_width=orig_width,
                img_height=orig_height
            )

            output_dict = {
                'pred_cam': pred_cam,
                'orig_cam': orig_cam,
                'verts': pred_verts,
                'pose': pred_pose,
                'betas': pred_betas,
                'joints3d': pred_joints3d,
                'joints2d': pred_joints2d,
                'bboxes': bboxes,
                'frame_ids': frames,
            }

            running_results[person_id] = output_dict

        del model

        end = time.time()
        fps = num_frames / (end - running_time)
        print(f'MPSnet FPS: {fps:.2f}')
        total_time = time.time() - total_time
        print(f'Total time spent: {total_time:.2f} seconds (including model loading time).')
        print(f'Total FPS (including model loading time): {num_frames / total_time:.2f}.')

        if args.save_pkl:
            # print(f"Saving output results to \'{os.path.join(output_path, 'mpsnet_output.pkl')}\'.")
            print(f"Saving output results to \'{os.path.join(output_path, 'output.pkl')}\'.")
            # joblib.dump(running_results, os.path.join(output_path, "mpsnet_output.pkl"))
            joblib.dump(running_results, os.path.join(output_path, "output.pkl"))

    else:
        running_results = joblib.load(args.pkl_file)

    if args.render_plain:
        output_dir_name = f'output_frames_plain'
    else:
        output_dir_name = f'output_frames'
    output_img_folder = os.path.join(output_path, output_dir_name)

    """ Render results as a single video """
    renderer = Renderer(resolution=(orig_width, orig_height), orig_img=True, wireframe=args.wireframe)
    try:
        os.makedirs(output_img_folder, exist_ok=False)
    except:
        pass

    print(f"\nRendering output video, writing frames to {output_img_folder}")
    # prepare results for rendering
    frame_results = prepare_rendering_results(running_results, num_frames)
    # mesh_color = {k: colorsys.hsv_to_rgb(np.random.rand(), 0.5, 1.0) for k in running_results.keys()}
    mesh_color = {k:(0.6274509803921569, 0.6274509803921569, 0.6274509803921569) for k in running_results.keys()} # Gray colour
    image_file_names = sorted([
        os.path.join(image_folder, x)   
        for x in os.listdir(image_folder)
        if x.endswith('.png') or x.endswith('.jpg')
    ])

    for frame_idx in tqdm(range(len(image_file_names))):
        img_fname = image_file_names[frame_idx]
        img = cv2.imread(img_fname)
        input_img = img.copy()
        if args.render_plain:
            img[:] = 0

        if args.sideview:
            side_img = np.zeros_like(img)

        for person_id, person_data in frame_results[frame_idx].items():
            frame_verts = person_data['verts']
            frame_cam = person_data['cam']

            mesh_filename = None
            if args.save_obj:
                mesh_folder = os.path.join(output_path, 'meshes', f'{person_id:04d}')
                try:
                    Path(mesh_folder).mkdir(parents=True, exist_ok=False)
                except:
                    pass
                mesh_filename = os.path.join(mesh_folder, f'{frame_idx:06d}.obj')

            mc = mesh_color[person_id]

            img = renderer.render(
                img,
                frame_verts,
                cam=frame_cam,
                color=mc,
                mesh_filename=mesh_filename,
            )
            if args.sideview:
                side_img = renderer.render(
                    side_img,
                    frame_verts,
                    cam=frame_cam,
                    color=mc,
                    angle=270,
                    axis=[0,1,0],
                )

        if args.sideview:
            img = np.concatenate([img, side_img], axis=1)

        # save output frames
        cv2.imwrite(os.path.join(output_img_folder, f'{frame_idx:06d}.jpg'), img)

        if args.display:
            cv2.imshow('Video', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    if args.display:
        cv2.destroyAllWindows()

    """ Save rendered video """
    if args.render_plain:
        output_save_name = f'output_plain.mp4'
    else:
        output_save_name = f'output.mp4'
    output_save_path = os.path.join(output_path, output_save_name)

    images_to_video(img_folder=output_img_folder, output_vid_file=output_save_path)
    if args.save_processed_input:
        # input_save_name = f'MPS-Net_{frames_dir_name}_input.mp4'
        input_save_name = f'input_proc.mp4'
        input_save_path = os.path.join(output_path, input_save_name)
        if args.file_type == "video":
            images_to_video(img_folder=image_folder, output_vid_file=input_save_path)
        elif args.file_type == "frames":
            print(f"!!! WARNING !!! The video made from the input frames won't be saved. Please check the README for steps if you want to save it")
            # Reason for not saving this is that the "images_to_video" function expects the frames to
            # abide by a certain naming format. And if our input doesn't follow that format, we run into issues
    
    print(f"Saving result video to {os.path.abspath(output_save_path)}")
    shutil.rmtree(output_img_folder)
    # shutil.rmtree(input_img_folder)
    shutil.rmtree(image_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    ##### CHANGES BELOW THIS BLOCK #####
    parser.add_argument('--file_type', required=True, choices=['video', 'frames'], help='What kind of input are you giving [videos/frames]?')
    parser.add_argument('--vid_file', type=str, help='input video path or youtube link')
    parser.add_argument('--frames_dir', type=str, help='path to directory with frames')
    parser.add_argument('--out_dir', required=True, help="Path to directory to store results")
    parser.add_argument('--save_processed_input', action='store_true', help='Should extracted frames and/or the combined video of the given frames i.e. without SMPL overlay be saved?')
    parser.add_argument('--render_from_pkl', action='store_true', help="Directly render from an existing pkl file. No need to perform prediction")
    parser.add_argument('--pkl_file', type=str, help='Path to pkl file which has the required info for rendering')
    ##### CHANGES ABOVE THIS BLOCK #####

    parser.add_argument('--save_pkl', action='store_true', help='save results to a pkl file')

    parser.add_argument('--save_obj', action='store_true', help='save results as .obj files.')

    parser.add_argument('--model', type=str, default='./data/base_data/mpsnet_model_best.pth.tar', help='path to pretrained model weight')

    parser.add_argument('--detector', type=str, default='yolo', choices=['yolo', 'maskrcnn'],
                        help='object detector to be used for bbox tracking')

    parser.add_argument('--yolo_img_size', type=int, default=416,
                        help='input image size for yolo detector')

    parser.add_argument('--tracker_batch_size', type=int, default=12,
                        help='batch size of object detector used for bbox tracking')

    parser.add_argument('--display', action='store_true',
                        help='visualize the results of each step during demo')

    parser.add_argument('--gender', type=str, default='neutral',
                        help='set gender of people from (neutral, male, female)')

    parser.add_argument('--wireframe', action='store_true',
                        help='render all meshes as wireframes.')

    parser.add_argument('--sideview', action='store_true',
                        help='render meshes from alternate viewpoint.')

    parser.add_argument('--render_plain', action='store_true',
                        help='render meshes on plain background')

    parser.add_argument('--gpu', type=int, default='1', help='gpu num')

    args = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

    # main(args)
    
    ##### CHANGES BELOW THIS BLOCK
    if args.file_type == "video":
        assert args.vid_file != None, "'--vid_file' flag must be specified when '--file_type' is specified to be video'"
    elif args.file_type == "frames":
        assert args.frames_dir != None, "'--frames_dir' flag must be specified when '--file_type' is specified to be 'frames'"
    if args.render_from_pkl:
        assert args.pkl_file != None, "'pkl_file' flag must be specified when '--render_from_pkl' is specified"
    main(args)
    ##### CHANGES ABOVE THIS BLOCK #####
