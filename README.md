# MPS-Net (Forked)

# Installation
After following the steps mentioned in the original README (see "README_original.md"), uninstall pyglet: ```pip uninstall pyglet```. And then reinstall an older version of pyglet (1.5): ```pip install pyglet=1.5```. This is because the latest version of pyglet is not compatible with python3.6 which has been used in this code base

# Demo
Command to Run: 
To run on a video: ```python demo.py --file_type video --vid_file /data/demo_data/sample_video.mp4 --gpu 0 --out_dir /data/mps_net_output_demo/
To run on a set of frames: ```python demo.py --file_type frames --frames_dir /data/demo_data/sample_video_mp4_frames --gpu 0 --out_dir /data/mps_net_output_demo/

If you want to save the pkl and obj files, add the ```--save_pkl``` and the ```--save_obj``` flags respectively

