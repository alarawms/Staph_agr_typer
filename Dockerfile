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

# Install the package
RUN pip install .

# Build databases (assuming references are included in the image)
# We need to run the conversion and indexing during build or entrypoint?
# Better to do it during build if possible, but we need the references.
# The references are in staph_agr_typer/db/references (copied in COPY .)

# Convert references
RUN python3 staph_agr_typer/convert_refs.py

# Build DBs
RUN staph_agr_typer build-db

ENTRYPOINT ["staph_agr_typer"]
CMD ["--help"]
