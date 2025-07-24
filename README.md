# BinaryAlert YARA Rule Management Documentation

> **Note:** This repository is a refined version of the rules shown in the public repository: [airbnb/binaryalert rules](https://github.com/airbnb/binaryalert/tree/master/rules). The rules in this binary file are derived from that source, with improvements and curation for enhanced detection.

## Overview
This project provides a framework for gathering, organizing, and compiling YARA rules for use in malware detection and analysis workflows. It includes scripts for rule discovery, metadata extraction, and rule compilation, supporting both Windows and cross-platform environments.

---

## Folder Structure
```
binaryalert/
├── LICENSE
├── README.md
├── requirements.txt
├── rules/
│   ├── generate_yara_list.ps1
│   ├── extract_yara_rule_descriptions.ps1
│   ├── compile_rules.py
│   ├── yara_files_list.json
│   ├── yara_rule_descriptions.json
│   ├── github.com/
│   │   └── ... (external YARA rules)
│   ├── public/
│   │   └── ... (public YARA rules)
│   └── ... (other subfolders and .yar/.yara files)
└── ...
```

---

## Pre-requisites
- **YARA**: Version 4.0.0 (for both CLI and Python bindings)
- **Python**: 3.7 or higher
- **PowerShell**: Required for running `.ps1` scripts (Windows: built-in, macOS/Linux: install PowerShell Core)
- **pip**: For Python package management
- **Microsoft Visual C++ Build Tools**: (Windows, for building `yara-python`)

---

## Procedure

### 1. Rule Gathering Technique
- YARA rules are collected from various sources and organized under the `rules/` directory.
- Subfolders (e.g., `github.com/`, `public/`) help categorize rules by source or type.
- All `.yar` and `.yara` files in `rules/` and its subdirectories are considered for compilation and metadata extraction.

### 2. Rule Creation Technique
- New rules can be added by placing `.yar` or `.yara` files in the appropriate subfolder under `rules/`.
- Each rule should follow YARA syntax and include a `meta` section with a `description` field for documentation and extraction.
- Example rule structure:
  ```yara
  rule ExampleRule {
    meta:
      description = "Detects Example Malware"
    strings:
      $a = "malicious_string"
    condition:
      $a
  }
  ```

### 3. Scripts and Their Usage

#### a. `generate_yara_list.ps1`
- **Purpose:** Recursively lists all `.yar` and `.yara` files under `rules/`, outputs a numerically ordered JSON file (`yara_files_list.json`).
- **Usage:**
  ```powershell
  pwsh ./rules/generate_yara_list.ps1
  ```

#### b. `extract_yara_rule_descriptions.ps1`
- **Purpose:** Extracts rule names and their one-line descriptions from the `meta` section of each rule in all `.yar`/`.yara` files, outputs to `yara_rule_descriptions.json`.
- **Usage:**
  ```powershell
  pwsh ./rules/extract_yara_rule_descriptions.ps1
  ```

#### c. `compile_rules.py`
- **Purpose:** Compiles all YARA rules in the `rules/` directory into a single binary file (`compiled_yara_rules.bin`) for efficient loading in applications (e.g., AWS Lambda).
- **Usage:**
  ```bash
  python ./rules/compile_rules.py
  ```
- **Note:** This script can be extended to run the above PowerShell scripts before compilation for up-to-date metadata.

---

## Environment Setup

### 1. Create and Activate a Python Virtual Environment
```bash
python -m venv yara-env
# On Windows:
yara-env\Scripts\activate
# On macOS/Linux:
source yara-env/bin/activate
```

### 2. Install YARA and Python Bindings (Version 4.0.0)
```bash
pip install yara-python==4.0.0
```

### 3. (Optional) Gather Rules from Upstream with `clone_rules.py`
You can optionally gather or update rules from upstream sources using the provided Python script:
```bash
python ./rules/clone_rules.py
```
This script will fetch and organize rules from the original public repository or other sources as configured.


### 5. Run the Compilation Script
```bash
python ./rules/compile_rules.py
```

---

## Example Workflow
1. **Add or update YARA rules** in the `rules/` directory.
2. **(Optional)** Generate the rule list and descriptions using the Python scripts as described above.
3. **Or, run the PowerShell scripts** to update the file list and rule descriptions:
   ```powershell
   pwsh ./rules/generate_yara_list.ps1
   pwsh ./rules/extract_yara_rule_descriptions.ps1
   ```
4. **Compile the rules** into a binary file:
   ```bash
   python ./rules/compile_rules.py
   ```
5. **Deploy** the compiled rules and metadata files as needed (e.g., to AWS Lambda).

---

## Notes
- Rule sources are denoted in `yara_files_list.json` and `yara_rule_descriptions.json`.
- Ensure all rules are compatible with YARA 4.0.0.
- If using on macOS/Linux, install PowerShell Core (`brew install --cask powershell` on macOS).
- For Windows, ensure Microsoft Visual C++ Build Tools are installed if building `yara-python` from source.
- The JSON outputs (`yara_files_list.json`, `yara_rule_descriptions.json`) are regenerated each time the scripts are run.

---

## References
- [YARA Documentation](https://yara.readthedocs.io/en/stable/)
- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)
- [Python YARA Bindings](https://github.com/VirusTotal/yara-python)
