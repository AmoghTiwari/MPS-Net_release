import os
import sys
sys.path.append("../")
sys.path.append("./")

import joblib
import argparse
from lib.utils.smooth_pose import smooth_pose


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", required=True, help="Path to file where data is dumped")
    args = parser.parse_args()
    data = joblib.load(args.file_path)
    data_ref = data # Creates a deepcopy
    for pid in data.keys():
        person_params = data[pid]
        poses = person_params['pose']
        betas = person_params['betas']
        verts_ref, poses_ref, joints3d_ref = smooth_pose(poses, betas)
        data_ref[pid]['verts'] = verts_ref
        data_ref[pid]['pose'] = poses_ref
        data_ref[pid]['joints3d'] = joints3d_ref
    dir_name = os.path.dirname(args.file_path)
    orig_file_name = ".".join(os.path.basename(args.file_path).split(".")[:-1])
    ext = os.path.basename(args.file_path).split(".")[-1]
    new_file_path = os.path.join(dir_name, f"{orig_file_name}_refined.{ext}")
    joblib.dump(data_ref, new_file_path)
