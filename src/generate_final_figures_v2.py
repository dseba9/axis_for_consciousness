
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# ============================================================
# GLOBAL CONFIG
# ============================================================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['svg.fonttype'] = 'none' # Edited for SVG text editing
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

# ============================================================
# DATASET COLORS
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
    return "ucla" # Fallback

def get_significance_symbol(p):
    if p < 0.001: return '***'
    if p < 0.01: return '**'
    if p < 0.05: return '*'
    return 'ns'

def add_stat_bar(ax, x1, x2, y, h, p_val):
    if p_val >= 0.05: return
    symbol = get_significance_symbol(p_val)
    # Check if horizontal bar already exists very close? No, straightforward logic 
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='k')
    ax.text((x1+x2)*.5, y+h, symbol, ha='center', va='bottom', color='k', fontsize=12)

def plot_panel_snippet_style(ax, df_sub, conditions, labels, title, metric_name, y_col='SampEn'):
    # Prepare Data
    series_list = []
    for c in conditions:
        s = df_sub[df_sub['dataset'] == c][y_col]
        series_list.append(s)
        
    x = np.arange(len(conditions))
    
    # ---------- Half-violin (Snippet Style) ----------
    parts = ax.violinplot(series_list, positions=x, widths=0.8,
                          showmeans=False, showextrema=False)

    for i, b in enumerate(parts["bodies"]):
        fam_key = get_fam(conditions[i])
        col = dataset_color[fam_key]
        b.set_facecolor(col)
        b.set_alpha(0.25)
        b.set_edgecolor("none")

        # cut left half: Keep only x >= mean (Right side)
        verts = b.get_paths()[0].vertices
        xm = verts[:,0].mean()
        verts[:,0] = np.maximum(verts[:,0], xm)

    # ---------- Scatter dots (Snippet Style) ----------
    for i, s in enumerate(series_list):
        if len(s) == 0: continue
        fam_key = get_fam(conditions[i])
        col = dataset_color[fam_key]
        
        # Center jitter
        jitter = (np.random.rand(len(s)) - 0.5) * 0.12
        ax.scatter(x[i] + jitter, s, s=60, alpha=0.6,
                   color=col, edgecolors='none', zorder=2)

    # ---------- Mean + SEM (Snippet Style w/o points, just errorbar + black dot) ----------
    means = [s.mean() if len(s) > 0 else np.nan for s in series_list]
    sems  = [s.std() / np.sqrt(len(s)) if len(s) > 0 else np.nan for s in series_list]

    ax.errorbar(x, means, yerr=sems, fmt='none', ecolor='black', capsize=8, lw=2, zorder=3)
    ax.scatter(x, means, s=100, color='black', zorder=4)

    # ---------- Statistics (User Provided) ----------
    # P-value lookup table (Metric -> Ref_Cond -> Comp_Cond -> p_value)
    p_values = {
        'dSW': {
            'ucla_control': {'ucla_schz': 0.000},
            'lsd_plcb': {'lsd': 0.027},
            'dmt_plcb': {'dmt_dmt': 0.075},
            'anestesia_block1': {
                'anestesia_block2': 0.036,
                'anestesia_block3': 0.003,
                'anestesia_block4': 0.947
            },
            'modafinil_placebo': {'modafinil': 0.072}
        },
        'dFC': {
            'ucla_control': {'ucla_schz': 0.000},
            'lsd_plcb': {'lsd': 0.0007},
            'dmt_plcb': {'dmt_dmt': 0.0009},
            'anestesia_block1': {
                'anestesia_block2': 0.0156,
                'anestesia_block3': 0.0117,
                'anestesia_block4': 0.5632
            },
            'modafinil_placebo': {'modafinil': 0.941}
        }
    }

    # Calculate Y for bars
    all_vals = pd.concat(series_list)
    y_max = all_vals.max()
    curr_y = y_max + 0.1 * (all_vals.max() - all_vals.min())
    step = 0.12 * (all_vals.max() - all_vals.min())
    
    ref_cond = conditions[0]
    
    # Iterate comparisons vs Ref (index 0)
    for i in range(1, len(conditions)):
        comp_cond = conditions[i]
        
        # Look up p-value
        try:
            # Get dict for metric
            d_met = p_values.get(metric_name, {})
            # Get dict for ref_cond (handle case where ref key missing)
            d_ref = d_met.get(ref_cond, {})
            # Get value. Default 1.0
            p = d_ref.get(comp_cond, 1.0)
            
            print(f"Comparing {metric_name}: {ref_cond} vs {comp_cond} -> p={p}")
        except:
            p = 1.0
            print(f"Comparing {metric_name}: {ref_cond} vs {comp_cond} -> FAILED lookup")
            
        if p < 0.05:
            add_stat_bar(ax, 0, i, curr_y, step * 0.4, p)
            curr_y += step

    # ---------- Axes / Formatting ----------
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_ylabel("SE")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def generate_figure(df, metric, filename):
    df_metric = df[df['metric'] == metric]
    
    # 5 Panels
    fig, axes = plt.subplots(1, 5, figsize=(18, 6), constrained_layout=True)
    
    # Anesthesia
    conds_anes = ['anestesia_block1', 'anestesia_block2', 'anestesia_block3', 'anestesia_block4']
    labels_anes = ['Wake', 'Light', 'Deep', 'Recovery']
    plot_panel_snippet_style(axes[0], df_metric, conds_anes, labels_anes, "A) Anesthesia", metric, y_col='SampEn')
    
    # Schizophrenia
    conds_sch = ['ucla_control', 'ucla_schz']
    labels_sch = ['Control', 'Schizophrenia']
    plot_panel_snippet_style(axes[1], df_metric, conds_sch, labels_sch, "B) Schizophrenia", metric, y_col='SampEn')
    
    # LSD
    conds_lsd = ['lsd_plcb', 'lsd']
    labels_lsd = ['Placebo', 'LSD']
    plot_panel_snippet_style(axes[2], df_metric, conds_lsd, labels_lsd, "C) LSD", metric, y_col='SampEn')
    
    # Modafinil
    conds_mod = ['modafinil_placebo', 'modafinil']
    labels_mod = ['Placebo', 'Modafinil']
    plot_panel_snippet_style(axes[3], df_metric, conds_mod, labels_mod, "D) Modafinil", metric, y_col='SampEn')
    
    # DMT
    conds_dmt = ['dmt_plcb', 'dmt_dmt']
    labels_dmt = ['Placebo', 'DMT']
    plot_panel_snippet_style(axes[4], df_metric, conds_dmt, labels_dmt, "E) DMT", metric, y_col='SampEn')
    
    plt.savefig(filename, format='svg')
    plt.savefig(filename.replace('.svg', '.png'), dpi=300)
    print(f"Saved {filename} and PNG")

# Main
df = pd.read_csv('../data/AAL_all_data_combined.csv')

generate_figure(df, 'dSW', '../output/Figure2_dSW_Final_SnippetStyle.svg')
generate_figure(df, 'dFC', '../output/Figure3_dFC_Final_SnippetStyle.svg')
