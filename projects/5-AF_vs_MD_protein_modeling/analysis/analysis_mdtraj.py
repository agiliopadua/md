import mdtraj as md
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from mdtraj.formats.pdb.pdbstructure import PdbStructure

sns.set_theme(
    style="ticks",
    context="paper",palette='deep',
    rc={
        "axes.linewidth": 1.5,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.minor.size": 3,
        "ytick.minor.size": 3,
        "xtick.major.width": 1.2,
        "ytick.major.width": 1.2,
        "xtick.minor.width": 1.0,
        "ytick.minor.width": 1.0,
        "font.family": "sans-serif"
    }
)

def analyze_system(traj_file, top_file, ref_file, label):
    """
    Load trajectory and compute RMSD, RMSF, Rg, pLDDT and secondary structure
    Returns a pandas DataFrame.
    """
    traj = md.load(traj_file, top=top_file)
    ## AF structure
    ref = md.load_pdb(ref_file)

    # Select protein backbone for RMSD
    ca = traj.topology.select("name CA")
    ca_ref=ref.topology.select("name CA")

    traj_ca = traj.atom_slice(ca)
    ref_ca=ref.atom_slice(ca_ref)

    # Extract pLDDT from the B-factor field of each atom
    with open(ref_file) as f:
        struct = PdbStructure(f, load_all_models=True)
    atoms = list(struct.iter_atoms())
    plddt = np.array([atoms[i].temperature_factor for i in ca_ref])

    # RMSD (reference = first frame)
    # md.rmsd
    rmsd = # to fill

    # RMSF (per residue, backbone atoms) 
    # md.rmsf
    rmsf = # to fill

    # Radius of gyration (whole protein)  
    # md.compute_rg
    rg = # to fill

    # Time in ns (assuming typical 2 fs timestep)
    time_ns = traj.time / 1000.0

    df = pd.DataFrame({
        "time_ns": time_ns,
        "RMSD_nm": rmsd,
        "Rg_nm": rg,
        "system": label
    })

    # Compute DSSP secondary structure
    # simplified=True returns H (helix), E (sheet), C (coil)
    # md.compute_dssp
    ss = # to fill

    # Number of residues
    n_res = ss.shape[1]

    # Compute fractions of each secondary structure type observed in a trajectory
    helix_frac = # to fill
    sheet_frac = # to fill
    coil_frac  = # to fill

    # Residue index
    residues = np.arange(1, n_res + 1)
    df_ss = pd.DataFrame({
        "residue_index": residues,
        "Helix": helix_frac,
        "Sheet": sheet_frac,
        "Coil": coil_frac,
        "system": label
    })

    return df, rmsf, plddt, df_ss

# === Load and analyze both systems ===
## specify location of the trajecory and AF files 
hp36_df, hp36_rmsf, hp36_plddt, hp36_ss  = analyze_system(
    traj_file="", #xtc file
    top_file="" , #pdb file
    ref_file="" , #AF pdb file
    label="HP36 (folded)"
)

p53_df, p53_rmsf, p53_plddt, p_53_ss  = analyze_system(
    traj_file="", #xtc file
    top_file="",  #pdb file
    ref_file="",  #AF pdb file
    label="p53 TAD (disordered)"
)
df = pd.concat([hp36_df, p53_df])
df_ss=pd.concat([hp36_ss, p_53_ss])
# === Plotting ===
fig, axes = plt.subplots(2, 3, figsize=(12, 7.5), sharex=False)

# RMSD
sns.lineplot(
    data=df,
    x="time_ns",
    y="RMSD_nm",
    hue="system",
    ax=axes[0,0],
    legend=True,
)
axes[0,0].set_title("RMSD")
axes[0,0].set_ylabel("RMSD (nm)")
axes[0,0].set_xlabel("time (ns)")

# Radius of gyration
sns.lineplot(
    data=df,
    x="time_ns",
    y="Rg_nm",
    hue="system",
    ax=axes[0,2],
    legend=False
)
axes[0,2].set_title("Radius of Gyration")
axes[0,2].set_ylabel("Rg (nm)")
axes[0,2].set_xlabel("time (ns)")

# RMSF (per residue, separate plot style)
axes[0,1].plot(hp36_rmsf, label="HP36 (folded)")
axes[0,1].plot(p53_rmsf, label="p53 TAD (disordered)")
axes[0,1].set_title("RMSF (Backbone)")
axes[0,1].set_xlabel("Aminon acid index")
axes[0,1].set_ylabel("RMSF (nm)")

# pLDDt (per residue, separate plot style)
ax2 = axes[0,1].twinx()
color1 = "tab:blue"
color2 = "tab:orange"
ax2.plot(hp36_plddt, color=color1, linestyle="--", label="pLDDT (AlphaFold)")
ax2.plot(p53_plddt, color=color2, linestyle="--", label="pLDDT (AlphaFold)")
ax2.set_ylabel("pLDDT", color='red')
ax2.set_ylim(0, 100)
ax2.tick_params(axis="y", labelcolor='red')

# Secondary Structure: Helix
sns.lineplot(
    data=df_ss,
    x="residue_index",
    y="Helix",
    hue="system",
    ax=axes[1,0],
    legend=False
)
axes[1,0].set_title("Helix")
axes[1,0].set_xlabel("Aminon acid index")
axes[1,0].set_ylabel("Fraction of time")

# Secondary Structure: Sheet
sns.lineplot(
    data=df_ss,
    x="residue_index",
    y="Sheet",
    hue="system",
    ax=axes[1,1],
    legend=False
)
axes[1,1].set_title("Sheet")
axes[1,1].set_xlabel("Aminon acid index")
axes[1,1].set_ylabel("Fraction of time")

# Secondary Structure: Coil
sns.lineplot(
    data=df_ss,
    x="residue_index",
    y="Coil",
    hue="system",
    ax=axes[1,2],
    legend=False
)
axes[1,2].set_title("Coil")
axes[1,2].set_xlabel("Aminon acid index")
axes[1,2].set_ylabel("Fraction of time")

plt.tight_layout()
plt.savefig('./analysis_mdtraj.pdf')
plt.show()