import argparse
import joblib
import numpy as np
import matplotlib.pyplot as plt

def plot_hist(arr, path):
    print(f"Min: {np.min(arr)}, Max: {np.max(arr)}")
    _ = plt.hist(arr, bins='auto')
    plt.savefig(path)
    plt.close()

def plot_all_errors(arr, path):
    full_arr = np.concatenate(arr)
    full_mean = np.mean(full_arr)
    print(f"Min: {np.min(full_arr)}, Max: {np.max(full_arr)}")
    seq_means = []
    seq_idx = np.arange(len(arr))
    for i in range(len(arr)):
        seq_means.append(np.mean(arr[i]))
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(seq_idx, seq_means)
    plt.savefig(path)
    plt.close() 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-d','--target_dataset', help='Description for foo argument', required=True)
    args = parser.parse_args()
    target_dataset =  args.target_dataset
    # target_dataset = "3dpw"
    print("Dataset: ", target_dataset)
    SAVE_SEQ_LENS = False
    pkl_path = f"./outputs/error_arrays/mpsnet_result_{target_dataset}.pkl"
    d = joblib.load(pkl_path)

    mpjpe_data = d['mpjpe']
    pampjpe_data = d['mpjpe_pa']
    acc_err_data = d['accel_err']
    if target_dataset == "3dpw":
        mpvpe_data = d['mpvpe']

    seq_lens = []
    if SAVE_SEQ_LENS == True:
        mpjpe_vals_all = []
        for i in range(len(mpjpe_data)):
            seq_lens.append(mpjpe_data[i].shape[0])
        seq_lens = np.array(seq_lens)
        np.save(f"{target_dataset}_seq_lens.npy", seq_lens)
        print(seq_lens.shape)
    else:
        seq_lens = np.load(f"{target_dataset}_seq_lens.npy")

    mpjpe_vals = np.concatenate(mpjpe_data)
    print("Num frames: ", mpjpe_vals.shape)
    pampjpe_vals = np.concatenate(pampjpe_data)
    acc_err_vals = np.concatenate(acc_err_data)
    if target_dataset == "3dpw":
        mpvpe_vals = np.concatenate(mpvpe_data)

    # plot_hist(mpjpe_vals, f"output/error_arrays/{target_dataset}_mpjpe_hist_full.png")
    # plot_hist(pampjpe_vals, f"output/error_arrays/{target_dataset}_pampjpe_hist_full.png")
    # plot_hist(acc_err_vals, f"output/error_arrays/{target_dataset}_acc_err_hist_full.png")
    # if target_dataset == "3dpw":
    #     plot_hist(mpvpe_vals, f"output/error_arrays/{target_dataset}_mpvpe_full.png")
    
    plot_all_errors(mpjpe_data, f"outputs/error_arrays/{target_dataset}_mpjpe_bar_plot.png")
    plot_all_errors(pampjpe_data, f"outputs/error_arrays/{target_dataset}_pampjpe_bar_plot.png")
    plot_all_errors(acc_err_data, f"outputs/error_arrays/{target_dataset}_acc_err_bar_plot.png")
    if target_dataset == "3dpw":
        plot_all_errors(mpvpe_data, f"outputs/error_arrays/{target_dataset}_mpvpe_bar_plot.png")
    
