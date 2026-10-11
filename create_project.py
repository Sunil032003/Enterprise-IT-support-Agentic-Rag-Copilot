from pathlib import Path
import os

root=Path(".")

folders=[
    "app/api",
    "app/core",
    "app/rag",
    "app/services",
    "data",
    "templates",
    "static",
    "uploads",
    "tests"
]

files=[
    "app/main.py",
    "ingest_sample_kb.py",
    "run.py",
    ".env"
]

for folder in folders:
    (root/folder).mkdir(parents=True, exist_ok=True )                

for file in files:
    (root/file).touch()