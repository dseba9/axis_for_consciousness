
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
# COLORS (Consolidated)
# ============================================================
dataset_color = {
    "anestesia" : "#E69F00",
    "dmt"       : "#CC79A7",
    "lsd"       : "#009E73",
    "modafinil" : "#F0E442",
    "ucla"      : "#0072B2"
}

# ============================================================
# DATA PREP
# ============================================================
df = pd.read_csv('../data/AAL_all_data_combined.csv')

# Define studies and controls
studies = {
    'Anesthesia': {'Control': 'anestesia_block1', 'Conditions': ['anestesia_block1', 'anestesia_block2', 'anestesia_block3', 'anestesia_block4']},
    'LSD': {'Control': 'lsd_plcb', 'Conditions': ['lsd_plcb', 'lsd']},
    'DMT': {'Control': 'dmt_plcb', 'Conditions': ['dmt_plcb', 'dmt_dmt']},
    'Modafinil': {'Control': 'modafinil_placebo', 'Conditions': ['modafinil_placebo', 'modafinil']},
    'Schizophrenia': {'Control': 'ucla_control', 'Conditions': ['ucla_control', 'ucla_schz']}
}

# Normalize (Z-Score)
normalized_dfs = []
for study, info in studies.items():
    control_cond = info['Control']
    conditions = info['Conditions']
    mask = df['dataset'].isin(conditions)
    study_df = df[mask].copy()
    
    # Calculate Mean/Std of Control for this Study
    control_dsw = study_df[(study_df['metrics'] == 'dSW') & (study_df['dataset'] == control_cond) if 'metrics' in study_df.columns else (study_df['metric'] == 'dSW') & (study_df['dataset'] == control_cond)]['SampEn']
    control_dfc = study_df[(study_df['metrics'] == 'dFC') & (study_df['dataset'] == control_cond) if 'metrics' in study_df.columns else (study_df['metric'] == 'dFC') & (study_df['dataset'] == control_cond)]['SampEn']
    
    # Fix potential column name mismatch
    metric_col = 'metric' if 'metric' in study_df.columns else 'metrics'
    
    mu_dsw = study_df[(study_df[metric_col] == 'dSW') & (study_df['dataset'] == control_cond)]['SampEn'].mean()
    std_dsw = study_df[(study_df[metric_col] == 'dSW') & (study_df['dataset'] == control_cond)]['SampEn'].std()
    
    mu_dfc = study_df[(study_df[metric_col] == 'dFC') & (study_df['dataset'] == control_cond)]['SampEn'].mean()
    std_dfc = study_df[(study_df[metric_col] == 'dFC') & (study_df['dataset'] == control_cond)]['SampEn'].std()
    
    def get_z(row):
        val = row['SampEn']
        if row[metric_col] == 'dSW': return (val - mu_dsw) / std_dsw
        elif row[metric_col] == 'dFC': return (val - mu_dfc) / std_dfc
        return val

    study_df['Z_SampEn'] = study_df.apply(get_z, axis=1)
    normalized_dfs.append(study_df)

norm_df = pd.concat(normalized_dfs)
metric_col = 'metric' if 'metric' in norm_df.columns else 'metrics'

# Pivot for aggregation
norm_df['unique_id'] = norm_df['dataset'] + '_' + norm_df['Subject'].astype(str)
pivot_df = norm_df.pivot_table(index=['dataset', 'unique_id'], columns=metric_col, values='Z_SampEn').reset_index()

# Stats
stats = pivot_df.groupby('dataset').agg({
    'dSW': ['mean', 'sem'],
    'dFC': ['mean', 'sem']
}).reset_index()

# ============================================================
# PLOTTING
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8)) # Square nice for 2D map

# Reference Lines
ax.axhline(0, color='gray', linestyle=':', alpha=0.4, linewidth=1)
ax.axvline(0, color='gray', linestyle=':', alpha=0.4, linewidth=1)

# Style Map
# Anesthesia
anest_style = {
    'anestesia_block2': {'label': 'Sedation', 'color': dataset_color['anestesia']},
    'anestesia_block3': {'label': 'LOC', 'color': dataset_color['anestesia']}, # Darker orange manually? Or stick to family color?
    # To distinguish levels, maybe vary alpha or saturation manually? 
    # User asked for "Figure 1 aesthetics". The uploaded image had distinct colors for Sed/LOC.
    # But new figures use single color per family.
    # Let's use the family color, maybe markers or labels distinguish them.
    # Or just use the family color for all.
}

# Add slight variation for Anesthesia levels if strictly needed, but consistent aesthetic implies family color.
# Actually, the user wants "Mantener la estetica". In Fig 2/3, Anesthesia is all Orange.
# So I will use same orange.

style_map = {
    'anestesia_block2': {'label': 'Sedation', 'color': dataset_color['anestesia'], 'marker': 'o'},
    'anestesia_block3': {'label': 'Deep', 'color': dataset_color['anestesia'], 'marker': 'o'}, # Deep
    # 'anestesia_block4': Recovery usually not plotted in summary maps unless requested, user image showed only Sed/LOC.
    
    'lsd': {'label': 'LSD', 'color': dataset_color['lsd'], 'marker': 'o'},
    'dmt_dmt': {'label': 'DMT', 'color': dataset_color['dmt'], 'marker': 'o'},
    'modafinil': {'label': 'Modafinil', 'color': dataset_color['modafinil'], 'marker': 'o'},
    'ucla_schz': {'label': 'Schizophrenia', 'color': dataset_color['ucla'], 'marker': 'o'}
}

# Plot Baseline
ax.errorbar(0, 0, xerr=0, yerr=0, fmt='o', color='black', ms=12, label='Baseline', zorder=10)
ax.text(0.1, 0.1, 'Wake', fontsize=12, fontweight='bold', ha='left', va='bottom')

# Plot Conditions
conditions_to_plot = ['anestesia_block2', 'anestesia_block3', 'lsd', 'dmt_dmt', 'modafinil', 'ucla_schz']

x_vals = []
y_vals = []

for cond in conditions_to_plot:
    if cond not in stats['dataset'].values: continue
    
    row = stats[stats['dataset'] == cond]
    x = row[('dFC', 'mean')].values[0]
    y = row[('dSW', 'mean')].values[0]
    x_err = row[('dFC', 'sem')].values[0]
    y_err = row[('dSW', 'sem')].values[0]
    
    x_vals.append(x + x_err)
    x_vals.append(x - x_err)
    y_vals.append(y + y_err)
    y_vals.append(y - y_err)
    
    style = style_map.get(cond, {})
    color = style.get('color', 'gray')
    label = style.get('label', cond) # Short label
    
    # Arrow
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=color, alpha=0.4, lw=2.5))
    
    # Point
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='o', color=color, 
                ms=12, capsize=5, elinewidth=2, markeredgecolor='none', label=label)
    
    # Label Text (Offsets to avoid clutter)
    offset_x, offset_y = 0.15, 0.15
    if 'Sedation' in label: offset_x = -0.5; offset_y = -0.2
    if 'Deep' in label: offset_x = -0.4; offset_y = -0.3
    if 'LSD' in label: offset_x = -0.4; offset_y = 0.2
    if 'Schiz' in label: offset_x = 0.1; offset_y = 0.1
    if 'DMT' in label: offset_x = 0.1; offset_y = -0.1
    
    ax.text(x + offset_x, y + offset_y, label, color=color, fontweight='bold', fontsize=12)

# Axis Labels (Clean)
ax.set_xlabel('SE dFC (Z-Score)', fontsize=14)
ax.set_ylabel('SE dSW (Z-Score)', fontsize=14)

# Aesthetics Clean-up
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Ensure bottom/left are visible
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)

# Limits (User Specified Tight Zoom)
ax.set_xlim(-1.8, 1.5)
ax.set_ylim(-1.5, 1.5)

# Ensure Zero is visually centered? It is if limits are symmetric.
# The previous plot might have looked off-center if the aspect ratio wasn't 1.
# ax.set_aspect('equal', 'box') # Remove fixed aspect to fill the rectangular limits correctly

# Save
plt.tight_layout()
plt.savefig('../output/Figure4_2D_Map_Clean.svg', format='svg')
plt.savefig('../output/Figure4_2D_Map_Clean.png', dpi=300)
print("Saved Figure4_2D_Map_Clean.svg and .png")
