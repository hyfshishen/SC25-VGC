import os, sys
import subprocess

vgc_path = "./vgc/vgc-compression/install/bin/cuSZp_"
datasets_path = "./datasets/"

# dds means: dataset dimensions
# dim_3, dim_2, dim_1, number of fields, single or double
dds = {
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
    base_cmd = "einspline_115_69_69_288.f32 -d 7935 69 288 -eb rel 1e-4"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/qmcpack/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/qmcpack/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["qmcpack"][0] * dds["qmcpack"][1] * dds["qmcpack"][2] * dds["qmcpack"][3] * dds["qmcpack"][4] * 4
    print("QMCPack compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_cesm_atm():
    cesm_atm_fields = os.listdir(datasets_path + "cesm_atm")
    base_cmd = " -d 26 1800 3600 -eb rel 1e-4"
    vgc_d_cmp_size = 0
    for field in cesm_atm_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}2D_float_plain -i {datasets_path}/cesm_atm/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in cesm_atm_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}2D_float_outlier -i {datasets_path}/cesm_atm/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["cesm_atm"][0] * dds["cesm_atm"][1] * dds["cesm_atm"][2] * dds["cesm_atm"][3] * dds["cesm_atm"][4] * 4
    print("CESM_ATM compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_miranda():
    base_cmd = "miranda_1024x1024x1024_float32.raw -d 1024 1024 1024 -eb rel 1e-4"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/miranda/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/miranda/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["miranda"][0] * dds["miranda"][1] * dds["miranda"][2] * dds["miranda"][3] * dds["miranda"][4] * 4
    print("Miranda compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


# def run_syntruss():
#     return ""


# def run_hcci():
#     return ""


# def run_magrec():
#     return ""


# def run_rtm():
#     return ""


# def run_magrec():
#     return ""


# def run_hacc():
#     return ""


# def run_scale():
#     return ""


# def run_nyx():
#     return ""

# def run_jetin():
#     return ""


# def run_s3d():
#     return ""


# def run_nwchem():
#     return ""


# run_qmcpack()
print()
run_cesm_atm()
print()
# run_miranda()
print()