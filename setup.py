from setuptools import setup, find_packages

setup(
    name="staph_agr_typer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "biopython>=1.79",
        "pandas>=1.3.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "staph_agr_typer=staph_agr_typer.cli:main",
        ],
    },
    package_data={
        "staph_agr_typer": ["db/*", "db/references/*"],
    },
)
