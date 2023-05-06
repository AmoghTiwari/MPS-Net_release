#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate mps_env

# Check the README for more details of each command/flag

cd .. # Go to parent directory

# Run simple inference of MPS-Net
python demo.py --file_type video --vid_file data/demo_data/sample_video.mp4 --out_dir outputs/sample_video_mp4/initial --gpu 0 --save_pkl --save_obj --save_processed_input
# It is recommended to save the processed inputs. It comes handy later if using one-euro filter
# The results will be found in <out_dir>

# Run One-Euro Filter
python scripts/smoothen_results.py --in_path outputs/sample_video_mp4/initial/output.pkl --out_path outputs/sample_video_mp4/refined1/output_refined1.pkl --min_cutoff 0.004 --beta 0.7

# Render results based on the refined pkl file
python demo.py --file_type frames --frames_dir outputs/sample_video_mp4/initial/extracted_frames --render_from_pkl --pkl_file outputs/sample_video_mp4/refined1/output_refined1.pkl --out_dir outputs/sample_video_mp4/refined1 --gpu 0 
# Note: To just render the SMPL, not overlay it, use the "--render_plain" argument
