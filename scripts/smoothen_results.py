import os
import sys
sys.path.append("../")
sys.path.append("./")

import joblib
import argparse
from lib.utils.smooth_pose import smooth_pose


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_path", required=True, help="Path to file where data is dumped")
    parser.add_argument("--out_path", required=True, help="Directory where output will be stored")
    args = parser.parse_args()
    data = joblib.load(args.in_path)
    data_ref = data # Creates a deepcopy
    for pid in data.keys():
        person_params = data[pid]
        poses = person_params['pose']
        betas = person_params['betas']
        verts_ref, poses_ref, joints3d_ref = smooth_pose(poses, betas, min_cutoff=0.004, beta=0.7)
        data_ref[pid]['verts'] = verts_ref
        data_ref[pid]['pose'] = poses_ref
        data_ref[pid]['joints3d'] = joints3d_ref
    # dir_name = os.path.dirname(args.file_path)
    # orig_file_name = ".".join(os.path.basename(args.file_path).split(".")[:-1])
    # ext = os.path.basename(args.file_path).split(".")[-1]
    # new_file_path = os.path.join(args.out_dir, f"output_refined.pkl")
    new_file_path = args.out_path
    if not os.path.isdir(os.path.dirname(new_file_path)):
        os.makedirs(os.path.dirname(new_file_path))
    joblib.dump(data_ref, new_file_path)
