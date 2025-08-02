import os, sys

vgc_path = "./vgc/install/bin/vgc_"
datasets_path = "./datasets/"

# dim_3, dim_2, dim_1, number of fields, single or double
dataset_dimensions = {
    "qmcpack": (115*69, 69, 288, 1, 1),
    "cesm_atm": (26, 1800, 3600, 33, 1),
    "miranda": (1024, 1024, 1024, 1, 1),
    "syntruss": (1200, 1200, 1200, 1, 1),
    "hcci": (560, 560, 560, 1, 1),
    "rtm": (1008, 1008, 352, 3, 1),
    "magrec": (512, 512, 512, 1, 1),
    "hacc": (1073726487, 1, 1, 6, 1),
    "scale": (98, 1200, 1200, 12, 1),
    "nyx": (512, 512, 512, 6, 1),
    "jetin": (1100, 1080, 1408, 1, 1),
    "s3d": (5500, 500, 500, 5, 2),
    "nwchem": (102953248, 712996037, 801098891, 3, 2) # 631, ccd, acd
}


def run_qmcpack():
    return ""


def run_cesm_atm():
    return ""


def run_miranda():
    return ""


def run_syntruss():
    return ""


def run_hcci():
    return ""


def run_magrec():
    return ""


def run_rtm():
    return ""


def run_magrec():
    return ""


def run_hacc():
    return ""


def run_scale():
    return ""


def run_nyx():
    return ""

def run_jetin():
    return ""


def run_s3d():
    return ""


def run_nwchem():
    return ""