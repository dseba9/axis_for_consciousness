# A Shared Entropic Axis Organizes Conscious Brain States Across Domains

This repository provides the code, data, and instructions necessary to reproduce the figures and results presented in our study. We introduce a unified geometric framework for analyzing neural complexity and functional connectivity across different states of consciousness (Anesthesia, Psychedelics, Schizophrenia, and Modafinil). 

The study calculates **Sample Entropy (SE)** across two orthogonal dimensions: 
1. Topological flexibility (dynamic Small-Worldness, **dSW**) 
2. Coupling stability (dynamic Functional Connectivity, **dFC**)

## 📄 Overview

The primary goal of this study is to demonstrate that heterogeneous states of consciousness can be embedded along a shared dynamical axis derived from the entropy of large-scale brain network reconfiguration. By using an identical analytical pipeline across diverse datasets, we show that consciousness arises within a constrained window of dynamical complexity.

**Key Findings:**
*   **A Continuous Entropic Gradient:** Reduced-awareness states (propofol anesthesia) occupy the low-entropy end of this axis, whereas expanded or dysregulated states (psychedelics and schizophrenia) occupy higher positions.
*   **Orthogonal Dimensions of Dynamics:** The topological entropy axis (SE dSW) is largely independent of overall connectivity strength (SE dFC). While both anesthetics and schizophrenia modulate these dimensions in tandem (decreasing and increasing both, respectively), psychedelics uniquely expand the temporal repertoire of spatial network configurations (high SE dSW) while rigidifying overall connectivity magnitude (low SE dFC).

## 📂 Repository Structure

*   **`src/`**: Python source code and analysis scripts used to compute metrics and generate figures.
    *   `generate_2d_map_clean.py`: Visualization of the 2D consciousness state map (Figure 4).
    *   `generate_figure1_sorted.py`: Generation of Raincloud plots for entropy distributions (Figure 1).
    *   `generate_final_figures_v2.py`: Generation of comparative violin plots (Figures 2 & 3).
*   **`data/`**: Curated input datasets required to replicate the analyses (e.g., `AAL_all_data_combined.csv`).
*   **`output/`**: Directory where generated figures, SVGs, and discrepancy reports are exported.
*   **`docs/`**: Scientific documentation, including the technical report and paper drafts.

## 🚀 Installation & Reproducibility

### Prerequisites

We recommend using a virtual environment (Python 3.9+). Install the required dependencies using the provided `requirements.txt`:

```bash
# Clone the repository
git clone https://github.com/dseba9/axis_for_consciousness.git
cd axis_for_consciousness

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Reproducing the Figures

The scripts are designed to be executed directly from inside the `src/` directory.

```bash
cd src
```

* **To generate the main 2D map of consciousness (Fig 4):**
  ```bash
  python generate_2d_map_clean.py
  ```

* **To generate the comparative Violin Plots (Figs 2 & 3):**
  ```bash
  python generate_final_figures_v2.py
  ```

* **To reproduce the individual state raincloud distributions (Fig 1):**
  ```bash
  python generate_figure1_sorted.py
  ```

All generated figures will be automatically saved in the `output/` folder.

## 👥 Authors and Acknowledgements

This work is conducted by the *Cognitive Science Group (IIPsi, CONICET-UNC)* in collaboration with the *University of Cambridge*. 

Theoretical frameworks build upon the *Entropic Brain Hypothesis (Carhart-Harris)* and the network dynamics investigated by Coppola et al.

### Key References

*   **Coppola, P., et al. (2022).** [Network dynamics scale with levels of awareness](https://doi.org/10.1016/j.neuroimage.2022.119128). *NeuroImage*, 254, 119128.
*   **Carhart-Harris, R. L. (2018).** The entropic brain - revisited. *Neuropharmacology*, 142, 167-178.
