import numpy as np
from matplotlib import pyplot as plt
import os
import shutil
from tqdm import tqdm
import argparse
import time


parser = argparse.ArgumentParser(description="Video making script")
parser.add_argument("--pdt", type=float, default=10e-6, help="Pixel dwell time used for the experiment (in s)")
parser.add_argument("--files_path", type=str, default="", help="Path to the saved npy and ffconcant files")
parser.add_argument("--delete_after", type=bool, default=True, help="Wether or not the figures are deleted after")
args = parser.parse_args()

# jpourrais mettre une option pour delete le folder avec les images après
delete_figures_after = args.delete_after
# These lines are the only ones that should be changed when we want to make new videos
# files_path = r"D:\SCHOOL\Maitrise\H2021\Recherche\data_generation\split\test_1"
files_path = args.files_path
pdt = args.pdt   # is there a way to get this value directly from the exp script?

# for ffmpeg, I think I don't have a choice but to save the figures on my computer
# make a directory for the figures
if not os.path.exists(files_path + "/figures"):
    os.mkdir(files_path + "/figures")

# read the datamaps, confocals, steds, dict
datamaps = np.load(files_path + "/datamaps.npy")
confocals = np.load(files_path + "/confocals.npy")
steds = np.load(files_path + "/steds.npy")
idx_type = np.load(files_path + "/idx_type_dict.npy", allow_pickle=True).item()

min_datamap, max_datamap = np.min(datamaps), np.max(datamaps)
min_confocal, max_confocal = np.min(confocals), np.max(confocals)
min_sted, max_sted = np.min(steds), np.max(steds)

d_idx, c_idx, s_idx = 0, 0, 0
# Generate the first figure
fig, axes = plt.subplots(1, 3, figsize=(15, 5), tight_layout=True)

dmap_imshow = axes[0].imshow(datamaps[d_idx], vmin=min_datamap, vmax=max_datamap)
axes[0].set_title(f"Datamap")
fig.colorbar(dmap_imshow, ax=axes[0], fraction=0.04, pad=0.05)

confocal_imshow = axes[1].imshow(confocals[c_idx], vmin=min_confocal, vmax=max_confocal)
axes[1].set_title(f"Confocal (Ground truth) \n "
                  f"1/3 the resolution of STED")
fig.colorbar(confocal_imshow, ax=axes[1], fraction=0.04, pad=0.05)

sted_imshow = axes[2].imshow(steds[s_idx], vmin=min_sted, vmax=max_sted)
axes[2].set_title(f"STED acquisition")
fig.colorbar(sted_imshow, ax=axes[2], fraction=0.04, pad=0.05)

fig.suptitle(f"Acquisition will start in 5 seconds")
plt.savefig(files_path + f"/figures/0.png")
plt.close()

# mettre un tqdm range or something maybe? :)
keys_list = sorted(idx_type.keys())
for idx, key in enumerate(tqdm(keys_list)):
    if idx_type[key] == "datamap":
        d_idx += 1
    elif idx_type[key] == "confocal":
        c_idx += 1
    elif idx_type[key] == "sted":
        s_idx += 1
    else:
        print(f"FORBIDDEN UNKNOWN")

    if key != keys_list[-1]:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), tight_layout=True)

        dmap_imshow = axes[0].imshow(datamaps[d_idx], vmin=min_datamap, vmax=max_datamap)
        axes[0].set_title(f"Datamap")
        fig.colorbar(dmap_imshow, ax=axes[0], fraction=0.04, pad=0.05)

        confocal_imshow = axes[1].imshow(confocals[c_idx], vmin=min_confocal, vmax=max_confocal)
        axes[1].set_title(f"Confocal (Ground truth) \n "
                          f"1/3 the resolution of STED")
        fig.colorbar(confocal_imshow, ax=axes[1], fraction=0.04, pad=0.05)

        sted_imshow = axes[2].imshow(steds[s_idx], vmin=min_sted, vmax=max_sted)
        axes[2].set_title(f"STED acquisition")
        fig.colorbar(sted_imshow, ax=axes[2], fraction=0.04, pad=0.05)

        fig.suptitle(f"Acquisition in progress...")
        plt.savefig(files_path + f"/figures/{key + 1}.png")
        plt.close()

    else:
        for i in range(2):
            fig, axes = plt.subplots(1, 3, figsize=(15, 5), tight_layout=True)

            dmap_imshow = axes[0].imshow(datamaps[d_idx], vmin=min_datamap, vmax=max_datamap)
            axes[0].set_title(f"Datamap")
            fig.colorbar(dmap_imshow, ax=axes[0], fraction=0.04, pad=0.05)

            confocal_imshow = axes[1].imshow(confocals[c_idx], vmin=min_confocal, vmax=max_confocal)
            axes[1].set_title(f"Confocal (Ground truth) \n "
                              f"1/3 the resolution of STED")
            fig.colorbar(confocal_imshow, ax=axes[1], fraction=0.04, pad=0.05)

            sted_imshow = axes[2].imshow(steds[s_idx], vmin=min_sted, vmax=max_sted)
            axes[2].set_title(f"STED acquisition")
            fig.colorbar(sted_imshow, ax=axes[2], fraction=0.04, pad=0.05)

            fig.suptitle(f"Acquisition has ended")
            plt.savefig(files_path + f"/figures/{key + 1}.png")
            plt.close()


# calculer le temps total du video en secondes et l'enregistrer qqpart pour
total_duration = 5 + (keys_list[-1] * pdt * 10) + 10

# copy the audio file over, :)
# regarder si la file est là avant
mp3_file = "D:/SCHOOL/Maitrise/H2021/Recherche/data_generation/time_integration/ffmpeg_video_tests/Trance_009_Sound_System_Dreamscape_HD.mp3"
shutil.copy(mp3_file, files_path + "/figures/")
shutil.copy(files_path + "/in.ffconcat", files_path + "/figures")

# call cmd lines to make the video
os.chdir(files_path + "/figures/")
os.system(fr'cmd /c "ffmpeg -i in.ffconcat -i Trance_009_Sound_System_Dreamscape_HD.mp3 -c:v libx264 -preset ultrafast -crf 0 -c:a copy -vf fps=25 out.avi"')
os.chdir(files_path + "/figures/")
os.system(fr'cmd /c "ffmpeg -ss 0 -i out.avi -t {total_duration} -c copy experiment_video.avi"')
shutil.move(files_path + "/figures/experiment_video.avi", files_path + "/experiment_video.avi")

# delete le .mp3, .avi et .ffconcat du fichier de figures
os.remove(files_path + "/figures/in.ffconcat")
os.remove(files_path + "/figures/out.avi")
os.remove(files_path + "/figures/Trance_009_Sound_System_Dreamscape_HD.mp3")

if delete_figures_after:
    for f in os.listdir(files_path + "/figures/"):
        os.remove(os.path.join(files_path + "/figures/", f))
    # os.rmdir(files_path + "/figures")   # can't delete the folder for some reasone
