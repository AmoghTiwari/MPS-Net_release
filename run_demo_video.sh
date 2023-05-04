#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate mps_env

# Check the README for more details of each command/flag

# Run simple inference of MPS-Net
python demo.py --file_type video --frames_dir data/demo_data/sample_video.mp4 --gpu 0 --out_dir outputs/sample_video_mp4 --save_pkl --save_obj --save_processed_input
# It is recommended to save the processed inputs. It comes handy later if using one-euro filter
# The results will be found in <out_dir>

# Run One-Euro Filter
python scripts/smoothen_results.py --in_path outputs/sample_video_mp4/output.pkl --out_path outputs/sample_video_mp4/output_refined.pkl

# Render results based on the refined pkl file
python demo.py --file_type frames --frames_dir outputs/sample_video_mp4/input_frames --gpu 0 --out_dir outputs/sample_video_mp4 --render_from_pkl --pkl_file outputs/sample_video_mp4/output_refined.pkl

# These results will be found in <out_dir>/from_pkl

# Note: To just render the SMPL, not overlay it, use the "--render_plain" argument

