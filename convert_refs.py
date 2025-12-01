from Bio import SeqIO
import os
import sys

REQUIRED_GENES = {"agrA", "agrB", "agrC", "agrD"}

def validate_record(record):
    """Check if record contains all required agr genes."""
    found_genes = set()
    for feature in record.features:
        if feature.type == "gene" or feature.type == "CDS":
            if "gene" in feature.qualifiers:
                gene_name = feature.qualifiers["gene"][0]
                if gene_name in REQUIRED_GENES:
                    found_genes.add(gene_name)
    
    missing = REQUIRED_GENES - found_genes
    if missing:
        print(f"WARNING: {record.id} is missing genes: {missing}")
        return False
    return True

def convert_gbk_to_fasta(db_dir):
    ref_dir = os.path.join(db_dir, "references")
    fasta_out = os.path.join(db_dir, "agr_references.fasta")
    
    records = []
    if not os.path.exists(ref_dir):
        print(f"Error: Reference directory {ref_dir} not found.")
        sys.exit(1)

    for filename in os.listdir(ref_dir):
        if filename.endswith(".gbk"):
            filepath = os.path.join(ref_dir, filename)
            try:
                # Parse GenBank
                for record in SeqIO.parse(filepath, "genbank"):
                    # Extract group from filename (e.g. gp1-operon_ref.gbk -> gp1)
                    group = filename.split("-")[0]
                    record.id = group
                    record.description = f"Reference agr operon for {group} (Validated)"
                    
                    if validate_record(record):
                        records.append(record)
                        print(f"Validated and added {group} from {filename}")
                    else:
                        print(f"Skipping {filename} due to missing genes.")
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
    
    if not records:
        print("No valid records found!")
        sys.exit(1)

    SeqIO.write(records, fasta_out, "fasta")
    print(f"Created {fasta_out} with {len(records)} sequences.")

if __name__ == "__main__":
    # Adjust path if running from root or package dir
    db_path = "staph_agr_typer/db"
    if not os.path.exists(db_path):
        # Try relative to script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "..", "db")
        
    convert_gbk_to_fasta(db_path)
