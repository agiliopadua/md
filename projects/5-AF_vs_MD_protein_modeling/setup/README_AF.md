## Running an AlphaFold Prediction

Follow these steps to generate a protein structure prediction using the AlphaFold server.

### 1. Open the AlphaFold Server

Navigate to the AlphaFold web interface:

https://alphafoldserver.com/welcome

### 2. Log in

Sign in using your account credentials to access the prediction interface.

### 3. Provide the Protein Sequence

In each system folder of this repository, you will find a **FASTA file** containing the protein sequence.

1. Open the FASTA file.
2. Copy the entire sequence (including the header line starting with `>`).
3. Paste it into the sequence input field on the AlphaFold server.

### 4. Submit the Job

Submit the prediction job using the default settings.

The server will begin computing the structure prediction.  
Depending on the system load, the calculation may take several minutes.

### 5. Inspect the Results

Once the job has finished:

1. Open the generated results folder.
2. Examine the predicted structure.
3. Pay attention to the **confidence scores (pLDDT)** shown in the visualization.

These results will be used as the **starting structures for the molecular dynamics simulations** in this tutorial.


### 6. Convert the AlphaFold Model to PDB Format

The AlphaFold server provides the predicted structures in **mmCIF format (`.cif`)**.  
However, **GROMACS** requires structures in **PDB format (`.pdb`)**.

To convert the file:

1. Download the **best model** from the AlphaFold results:
   
   ```
   model_0.cif
   ```

2. Open the online conversion tool:

   https://project-gemmi.github.io/wasm/convert/cif2pdb.html

3. Upload the file `model_0.cif`.

4. Convert the structure to **PDB format**.

5. Download the converted file and rename it following the tutorial naming convention:

   ```
   fold_<system_name>_model_0.pdb
   ```

Example:

```
fold_hp36_model_0.pdb
```

or

```
fold_p53_tad_model_0.pdb
```

Place this file inside the corresponding system folder. This PDB structure will be used as the **starting configuration for the molecular dynamics simulation in GROMACS**.