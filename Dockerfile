FROM continuumio/miniconda3

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install bioconda tools
RUN conda config --add channels defaults
RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge
RUN conda install -y \
    blast \
    kma \
    mafft \
    biopython \
    pandas \
    click \
    && conda clean -a

# Copy package code
COPY . /app

# Restructure for package installation (Fixing flat structure)
# We move the source files into a package subdirectory so setuptools can find them
RUN mkdir -p staph_agr_typer_pkg/staph_agr_typer && \
    mv cli.py typer.py utils.py __init__.py convert_refs.py db staph_agr_typer_pkg/staph_agr_typer/ && \
    mv setup.py staph_agr_typer_pkg/ && \
    mv README.md staph_agr_typer_pkg/

WORKDIR /app/staph_agr_typer_pkg

# Generate DB files in source BEFORE install
RUN python3 staph_agr_typer/convert_refs.py

# Build indices manually in source so they get packaged
RUN makeblastdb -in staph_agr_typer/db/agr_references.fasta -dbtype nucl -out staph_agr_typer/db/agr_blastdb
RUN kma index -i staph_agr_typer/db/agr_references.fasta -o staph_agr_typer/db/agr_kma

# Install the package (will include generated DB files)
RUN pip install .

ENTRYPOINT ["staph_agr_typer"]
CMD ["--help"]
