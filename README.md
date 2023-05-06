# MPS-Net (Forked)

# To Do
- Experiment for videos as input

# Installation
After following the steps mentioned in the original README (see "README_original.md"), uninstall pyglet: ```pip uninstall pyglet```. And then reinstall an older version of pyglet (1.5): ```pip install pyglet=1.5```. This is because the latest version of pyglet is not compatible with python3.6 which has been used in this code base

# Demo
- Activate conda environmnet:
```
    source /data/groot/miniconda3/condabin/conda # Source your conda environment
    conda activate mps_env # Activate your conda environment
```
- To run on a video, see ```run_demo_video.sh``` (Only the first command of the script is needed)
- To run on a set of frames, see ```run_demo_frames.sh``` (Only the first command of the script is needed)
- **Important !!!** Please copy paste the commands one by one from the bash script and run them individually. Also ensure that you read the corresponding comments in the bash script. This is because you might not require all the steps done in the bash script
- To render results on a plain background (i.e. without overlaying the results on the input video), include the ```--render_plain``` flag when running the ```demo.py``` file.

# Run One-Euro Filter
- Check the second command in ```run_demo_video.sh``` or ```run_demo_frames.sh```
- You should experiment with different hyper-parameters to get good results

# Get results based on the smoothened outputs
- Check the third command in ```run_demo_video.sh``` or ```run_demo_frames.sh```
- We will be using the ```render_from_pkl``` flag here, where we specify path to a ```pkl_file``` and then the code renders outputs directly from the pkl file, instead of doing inference. In this case, we will use the smoothened pkl file which we had obtained after running one-euro filter

# Notes
- If you want to run one-euro filter, either use frames as input always, or alternatively, generate results with the ```--save_processed_input``` flag, and then use the generated set of frames to run one-euro filter, and then later render from the refined pkl file

- Command used internally to split a video into frames: <br/>
``` ffmpeg -i <path_to_video> -r 30000/1001 -f image2 -v error <path_to_target_dir>/%06d.jpg``` <br/>
For example: ``` ffmpeg -i sample_video.mp4 -r 30000/1001 -f image2 -v error sample_video_mp4/%06d.jpg``` <br/>
**Note**: Ensure that the "target_dir" already exists before running the above command

- Example command used internally to join frames to get video: ```ffmpeg -framerate 30000/1001 -y -threads 16 -i outputs/sample_video_mp4/output_frames/%06d.jpg -profile:v baseline -level 3.0 -c:v libx264 -pix_fmt yuv420p -an -v error outputs/sample_video_mp4/output.mp4```

## Details on CLI options provided with the demo file
**Additional Flags**:
- ```--save_pkl``` (optional)to save the pkl files which has all the predicted pose and shape data
- ```--save_obj``` (optional) to save the meshes
- ```--render_from_pkl```: To render directly from a saved pkl file containing shape and pose parameters. Be careful not to overwrite any past results you might have when using this flag
- ```--render_plain```: To render on a plain background
- ```--save_processed_input```: Specify it if you want to save the extracted frames from the input video.
