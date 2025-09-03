# This script does not download the RTM datasets, however it will validate that their location and size are correct if the dataset is already downloaded
# NOTE: This script executes RAW SHELL COMMANDS on your behalf. Ensure that all commands are appropriate to execute on your system PRIOR to execution
import os
import sys
import pathlib
import subprocess

# Set to TRUE to delete tar files after extraction
remove_files = False

# Each key is a dataset identifier to use in all subsequent dictionaries
# Each value is the URL to download the dataset
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
    "nwchem": "https://g-8d6b0.fd635.8443.data.globus.org/ds131.2/Data-Reduction-Repo/raw-data/NWChem/SDRBENCH-NWChem-dataset.tar.gz",
}
# The expected disk size of the dataset after complete download and extraction as reported by the DU utility in human-readable format
expect_sizes = {
    "qmcpack": "1.2G",
    "cesm_atm": "21G",
    "miranda": "4.0G", # Originally listed as 4.1G
    "syntruss": "6.5G",
    "hcci": "670M",
    "magrec": "512M", # Originally listed as 513M
    "hacc": "24G",
    "scale": "6.4G",
    "nyx": "3.1G",
    "jetin": "6.3G",
    "s3d": "52G",
    "nwchem": "13G",
    "rtm": "4.0G",
}
# For each dataset, make a list of shell instructions to execute that prepare the file
# The final command should remove any files that are not needed long-term, or supply None if no removals are required
recipes = {
    "qmcpack": ["tar -xvzf SDRBENCH-QMCPack.tar.gz",
                "mv dataset qmcpack",
                "cd qmcpack",
                # Note that this command deletes some data, but I do not know if allowing it to optionally persist would affect behaviors of other scripts in the repository
                "mv 115x69x69x288/* ./ && mv 288x115x69x69/* ./ && rm -rf 115x69x69x288 288x115x69x69",
                "cd ..",
                "rm SDRBENCH-QMCPack.tar.gz"
                ],
    "cesm_atm": ["tar -xvzf SDRBENCH-CESM-ATM-26x1800x3600.tar.gz",
                 "mv SDRBENCH-CESM-ATM-26x1800x3600 cesm_atm",
                 "rm SDRBENCH-CESM-ATM-26x1800x3600.tar.gz"
                ],
    "miranda": ["mkdir miranda",
                "mv miranda_1024x1024x1024_float32.raw miranda/",
                None
                ],
    "syntruss": ["mkdir syntruss",
                 "mv synthetic_truss_with_five_defects_1200x1200x1200_float32.raw syntruss/",
                 None
                ],
    "hcci": ["mkdir hcci",
             "mv hcci_oh_560x560x560_float32.raw hcci/",
             None
            ],
    "magrec": ["mkdir magrec",
               "mv magnetic_reconnection_512x512x512_float32.raw magrec/",
               None
              ],
    "hacc": ["tar -xvzf EXASKY-HACC-data-big-size.tar.gz",
             "mv 1billionparticles_onesnapshot hacc",
             "rm EXASKY-HACC-data-big-size.tar.gz",
             ],
    "scale": ["tar -xvzf SDRBENCH-SCALE-98x1200x1200.tar.gz",
              "mv SDRBENCH-SCALE_98x1200x1200 scale",
              "rm SDRBENCH-SCALE-98x1200x1200.tar.gz",
             ],
    "nyx": ["tar -xvzf SDRBENCH-EXASKY-NYX-512x512x512.tar.gz",
            "mv SDRBENCH-EXASKY-NYX-512x512x512 nyx",
            "rm SDRBENCH-EXASKY-NYX-512x512x512.tar.gz",
           ],
    "jetin": ["mkdir jetin",
              "mv jicf_q_1408x1080x1100_float32.raw jetin/",
              None
             ],
    "s3d": ["tar -xvzf SDRBENCH-S3D.tar.gz",
            "mv SDRBENCH-S3D s3d",
            "rm SDRBENCH-S3D.tar.gz",
           ],
    "nwchem": ["tar -xvzf SDRBENCH-NWChem-dataset.tar.gz",
               "mv SDRBENCH-NWChem-dataset nwchem",
               "rm nwchem/readbin.cpp SDRBENCH-NWChem-dataset.tar.gz",
              ],
}

# Begin the dataset creation process
pathlib.Path('datasets').mkdir(exist_ok=True)
os.chdir("datasets")

# Special check for RTM
try:
    out = subprocess.check_output(f'du -sh ./rtm}/'.split()).decode('utf-8')
    section_out = out.lstrip().split('\t',1)[0]
    if section_out == expect_sizes['rtm']:
        print(f"Found expected {expect_sizes['rtm']} data for rtm.")
    else:
        print(f"Dataset rtm had size: {section_out} (Expected: {expect_sizes['rtm']})")
        print(out.rstrip())
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Unable to run du command, directory for rtm probably does not exist")

# Run all other dataset processes
for dataset, link in download_links.items():
    # Attempt to validate that the dataset is already downloaded and fully extracted / ready for use
    try:
        out = subprocess.check_output(f'du -sh ./{dataset}/'.split()).decode('utf-8')
        section_out = out.lstrip().split('\t',1)[0]
        if section_out == expect_sizes[dataset]:
            print(f"Found expected {expect_sizes[dataset]} data for {dataset}. Continuing.")
            continue
        else:
            print(f"Dataset {dataset} had size: {section_out} (Expected: {expect_sizes[dataset]})")
            print(out.rstrip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Unable to run du command, directory for {dataset} probably does not exist")
        pass

    # Safely adjust downloads or skip them if it seems reasonable
    print(f"Downloading {dataset} dataset...")
    expect_download = pathlib.Path(pathlib.Path(link).name)
    if expect_download.exists():
        print(f"Download for {dataset} already exists -- if this download is incomplete, delete {expect_download} before re-running this script")
        continue
    if link.endswith(".tar.gz"):
        os.system(f"wget {link}")
    elif link.endswith(".raw"):
        os.system(f"wget {link}")
    else:
        print(f"Unknown file type for {dataset}, skipping download.")

    # Follow all instructions given to prepare this dataset for usage. Final instruction is OPTIONAL for removing files based on the variable "remove_files" at the top of this file
    my_recipe = recipes[dataset]
    for inst in my_recipe[:-1]:
        print(f"{dataset} preparation instruction:",inst)
        os.system(inst)
    if remove_files and my_recipe[-1] is not None:
        print(f"{dataset} cleanup instruction:",inst)
        os.system(inst)
