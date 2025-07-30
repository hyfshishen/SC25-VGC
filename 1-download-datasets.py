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


# for qmcpack
os.system("tar -xvzf SDRBENCH-QMCPack.tar.gz")
os.system("mv dataset qmcpack")
os.chdir("qmcpack")
os.system("mv 115x69x69x288/* ./ && mv 288x115x69x69/* ./ && rm -rf 115x69x69x288 288x115x69x69")
os.chdir("..")
os.system("rm SDRBENCH-QMCPack.tar.gz")

# for cesm_atm
os.system("tar -xvzf SDRBENCH-CESM-ATM-26x1800x3600.tar.gz")
os.system("mv SDRBENCH-CESM-ATM-26x1800x3600 cesm_atm")
os.system("rm SDRBENCH-CESM-ATM-26x1800x3600.tar.gz")

# for miranda
os.system("mkdir miranda")
os.system("mv miranda_1024x1024x1024_float32.raw miranda/")

# for syntruss
os.system("mkdir syntruss")
os.system("mv synthetic_truss_with_five_defects_1200x1200x1200_float32.raw syntruss/")

# for hcci
os.system("mkdir hcci")
os.system("mv hcci_oh_560x560x560_float32.raw hcci/")

# for magrec
os.system("mkdir magrec")
os.system("mv magnetic_reconnection_512x512x512_float32.raw magrec/")

# for hacc
os.system("tar -xvzf EXASKY-HACC-data-big-size.tar.gz")
os.system("mv 1billionparticles_onesnapshot hacc")
os.system("rm EXASKY-HACC-data-big-size.tar.gz")

# for scale
os.system("tar -xvzf SDRBENCH-SCALE-98x1200x1200.tar.gz")
os.system("mv SDRBENCH-SCALE_98x1200x1200 scale")
os.system("rm SDRBENCH-SCALE-98x1200x1200.tar.gz")

# for nyx
os.system("tar -xvzf SDRBENCH-EXASKY-NYX-512x512x512.tar.gz")
os.system("mv SDRBENCH-EXASKY-NYX-512x512x512 nyx")
os.system("rm SDRBENCH-EXASKY-NYX-512x512x512.tar.gz")

# for jetin
os.system("mkdir jetin")
os.system("mv jicf_q_1408x1080x1100_float32.raw jetin/")

# for s3d
os.system("tar -xvzf SDRBENCH-S3D.tar.gz")
os.system("mv SDRBENCH-S3D s3d")
os.system("rm SDRBENCH-S3D.tar.gz")

# for nwchem
os.system("tar -xvzf SDRBENCH-NWChem-dataset.tar.gz")
os.system("rm ./SDRBENCH-NWChem-dataset/readbin.cpp")
os.system("mv SDRBENCH-NWChem-dataset nwchem")
os.system("rm SDRBENCH-NWChem-dataset.tar.gz")


os.chdir("..")
os.system("Done downloading datasets.")