"""Compile all of the YARA rules into a single binary file."""
import os
import subprocess
from typing import Generator

import yara

RULES_DIR = os.path.dirname(os.path.realpath(__file__))  # Directory containing this file.


def _find_yara_files() -> Generator[str, None, None]:
    """Find all .yar[a] files in the rules directory.

    Yields:
        YARA rule filepaths, relative to the rules root directory.
    """
    for root, _, files in os.walk(RULES_DIR):
        for filename in files:
            lower_filename = filename.lower()
            if lower_filename.endswith('.yar') or lower_filename.endswith('.yara'):
                yield os.path.relpath(os.path.join(root, filename), start=RULES_DIR)


def compile_rules(target_path:str, rules_dir: str) -> None:
    """Compile YARA rules into a single binary rules file.

    Args:
        target_path: Where to save the compiled rules file.
    """
    global RULES_DIR
    RULES_DIR = rules_dir
    # Each rule file must be keyed by an identifying "namespace"; in our case the relative path.
    yara_filepaths = {relative_path: os.path.join(RULES_DIR, relative_path)
                      for relative_path in _find_yara_files()}

    # Compile all available YARA rules. Note that external variables are defined but not set;
    # these will be set at runtime by the lambda function during rule matching.
    rules = yara.compile(
        filepaths=yara_filepaths,
        externals={'extension': '', 'filename': '', 'filepath': '', 'filetype': ''})
    rules.save(target_path)

# Function to run the powershell scripts - make sure to have PowerShell installed and paths are configured correctly.
def run_powershell_script(script_path):
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)

if __name__ == "__main__":
    rules_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "rules")
    output_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "output", "compiled_yara_rules.bin"))
    compile_rules(output_path, rules_directory)
   
    # Run the PowerShell scripts
    ps1_dir = os.path.dirname(os.path.realpath(__file__))
    generate_list_script = os.path.join(ps1_dir, "generate_yara_list.ps1")
    extract_desc_script = os.path.join(ps1_dir, "extract_yara_rule_descriptions.ps1")
    run_powershell_script(generate_list_script)
    run_powershell_script(extract_desc_script)

    # Compile YARA rules
    compile_rules(output_path, rules_directory)