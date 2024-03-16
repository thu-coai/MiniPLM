import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.ndimage import gaussian_filter1d
from tqdm import tqdm


base_path = "/home/lidong1/yuxian/sps-toy/results/toy/trm/toy-trm-l2-5k-ln-ts-64/bs512-lr0.1-tn16384-dn512-e4000/-0.8_30-eval_opt/10-20-7"
alpha_base_path = "/home/lidong1/yuxian/sps-toy/results/toy/trm/toy-trm-l2-5k-ln-ts-64/bs512-lr0.1-tn16384-dn512-e4000"

split = "test"

paths = [
    (os.path.join(base_path, "opt_alpha_0.1/0"), "opt_alpha_0"),
    (os.path.join(base_path, "opt_alpha_0.1/1"), "opt_alpha_1"),
    (os.path.join(base_path, "opt_alpha_0.1/2"), "opt_alpha_2"),
    (os.path.join(base_path, "opt_alpha_0.1/3"), "opt_alpha_3"),
    (os.path.join(base_path, "opt_alpha_0.1/4"), "opt_alpha_4"),
    (os.path.join(base_path, "opt_alpha_0.1/5"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.1/6"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.1/7"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/0"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/1"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/2"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/3"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/4"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/5"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/10"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.2/15"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/0"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/1"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/2"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/3"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/4"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/5"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/6"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/7"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/8"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/9"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/10"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/11"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/12"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/13"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/14"), "opt_alpha_5"),
    (os.path.join(base_path, "opt_alpha_0.4/15"), "opt_alpha_5"),
    # (os.path.join(base_path, "opt_alpha_0.4/16"), "opt_alpha_5"),
    # (os.path.join(base_path, "opt_alpha_0.4/17"), "opt_alpha_5"),
    # (os.path.join(base_path, "opt_alpha_0.4/18"), "opt_alpha_5"),
    # (os.path.join(base_path, "opt_alpha_0.4/19"), "opt_alpha_5"),
]

plot, ax = plt.subplots(1, 1, figsize=(4, 2.6))


step_min = 0
step_max = 100
vocab_size = 5000
tot_info = 4000

all_neg_IF_alpha_0_ratio, all_areas = [], []

cm = plt.colormaps['coolwarm']

for path in tqdm(paths):
    path = path[0]
    alpha_lr = path.split("/")[-2].split("_")[-1]
    alpha_epoch = path.split("/")[-1]
    alpha_path = os.path.join(alpha_base_path, f"-0.8_30-opt-{alpha_lr}-0/10-20-7/epoch_{alpha_epoch}/opt_alpha.pt")
    alpha = torch.load(alpha_path, map_location="cpu").numpy()
    all_loss = torch.load(os.path.join(path, f"all_loss.pt"), map_location="cpu")
    loss = all_loss[0] if split == "dev" else all_loss[1]
    IFs = torch.load(os.path.join(path, f"all_{split}_IF.pt"), map_location="cpu")
        
    IF = np.array(IFs[0])
    
    IF = IF[:step_max]
    alpha = alpha[:step_max]
    
    alpha_neg_IF = alpha[IF < 0]
    alpha_neg_IF = alpha_neg_IF.reshape(-1)
    num_alpha_neg_IF_0 = np.sum((alpha_neg_IF < 1e-8))
    all_neg_IF_alpha_0_ratio.append(num_alpha_neg_IF_0 / alpha_neg_IF.shape[0])
    area = sum(loss)
    all_areas.append(area)

# all_losses = [gaussian_filter1d(loss, sigma=1) for loss in all_losses]
# all_IF_ratios = [gaussian_filter1d(IF_ratio, sigma=100) for IF_ratio in all_IF_ratios]

all_areas = np.array(all_areas)
print(all_areas)
all_cp_rate = tot_info * np.log2(vocab_size) / all_areas
print(all_cp_rate)

all_cp_rate = np.array(all_cp_rate)
all_neg_IF_alpha_0_ratio = np.array(all_neg_IF_alpha_0_ratio)
sort_idx = np.argsort(all_cp_rate)
all_cp_rate = all_cp_rate[sort_idx]
all_neg_IF_alpha_0_ratio = all_neg_IF_alpha_0_ratio[sort_idx]

ax.plot(all_cp_rate, all_neg_IF_alpha_0_ratio * 100, marker="o", color="green")
ax.scatter(all_cp_rate[-1], all_neg_IF_alpha_0_ratio[-1] * 100, color="red", marker="*", s=140, label=r"Near-Optimal Learning", zorder=10)
ax.scatter(all_cp_rate[0], all_neg_IF_alpha_0_ratio[0] * 100, color="blue", marker="s", s=50, label=r"Conventional Learning", zorder=10)
# 
# ax.set_xscale("log")
# ax.set_yscale("log")
ax.set_xlabel(r"Compresson Rate ($\operatorname{CR}$)", fontsize=14)
ax.set_ylabel(r"Fraction of $\gamma_{n,t}=0$ (%)", fontsize=14)
# set the font size of x-axis and y-axis
ax.tick_params(axis='both', which='both', labelsize=14)
# ax.invert_xaxis()

plt.legend(fontsize=12, loc="upper left")

# plt.title("Transformer Language Modeling", fontsize=14)
plt.savefig(os.path.join("/home/lidong1/yuxian/sps-toy/results/toy/arxiv",
            f"{split}_neg_if.pdf"), bbox_inches="tight")
plt.close()