#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate mps_env

# Check the README for more details of each command/flag

# Run simple inference of MPS-Net

python demo.py --file_type frames --frames_dir /data/volumetric/past_data/data2/color/1 --gpu 0 --out_dir /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1 --save_pkl --save_obj --render_plain

# It is recommended to save the processed inputs. It comes handy later if using one-euro filter
# The results will be found in <out_dir>

# Run One-Euro Filter

python scripts/smoothen_results.py --in_path /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/output.pkl --out_path /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/output_refined.pkl


# Render results based on the refined pkl file
python demo.py --file_type frames --frames_dir /data/volumetric/past_data/data2/color/1 --gpu 0 --out_dir /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1 --save_pkl --save_obj --render_from_pkl --pkl_file /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/output_refined.pkl --render_plain

# These results will be found in <out_dir>/from_pkl

# Note: To just render the SMPL, not overlay it, use the "--render_plain" argument

