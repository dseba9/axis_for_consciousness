
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem

# ============================================================
# CONFIG
# ============================================================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# ============================================================
# COLORS
# ============================================================
dataset_color = {
    "anestesia" : "#E69F00",
    "dmt"       : "#CC79A7",
    "lsd"       : "#009E73",
    "modafinil" : "#F0E442",
    "ucla"      : "#0072B2"
}

def get_fam(d):
    if "anestesia" in d: return "anestesia"
    if "dmt" in d: return "dmt"
    if "lsd" in d: return "lsd"
    if "modafinil" in d: return "modafinil"
    if "ucla" in d: return "ucla"
    return "ucla"

# ============================================================
# DATA LOADING & SELECTION
# ============================================================
df = pd.read_csv('../data/AAL_all_data_combined.csv')

# Use nice labels map
# Use nice labels map
dataset_label_map = {
    "anestesia_block1": "Wake",
    "anestesia_block2": "Sedation",
    "anestesia_block3": "Deep",
    "anestesia_block4": "Recovery",
    "dmt_dmt": "DMT",
    "dmt_plcb": "Placebo",
    "lsd": "LSD",
    "lsd_plcb": "Placebo",
    "modafinil": "Modafinil",
    "modafinil_placebo": "Placebo",
    "ucla_schz": "Schizophrenia",
    "ucla_control": "Control"
}

# ============================================================
# SORTING LOGIC
# ============================================================
# We want to sort conditions by their MEAN SampEn
# We will do this separately for dSW and dFC if needed, or global?
# User said "ordenadas por valor de entropia". Usually implies sorting per metric.
# Because the order might differ for dSW vs dFC.

def get_sorted_conditions(df_metric):
    means = df_metric.groupby('dataset')['SampEn'].mean()
    # Filter only ones in our map
    means = means[means.index.isin(dataset_label_map.keys())]
    return means.sort_values().index.tolist()

# ============================================================
# RAINCLOUD PLOT FUNCTION
# ============================================================
def plot_raincloud_sorted(ax, df_metric, title, ylabel):
    conditions = get_sorted_conditions(df_metric)
    
    # Prepare data list
    series_list = []
    labels = []
    colors = []
    
    for c in conditions:
        s = df_metric[df_metric['dataset'] == c]['SampEn']
        series_list.append(s)
        labels.append(dataset_label_map[c])
        colors.append(dataset_color[get_fam(c)])
        
    x = np.arange(len(conditions))
    
    # 1. Half-Violin (Right)
    parts = ax.violinplot(series_list, positions=x, widths=0.8,
                          showmeans=False, showextrema=False)
    
    for i, b in enumerate(parts["bodies"]):
        b.set_facecolor(colors[i])
        b.set_alpha(0.3)
        b.set_edgecolor("none")
        # Cut left half (keep x >= mean)
        verts = b.get_paths()[0].vertices
        xm = verts[:,0].mean()
        verts[:,0] = np.maximum(verts[:,0], xm)

    # 2. Jitter Dots (Center/Leftish)
    for i, s in enumerate(series_list):
        if len(s) == 0: continue
        # Jitter centered on x[i]
        jitter = (np.random.rand(len(s)) - 0.5) * 0.15
        ax.scatter(x[i] + jitter, s, s=40, alpha=0.6,
                   color=colors[i], edgecolors='none', zorder=2)

    # 3. Mean + ErrorBar (Black)
    means = [s.mean() if len(s)>0 else np.nan for s in series_list]
    sems  = [s.std()/np.sqrt(len(s)) if len(s)>0 else np.nan for s in series_list]
    
    ax.errorbar(x, means, yerr=sems, fmt='none', ecolor='black', capsize=8, lw=2, zorder=3)
    ax.scatter(x, means, s=80, color='black', zorder=4)

    # Styles
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=11)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold', pad=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add subtle background bars for family? (Optional, user didn't ask but snippet had it)
    # User said "igual a las otras" (Raincloud). Snippet had bars AND raincloud.
    # But Fig 2/3 don't have bars. I'll skip bars to match Fig 2/3 aesthetic.

# ============================================================
# MAIN FIGURE
# ============================================================
fig, axes = plt.subplots(2, 1, figsize=(14, 10), constrained_layout=True)

# Panel A: dSW
df_dsw = df[df['metric'] == 'dSW']
plot_raincloud_sorted(axes[0], df_dsw, "A) SampEn dSW", "SE")

# Panel B: dFC
df_dfc = df[df['metric'] == 'dFC']
plot_raincloud_sorted(axes[1], df_dfc, "B) SampEn dFC", "SE")

plt.savefig('../output/Figure1_Ordered_Entropy.svg')
plt.savefig('../output/Figure1_Ordered_Entropy.png', dpi=300)
print("Saved Figure1_Ordered_Entropy.svg and .png")
