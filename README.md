# MPS-Net (Forked)

# Installation
After following the steps mentioned in the original README (see "README_original.md"), uninstall pyglet: ```pip uninstall pyglet```. And then reinstall an older version of pyglet (1.5): ```pip install pyglet=1.5```. This is because the latest version of pyglet is not compatible with python3.6 which has been used in this code base

# Demo
**Commands to Run**: <br/>
- Activate conda environment: ```conda activate mps_env```
- To run on a video: ```python demo.py --file_type video --vid_file data/demo_data/sample_video.mp4 --gpu 0 --out_dir outputs/``` <br/>
- To run on a set of frames: ```python demo.py --file_type frames --frames_dir data/demo_data/sample_video_mp4 --gpu 0 --out_dir outputs```

**Additional Flags**:
- ```--save_pkl``` to save the pkl files which has all the predicted pose and shape data
- ```--save_obj``` to save the meshes
- ```--render_from_pkl```: To render directly from a saved pkl file containing shape and pose parameters
- ```--render_plain```: To render on a plain background
- ```--save_processed_input```: Specify it if you want to save the extracted frames from the input video.

# Running One-Euro Filter
From the root dir itself, run: ```python scripts/smoothen_results.py --file_path outputs/sample_video_mp4/mpsnet_output.pkl```
This will save a file with the suffix "_refined" to where your earlier pkl file had existed
To get results using the new refined pkl file, check out the ```--render_from_pkl``` flag

# Notes
- If you want to run one-euro filter, either use frames as input always, or alternatively, generate results with the ```--save_processed_input``` flag, and then use the generated set of frames to run one-euro filter, and then later render from the refined pkl file
Command which the code uses internally to split a video into frames: <br/>
``` ffmpeg -i <path_to_video> -r 30000/1001 -f image2 -v error <path_to_target_dir>/%06d.jpg``` <br/>
For example: ``` ffmpeg -i sample_video.mp4 -r 30000/1001 -f image2 -v error sample_video_mp4/%06d.jpg``` <br/>
**Note**: Ensure that the "target_dir" already exists before running the above command
