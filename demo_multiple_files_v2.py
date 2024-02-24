import subprocess

# file_paths = ["/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/3DPW/courtyard_drinking_00.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/3DPW/downtown_downstairs_00.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/3DPW/outdoors_fencing_01.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/Human3_6M/S11/_ALL_1.60457274.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/Human3_6M/S11/Eating_1.60457274.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/Human3_6M/S11/SittingDown_1.55011271.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/Human3_6M/S11/SittingDown_1.58860488.mp4",
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/internet_videos/demo.mp4",
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/MPI_INF_3DHP/TS2/TS2.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/MPI_INF_3DHP/TS3/TS3.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/MPI_INF_3DHP/TS4/TS4.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/new/MPI_INF_3DHP/TS6/TS6.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/1_DoZZRqd5.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/2023_05_27_YT_04.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/62959_3.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/62992_5.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/80920_3.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/challenging_for_PMCE_GLOT/Dance_2.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_4/MPI.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_4/mule_kick.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_4/outdoors_climbing_02.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_4/walk_the_box.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_6/courtyard_backpack_00.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_7/62947_2.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_7/N3Office.mp4", 
# "/data/amogh/projects/smpl_fitting_tcs/data/20240117_For_Comparison/old/Fig_7/N3OpenArea.mp4"]

# names = ["new/3DPW/courtyard_drinking_00", 
# "new/3DPW/downtown_downstairs_00", 
# "new/3DPW/outdoors_fencing_01", 
# "new/Human3_6M/S11/_ALL_1.60457274", 
# "new/Human3_6M/S11/Eating_1.60457274", 
# "new/Human3_6M/S11/SittingDown_1.55011271", 
# "new/Human3_6M/S11/SittingDown_1.58860488",
# "new/internet_videos/demo",
# "new/MPI_INF_3DHP/TS2/TS2", 
# "new/MPI_INF_3DHP/TS3/TS3", 
# "new/MPI_INF_3DHP/TS4/TS4", 
# "new/MPI_INF_3DHP/TS6/TS6", 
# "old/challenging_for_PMCE_GLOT/1_DoZZRqd5", 
# "old/challenging_for_PMCE_GLOT/2023_05_27_YT_04", 
# "old/challenging_for_PMCE_GLOT/62959_3", 
# "old/challenging_for_PMCE_GLOT/62992_5", 
# "old/challenging_for_PMCE_GLOT/80920_3", 
# "old/challenging_for_PMCE_GLOT/Dance_2", 
# "old/Fig_4/MPI", 
# "old/Fig_4/mule_kick", 
# "old/Fig_4/outdoors_climbing_02", 
# "old/Fig_4/walk_the_box", 
# "old/Fig_6/courtyard_backpack_00", 
# "old/Fig_7/62947_2", 
# "old/Fig_7/N3Office", 
# "old/Fig_7/N3OpenArea"]

# num_files = len(file_paths)
# for idx in range(num_files):
#     file_path = file_paths[idx]
#     name = names[idx]
#     print("############################################################")
#     print(f"Evaluating: File #{idx+1}/{num_files}; Path: {file_path}")
#     print("############################################################")
#     command = ["python",
#     "demo.py",
#     "--file_type",
#     "video",
#     "--out_dir",
#     f"outputs/{name}",
#     "--vid_file",
#     f"{file_path}",
#     "--gpu",
#     "2",
#     "--save_pkl"]
#     print(f"Running command: {' '.join(command)}")
#     subprocess.call(command)

# file_paths = ["/data/groot/Datasets/i3db_dataset/i3DB/Scene04/VID_20180114_183708_lobby19-3.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene05/VID_20180114_184009_lobby18-1.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene07/VID_20171211_094511_lobby15.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene10/VID_20180114_190228_lobby22-1.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene11/VID_20171226_130716.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene12/VID_20180117_230045_office1-1.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene13/VID_20180120_174424_library3.mp4", 
# "/data/groot/Datasets/i3db_dataset/i3DB/Scene14/VID_20171014_114024_garden1.mp4"]

file_paths = [
"/data/groot/Datasets/i3db_dataset/i3DB/Scene04/Scene04.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene05/Scene05.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene07/Scene07.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene10/Scene10.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene11/Scene11.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene12/Scene12.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene13/Scene13.mp4", 
"/data/groot/Datasets/i3db_dataset/i3DB/Scene14/Scene14.mp4"
]


num_files = len(file_paths)
for idx in range(num_files):
    file_path = file_paths[idx]
    print("############################################################")
    print(f"Evaluating: File #{idx+1}/{num_files}; Path: {file_path}")
    print("############################################################")
    command = ["python",
    "./main/run_demo.py",
    "--vid_file",
    f"{file_path}",
    "--gpu",
    "0",
    "--save_pkl"]
    print(f"Running command: {' '.join(command)}")
    subprocess.call(command)
