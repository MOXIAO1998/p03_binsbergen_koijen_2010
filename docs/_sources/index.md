# Predictive Regressions: A Present-Value Approach

Last updated: {sub-ref}`today` 


## Table of Contents

```{toctree}
:maxdepth: 1
:caption: Notebooks 📖

```



```{toctree}
:maxdepth: 1
:caption: Pipeline Charts 📈
charts.md
```

```{postlist}
:format: "{title}"
```


```{toctree}
:maxdepth: 1
:caption: Pipeline Dataframes 📊
dataframes/PR/replication_data.md
```


```{toctree}
:maxdepth: 1
:caption: Appendix 💡
myst_markdown_demos.md
apidocs/index
```


## Pipeline Specs
| Pipeline Name                   | Predictive Regressions: A Present-Value Approach                       |
|---------------------------------|--------------------------------------------------------|
| Pipeline ID                     | [PR](./index.md)              |
| Lead Pipeline Developer         | Moxiao Li & Yilun Cai             |
| Contributors                    | Moxiao Li & Yilun Cai           |
| Git Repo URL                    |                         |
| Pipeline Web Page               | <a href="file:///Users/moxiaoli/Desktop/Uchicago/2025 - 2026/Full-Stack Finance/p03_binsbergen_koijen_2010/docs/index.html">Pipeline Web Page      |
| Date of Last Code Update        | 2026-03-16 12:40:39           |
| OS Compatibility                |  |
| Linked Dataframes               |  [PR:replication_data](./dataframes/PR/replication_data.md)<br>  |




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

### 1. Install LaTeX

You must install a LaTeX distribution such as **TeX Live** or **MacTeX**.

Mac:
https://tug.org/mactex/

Windows:
https://tug.org/texlive/windows.html

---

### 2. Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate