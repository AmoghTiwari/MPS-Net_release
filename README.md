# MPS-Net (Forked)

# To Do
- Experiment for videos as input
- Remove redundant if-else statements in demo.py

# Summary
Commands to Run MPS-Net: 
- With Overlay: ```/data/common/MPS-Net_release/run_on_dance_data.sh```
- Without Overlay: ```/data/common/MPS-Net_release/run_on_dance_data_no_overlay.sh```
- Path to README: ```/data/common/MPS-Net_release/README.md```

Relevant Steps (same as mentioned in the bash script / README):
1. Run vanilla MPS-Net
2. Run euro-filter script:
    a. See command to run in bash script / README
    b. Modify the EURO-Filter parameters in script/smoothen_pose.py, where smooth_pose() function is called
3. After smoothening, we want to directly render things from the refined PKL file, and not do inference. For that, we specify the --render_from_pkl flag and provide the path to the pkl file in ```--pkl_file```. The results for this are saved in ```args.out_dir/from_pkl```

General Note: Default setting is that results are rendered as overlayed on the original video. But if we don't want overlay, use the ```--render_plain``` flag.

# Details
## Installation
After following the steps mentioned in the original README (see "README_original.md"), uninstall pyglet: ```pip uninstall pyglet```. And then reinstall an older version of pyglet (1.5): ```pip install pyglet=1.5```. This is because the latest version of pyglet is not compatible with python3.6 which has been used in this code base

## Demo
**Example commands**: See ```run_demo_video.sh``` and ```run_demo_frames.sh``` to see the steps to perform inference on a video and a set of frames respectively. More details below

**Commands to Run**: <br/>
- Activate conda environment: ```conda activate mps_env```
- To run on a video: ```python demo.py --file_type video --vid_file data/demo_data/sample_video.mp4 --gpu 0 --out_dir outputs/<unique_identifier_for_this_file>``` <br/>
- To run on a set of frames, specify```file_type``` as "frames" and specify path to the frames directory in ```frames_dir```
- An example command: ```python demo.py --file_type frames --frames_dir data/demo_data/sample_video_mp4 --gpu 0 --out_dir outputs/sample_video_mp4 --save_pkl --save_obj```

**Additional Flags**:
- ```--save_pkl``` (optional)to save the pkl files which has all the predicted pose and shape data
- ```--save_obj``` (optional) to save the meshes
- ```--render_from_pkl```: To render directly from a saved pkl file containing shape and pose parameters. Stores results in a directory called ```from_pkl``` within the args.out_dir
- ```--render_plain```: To render on a plain background
- ```--save_processed_input```: Specify it if you want to save the extracted frames from the input video.

##  Smoothen the Results (Using One-Euro Filter)
From the root dir itself, run: ```python scripts/smoothen_results.py --in_path outputs/sample_video_mp4/output.pkl --out_path outputs/sample_video_mp4/output_refined.pkl```. To get results using the new refined pkl file, check out the ```--render_from_pkl``` flag. For example, you can run this command: ```python demo.py --file_type frames --frames_dir data/demo_data/sample_video_mp4 --gpu 0 --out_dir outputs/sample_video_mp4 --render_from_pkl --pkl_file outputs/sample_video_mp4/output_refined.pkl```

To modify the parameters of the One-Euro Filter, modify the ```smooth_pose()``` function call in ```scripts/smoothen_results.py```

## Notes
- If you want to run one-euro filter, either use frames as input always, or alternatively, generate results with the ```--save_processed_input``` flag, and then use the generated set of frames to run one-euro filter, and then later render from the refined pkl file

- Command used internally to split a video into frames: <br/>
``` ffmpeg -i <path_to_video> -r 30000/1001 -f image2 -v error <path_to_target_dir>/%06d.jpg``` <br/>
For example: ``` ffmpeg -i sample_video.mp4 -r 30000/1001 -f image2 -v error sample_video_mp4/%06d.jpg``` <br/>
**Note**: Ensure that the "target_dir" already exists before running the above command

- Example command used internally to join frames to get video: ```ffmpeg -framerate 30000/1001 -y -threads 16 -i outputs/sample_video_mp4/output_frames/%06d.jpg -profile:v baseline -level 3.0 -c:v libx264 -pix_fmt yuv420p -an -v error outputs/sample_video_mp4/output.mp4```
