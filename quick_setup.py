import os
import sys
import subprocess

NOTEBOOK = "prediction.ipynb"
VENV_DIR = ".venv"

def run_command(command: list, check=True, stdout=subprocess.DEVNULL, stderr=None):
    """
    Function for running command in a subprocess.
    """
    subprocess.run(command, check=check, stdout=stdout, stderr=stderr)

def create_venv():
    """
    Create a new virtual environment if it doesn't exist.
    """
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment ...")
        run_command([sys.executable, "-m", "venv", VENV_DIR])
        print(f"Virtual environment created at \"{VENV_DIR}\".")
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """
    Installs requirements and development requirements (jupyter) from requirements files.
    """
    print("Installing dependencies ...")

    if os.name == "nt":
        pip_path = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(VENV_DIR, "bin", "pip")

    run_command([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencies installed.")
    print("Installing development dependencies ...")
    run_command([pip_path, "install", "-r", "requirements-dev.txt"])
    print("Development dependencies installed.")

def execute_notebook():
    """
    Execute the notebook so it has the results.
    """
    print(f"Executing notebook {NOTEBOOK} ...")

    if os.name == "nt":
        python_path = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_path = os.path.join(VENV_DIR, "bin", "python")

    # The notebook will save figures to the "figs" folder.
    os.mkdir("figs")
    run_command([python_path, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", NOTEBOOK, "--output", NOTEBOOK])
    print(f"Notebook executed and saved as {NOTEBOOK}")

def open_jupyter_lab():
    """
    Open the notebook in Jupyter Lab.
    """
    print("Launching JupyterLab ...")

    if os.name == "nt":
        python_path = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        python_path = os.path.join(VENV_DIR, "bin", "python")

    try:
        run_command([python_path, "-m", "jupyter", "lab", NOTEBOOK])
    except KeyboardInterrupt:
        print("Exiting ...")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    execute_notebook()
    open_jupyter_lab()