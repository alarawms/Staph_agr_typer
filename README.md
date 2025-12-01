# Staph Agr Typer

A robust, modular open-source tool for *Staphylococcus aureus* *agr* locus typing and variant assessment. 
This tool supports typing from both **genome assemblies** (FASTA) and **raw sequencing reads** (FASTQ), removing the need for proprietary dependencies like USEARCH.

## Features
- **Assembly Typing**: Uses BLAST+ to identify *agr* groups (I-IV).
- **Read Typing**: Uses KMA for direct typing from paired or single-end reads.
- **Dockerized**: Easy deployment with Docker.
- **Validated Database**: Reference sequences validated for *agrA-D* genes.

## Installation

### Docker (Recommended)
```bash
docker build -t staph_agr_typer .
```

### Local (Python)
Requires `blastn`, `kma`, and `mafft` to be in your PATH.
```bash
pip install .
staph_agr_typer build-db
```

## Usage

### Type an Assembly
```bash
staph_agr_typer run --fasta genome.fasta -o results/
```

### Type Reads
```bash
staph_agr_typer run --fastq-1 R1.fastq.gz --fastq-2 R2.fastq.gz -o results/
```

## Attribution
This tool is inspired by and builds upon the concepts from [AgrVATE](https://github.com/VishnuRaghuram94/AgrVATE). 
We acknowledge the original authors for their work on *agr* typing methodology and reference curation.

If you use this tool, please also consider citing the original AgrVATE paper:
> Raghuram V, et al. Species-Wide Phylogenomics of the Staphylococcus aureus Agr Operon... Microbiol Spectr. 2022.
