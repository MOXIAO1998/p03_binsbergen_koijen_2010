# Dividend Growth Predictability Replication

## About this project

This repository contains our final replication project for **FINM 32900: Full-Stack Finance** at the University of Chicago.

We replicate key empirical results from:

> van Binsbergen, Jules H., and Ralph S. J. Koijen.  
> *Predictive Regressions: A Present-Value Approach*.  
> Journal of Finance (2010).

The project focuses on replicating the **dividend growth predictability results** in the paper and comparing the replicated statistics with the values reported in the original publication.

Using an end-to-end reproducible analytical pipeline, we reproduce:

- **Summary statistics of dividend growth**
- **Predictive regression specifications**
- **Key tables used to validate the replication**

We also extend the data sample through **2024** to examine how the results change in more recent periods.

The project is implemented using a **fully reproducible pipeline** with:

- Python
- PyDoit task automation
- Jupyter notebooks
- LaTeX report generation

---

## Replication objects

Our replication produces the following outputs:

- **Table 1** – Summary statistics of dividend growth
- **Specification tables for predictive regressions**
- **Side-by-side comparisons between replicated and paper results**

All tables are generated automatically from the pipeline and compiled into a LaTeX report.

---

## Pipeline overview

The pipeline executes the following steps:

1. Pull raw data from CRSP
2. Clean and organize the data into tidy datasets
3. Construct dividend growth series
4. Compute summary statistics and regression inputs
5. Generate tables and figures
6. Convert notebooks into LaTeX
7. Compile the final PDF report

The entire pipeline can be executed automatically using **PyDoit**.

---

## Quick start

### 1. Set up Environment

```bash
pip install -r requirements.txt
```
if you did not install pip, please run:
```bash
conda install pip
```


---

### 2. dodo.py

```bash
doit
```

### 3. report 

In reports, there are two tex files. These are latex files of report of the project you can review them and generate PDF files by them.