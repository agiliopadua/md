## Trajectory Analysis

The following Python script analyzes molecular dynamics trajectories using the **MDTraj** library.  
The goal is to compare the behavior of two proteins:

- **HP36** – a small, well-folded protein
- **p53 TAD** – an intrinsically disordered protein

The analysis extracts several structural and dynamical quantities from the trajectories and visualizes them in a single figure.

---

## Quantities Analyzed

### 1. Root Mean Square Deviation (RMSD)

**RMSD** measures how much the protein structure deviates from a reference structure over time.

It is computed using the **Cα atoms** of the protein backbone.

$$
\rm {RMSD}(t) = \sqrt{\frac{1}{N}\sum_{i=1}^{N} (r_i(t) - r_i^{ref})^2}
$$

RMSD provides information about **structural stability during the simulation**.

**Questions for students**

- Which protein shows a **more stable RMSD** over time?
- Does the RMSD of either protein **increase significantly during the simulation**?
- What might large RMSD fluctuations indicate about the protein's structural stability?

---

### 2. Root Mean Square Fluctuation (RMSF)

**RMSF** measures the flexibility of each residue during the trajectory.

$$
\rm{RMSF}(i) = \sqrt{\langle (r_i - \langle r_i \rangle)^2 \rangle}
$$

It is computed for **backbone atoms** and plotted as a function of residue index.

**Questions for students**

- Which protein shows **larger residue fluctuations**?
- Are there specific regions with particularly **high flexibility**?
- How do the fluctuation patterns differ between the two proteins?

---

### 3. Radius of Gyration (Rg)

The **radius of gyration** measures the overall compactness of the protein.

$$
R_g = \sqrt{\frac{\sum_i m_i (r_i - r_{COM})^2}{\sum_i m_i}}
$$

This quantity describes how **compact or expanded** the protein structure is during the simulation.

**Questions for students**

- Which protein appears **more compact** during the simulation?
- Does the radius of gyration remain stable or fluctuate significantly?
- What might changes in Rg indicate about protein folding or structural rearrangements?

---

### 4. AlphaFold Confidence Score (pLDDT)

AlphaFold assigns a **per-residue confidence score (pLDDT)** that estimates the reliability of the predicted structure.

The pLDDT values are stored in the **B-factor column** of the AlphaFold PDB file and are extracted for **Cα atoms**.

Typical interpretation:

| pLDDT | Confidence |
|------|------|
| 90–100 | very high confidence |
| 70–90 | good confidence |
| 50–70 | low confidence |
| <50 | likely disordered |

The script overlays **pLDDT values with RMSF** to compare AlphaFold predictions with molecular dynamics flexibility.

**Questions for students**

- Do regions with **low pLDDT** correspond to regions with **high RMSF**?
- Are there regions where AlphaFold predicts **high confidence but MD shows strong fluctuations**?
- What might this tell us about the **limitations of structure prediction methods**?

---

### 5. Secondary Structure

Secondary structure is computed using the **DSSP algorithm** implemented in MDTraj.

Each residue is classified as:

| Symbol | Structure |
|------|------|
| H | Helix |
| E | β-sheet |
| C | Coil / disordered |

For each residue, the script calculates the **fraction of simulation time spent in each structure type**.

$$
\rm{Fraction} = \frac{\text{Number of frames with structure}}{\text{Total frames}}
$$

**Questions for students**

- Which protein shows **more stable secondary structure elements**?
- Are helices or sheets **persistent during the simulation**, or do they fluctuate?
- Does one protein appear **mostly coil-like**?
- How does the observed secondary structure compare with the **AlphaFold predicted structure**?

---

## Visualization

The script produces a figure with **six panels**.

### Structural Dynamics

1. **RMSD vs time**
2. **RMSF per residue**
3. **Radius of gyration vs time**

### Secondary Structure Propensity

4. **Helix fraction per residue**
5. **Sheet fraction per residue**
6. **Coil fraction per residue**

The **pLDDT profile from AlphaFold** is overlaid with the RMSF plot to help compare **predicted structural confidence** with **observed flexibility in the MD simulation**.

---

## Output

The script generates a figure:

```
analysis_mdtraj.pdf
```

Use this figure to compare the **structural stability, flexibility, compactness, and secondary structure behavior** of the two proteins.