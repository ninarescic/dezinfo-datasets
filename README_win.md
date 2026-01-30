# dezinfo-datasets — Windows version

This repository provides **access, inspection, and documentation** of DezInfo datasets for **Windows users** via **WSL (Ubuntu)**.

⚠️ **Important:**  
This is the **Windows + WSL implementation** of the project.  
A **native Linux version** is maintained separately.

Datasets are stored on a remote server and are **not included** in this repository.

---

## Purpose

This project:
- connects to a remote dataset server
- loads and validates dataset structure
- computes basic and full-dataset statistics
- documents each dataset in Jupyter notebooks

It supports reproducible dataset access for the DezInfo project.

---

## Repository structure

```
dezinfo-datasets/
│
├─ src/
│  ├─ core/                 # shared configuration
│  └─ datasets/
│     └─ social_media/
│        └─ higgs-twitter/
│           ├─ pull.py
│           └─ reports/
│
├─ notebooks/
│  └─ social_media/
│     └─ higgs_twitter.ipynb
│
├─ requirements.txt
├─ .env
└─ README_win.md
```

---

## Supported datasets

### Social media
- Higgs Twitter  
- Twitter7  
- Kwak10twitter  
- Bluesky  

### Citation networks
- openalexCG  

---

## Requirements (Windows)

- Windows 10/11  
- **WSL2 (Ubuntu)**  
- PyCharm with **WSL Python interpreter**  
- SSH access to the dataset server  
- Python ≥ 3.10 (inside WSL)

---

## Configuration

Create a `.env` file in the project root:

```ini
DATA_ROOT=/home/<your_wsl_user>/dezinfo_data
```

Example:

```ini
DATA_ROOT=/home/rescic/dezinfo_data
```

---

## Connecting to the dataset server (required after every restart)

Datasets are mounted using `sshfs`.  
This must be done **after every reboot or WSL shutdown**.

In WSL terminal:

```bash
mkdir -p ~/dezinfo_data
sshfs nrescic@ndw-workhorse-2.adui.cs.cas.cz:/mnt/DATA/Dezinfo-Social_nets ~/dezinfo_data
```

Verify:

```bash
ls ~/dezinfo_data
```

You should see dataset folders (e.g. `higgs-twitter`).

---

## Installing dependencies

Inside WSL:

```bash
pip install -r requirements.txt
```

---

## Running a dataset script

Example:

```bash
python src/datasets/social_media/higgs-twitter/pull.py
```

This will:
- print the first rows of each file
- validate file structure
- write a report file to `reports/`

---

## Using notebooks

Notebooks are located in:

```
notebooks/
```

Each notebook:
- documents one dataset
- displays table heads
- computes full-dataset statistics using streaming
- performs structural analysis (e.g. SCC samples)

Run notebooks using the **WSL interpreter**.

---

## Design notes

- Dataset paths are configured via `DATA_ROOT`
- No usernames or machine-specific paths are hardcoded
- Large files are processed via streaming
- Scripts are for automation
- Notebooks are for documentation and analysis

---

## Linux version

This repository is the **Windows-specific version**.  
A **native Linux implementation** is maintained separately.

---

## License / data usage

This repository contains only code.  
Datasets remain on the server and are subject to their original licenses.

---

## Contact

Project: **DezInfo**  
Maintainer (Windows version): *your name here*
