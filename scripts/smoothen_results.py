import os
import sys
sys.path.append("../")
sys.path.append("./")

import joblib
import argparse
from lib.utils.smooth_pose import smooth_pose

def main(args):
    data = joblib.load(args.in_path)
    data_ref = data # Creates a deepcopy
    min_cutoff = args.min_cutoff
    beta = args.beta
    
    for pid in data.keys():
        person_params = data[pid]
        poses = person_params['pose']
        betas = person_params['betas']
        verts_ref, poses_ref, joints3d_ref = smooth_pose(poses, betas, min_cutoff=min_cutoff, beta=beta)
        data_ref[pid]['verts'] = verts_ref
        data_ref[pid]['pose'] = poses_ref
        data_ref[pid]['joints3d'] = joints3d_ref

    new_file_path = args.out_path
    if not os.path.isdir(os.path.dirname(new_file_path)):
        os.makedirs(os.path.dirname(new_file_path))
    joblib.dump(data_ref, new_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_path", required=True, help="Path to file where data is dumped")
    parser.add_argument("--out_path", required=True, help="Directory where output will be stored")
    parser.add_argument("--min_cutoff", default=0.004, help="Min cutoff param of one-euro filter")
    parser.add_argument("--beta", default=0.7, help="Beta parameter of one-euro filter")
    args = parser.parse_args()
    main(args)
