import os
import pandas as pd
from pathlib import Path
from .utils import run_command, check_dependency

class AgrTyper:
    def __init__(self, db_dir):
        self.db_dir = Path(db_dir)
        self.ref_fasta = self.db_dir / "agr_references.fasta"
        self.blast_db = self.db_dir / "agr_blastdb"
        self.kma_db = self.db_dir / "agr_kma"

    def type_assembly(self, assembly_path, output_dir):
        """Type an assembly using BLASTN."""
        check_dependency("blastn")
        out_file = Path(output_dir) / "blast_results.txt"
        
        # Run BLASTN
        cmd = [
            "blastn",
            "-query", str(assembly_path),
            "-db", str(self.blast_db),
            "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore",
            "-max_target_seqs", "1",
            "-out", str(out_file)
        ]
        run_command(cmd)
        
        # Parse results
        if not out_file.exists() or out_file.stat().st_size == 0:
            return {"agr_group": "Unknown", "confidence": 0.0}
            
        df = pd.read_csv(out_file, sep="\t", header=None, 
                         names=["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"])
        
        # Simple logic: take the best hit
        best_hit = df.sort_values("bitscore", ascending=False).iloc[0]
        agr_group = best_hit["sseqid"] # e.g., "gp1"
        
        return {
            "agr_group": str(agr_group),
            "confidence": float(best_hit["pident"]),
            "contig": str(best_hit["qseqid"]),
            "start": int(best_hit["qstart"]),
            "end": int(best_hit["qend"])
        }

    def type_reads(self, r1, r2, output_dir):
        """Type reads using KMA."""
        check_dependency("kma")
        out_prefix = Path(output_dir) / "kma_results"
        
        cmd = [
            "kma",
            "-ipe", str(r1), str(r2) if r2 else "",
            "-t_db", str(self.kma_db),
            "-o", str(out_prefix),
            "-1t1" # One template per read
        ]
        # Handle single end
        if not r2:
            cmd[2] = "-i"
            cmd[3] = str(r1)
            del cmd[4] # remove r2 arg

        run_command(cmd)
        
        res_file = out_prefix.with_suffix(".res")
        if not res_file.exists():
            return {"agr_group": "Unknown", "confidence": 0.0}
            
        df = pd.read_csv(res_file, sep="\t")
        # KMA res columns: #Template Score Expected Template_length Template_Identity ...
        
        if df.empty:
            return {"agr_group": "Unknown", "confidence": 0.0}
            
        best_hit = df.sort_values("Score", ascending=False).iloc[0]
        return {
            "agr_group": str(best_hit["#Template"].strip()),
            "confidence": float(best_hit["Template_Identity"]),
            "depth": float(best_hit["Depth"])
        }
