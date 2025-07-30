import os, sys


download_links = {
    "qmcpack": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/QMCPack/SDRBENCH-QMCPack.tar.gz",
    "cesm_atm": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/CESM-ATM/SDRBENCH-CESM-ATM-26x1800x3600.tar.gz",
    "miranda": "http://klacansky.com/open-scivis-datasets/miranda/miranda_1024x1024x1024_float32.raw",
    "syntruss": "http://klacansky.com/open-scivis-datasets/synthetic_truss_with_five_defects/synthetic_truss_with_five_defects_1200x1200x1200_float32.raw",
    "hcci": "http://klacansky.com/open-scivis-datasets/hcci_oh/hcci_oh_560x560x560_float32.raw",
    "magrec": "http://klacansky.com/open-scivis-datasets/magnetic_reconnection/magnetic_reconnection_512x512x512_float32.raw",
    "hacc": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/EXASKY/HACC/EXASKY-HACC-data-big-size.tar.gz",
    "scale": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/SCALE_LETKF/SDRBENCH-SCALE-98x1200x1200.tar.gz",
    "nyx": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/EXASKY/NYX/SDRBENCH-EXASKY-NYX-512x512x512.tar.gz",
    "jetin": "http://klacansky.com/open-scivis-datasets/jicf_q/jicf_q_1408x1080x1100_float32.raw",
    "s3d": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/S3D/SDRBENCH-S3D.tar.gz",
    "nwchem": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/NWChem/SDRBENCH-NWChem-dataset.tar.gz"
}


os.system("mkdir datasets")
os.chdir("datasets")
for dataset, link in download_links.items():
    print(f"Downloading {dataset} dataset...")
    if link.endswith(".tar.gz"):
        os.system(f"wget {link}")
    elif link.endswith(".raw"):
        os.system(f"wget {link}")
    else:
        print(f"Unknown file type for {dataset}, skipping download.")
