import click
import json
from pathlib import Path
from .typer import AgrTyper
from .utils import make_blast_db, index_kma_db

@click.group()
def main():
    """Staphylococcus aureus agr typer."""
    pass

@main.command()
@click.option("--fasta", help="Input genome assembly (FASTA)")
@click.option("--fastq-1", help="Input reads R1 (FASTQ)")
@click.option("--fastq-2", help="Input reads R2 (FASTQ)")
@click.option("--db-dir", default=None, help="Path to database directory")
@click.option("--output", "-o", required=True, help="Output directory")
def run(fasta, fastq_1, fastq_2, db_dir, output):
    """Run the typer on assembly or reads."""
    if not db_dir:
        # Default to package db
        db_dir = Path(__file__).parent.parent / "db"
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    typer = AgrTyper(db_dir)
    
    results = {}
    
    if fasta:
        click.echo(f"Typing assembly: {fasta}")
        results = typer.type_assembly(fasta, output_path)
    elif fastq_1:
        click.echo(f"Typing reads: {fastq_1}")
        results = typer.type_reads(fastq_1, fastq_2, output_path)
    else:
        click.echo("Error: Must provide --fasta or --fastq-1")
        return

    # Save results
    with open(output_path / "result.json", "w") as f:
        json.dump(results, f, indent=2)
    
    click.echo(f"Results saved to {output_path}/result.json")
    click.echo(json.dumps(results, indent=2))

@main.command()
@click.option("--db-dir", default=None, help="Path to database directory")
def build_db(db_dir):
    """Build BLAST and KMA databases."""
    if not db_dir:
        db_dir = Path(__file__).parent.parent / "db"
    
    fasta_path = Path(db_dir) / "agr_references.fasta"
    if not fasta_path.exists():
        click.echo("Error: agr_references.fasta not found in db dir.")
        return

    click.echo("Building BLAST database...")
    make_blast_db(fasta_path, Path(db_dir) / "agr_blastdb")
    
    click.echo("Building KMA database...")
    index_kma_db(fasta_path, Path(db_dir) / "agr_kma")
    
    click.echo("Databases built successfully.")

if __name__ == "__main__":
    main()
