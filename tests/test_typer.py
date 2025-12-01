import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
from staph_agr_typer.typer import AgrTyper

class TestAgrTyper(unittest.TestCase):
    def setUp(self):
        self.typer = AgrTyper("dummy_db")

    @patch("staph_agr_typer.typer.run_command")
    @patch("staph_agr_typer.typer.check_dependency")
    @patch("pandas.read_csv")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.stat")
    def test_type_assembly_success(self, mock_stat, mock_exists, mock_read_csv, mock_check, mock_run):
        # Setup mocks
        mock_exists.return_value = True
        mock_stat.return_value.st_size = 100
        
        # Mock BLAST output
        mock_df = pd.DataFrame({
            "qseqid": ["contig1"],
            "sseqid": ["gp1"],
            "pident": [99.5],
            "length": [1000],
            "mismatch": [0],
            "gapopen": [0],
            "qstart": [1],
            "qend": [1000],
            "sstart": [1],
            "send": [1000],
            "evalue": [0.0],
            "bitscore": [2000]
        })
        mock_read_csv.return_value = mock_df

        # Run
        result = self.typer.type_assembly("assembly.fasta", "out_dir")
        
        # Verify
        self.assertEqual(result["agr_group"], "gp1")
        self.assertEqual(result["confidence"], 99.5)
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[0], "blastn")

    @patch("staph_agr_typer.typer.run_command")
    @patch("staph_agr_typer.typer.check_dependency")
    @patch("pandas.read_csv")
    @patch("pathlib.Path.exists")
    def test_type_reads_success(self, mock_exists, mock_read_csv, mock_check, mock_run):
        # Setup mocks
        mock_exists.return_value = True
        
        # Mock KMA output
        mock_df = pd.DataFrame({
            "#Template": ["gp2 "],
            "Score": [1000],
            "Expected": [1000],
            "Template_length": [1000],
            "Template_Identity": [98.0],
            "Template_Coverage": [100.0],
            "Depth": [50.0],
            "q_value": [0.0],
            "p_value": [0.0]
        })
        mock_read_csv.return_value = mock_df

        # Run
        result = self.typer.type_reads("r1.fastq", "r2.fastq", "out_dir")
        
        # Verify
        self.assertEqual(result["agr_group"], "gp2")
        self.assertEqual(result["confidence"], 98.0)
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[0], "kma")

if __name__ == "__main__":
    unittest.main()
