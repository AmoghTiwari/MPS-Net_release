#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate mps_env

### Check the README for more details of each command/flag

cd .. # Go to parent directory

# Run simple inference of MPS-Net
python demo.py --file_type frames --frames_dir /data/volumetric/past_data/data2/color/1 --out_dir /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/initial --gpu 0 --save_pkl --save_obj
# The results will be found in <out_dir>
# It is recommended to save the processed inputs. It comes handy later if using one-euro filter

# Run One-Euro Filter
python scripts/smoothen_results.py --in_path /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/initial/output.pkl --out_path /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/refined1/output_refined1.pkl --min_cutoff 0.004 --beta 0.7

# Render results based on the refined pkl file
python demo.py --file_type frames --frames_dir /data/volumetric/past_data/data2/color/1 --render_from_pkl --pkl_file /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/refined1/output_refined1.pkl --out_dir /data/results/smpl_fitting/dance_data/mpsnet_results/data2/color/1/refined1 --gpu 0 --save_pkl --save_obj 

# Note: To just render the SMPL, not overlay it, use the "--render_plain" argument
