import subprocess
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

def check_dependency(name):
    """Check if a tool is available in PATH."""
    if shutil.which(name) is None:
        raise RuntimeError(f"Required tool '{name}' not found in PATH.")

def run_command(cmd, cwd=None):
    """Run a shell command and return output."""
    logger.debug(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(cmd)}")
        logger.error(f"Stderr: {e.stderr}")
        raise RuntimeError(f"Command failed: {e.stderr}")

def make_blast_db(fasta_path, db_path):
    """Create a BLAST database from a FASTA file."""
    check_dependency("makeblastdb")
    cmd = [
        "makeblastdb",
        "-in", str(fasta_path),
        "-dbtype", "nucl",
        "-out", str(db_path)
    ]
    run_command(cmd)

def index_kma_db(fasta_path, db_path):
    """Index a FASTA file for KMA."""
    check_dependency("kma")
    cmd = [
        "kma",
        "index",
        "-i", str(fasta_path),
        "-o", str(db_path)
    ]
    run_command(cmd)
