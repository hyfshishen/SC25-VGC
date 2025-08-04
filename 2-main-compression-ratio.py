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


def run_qmcpack(error_bound):
    base_cmd = f"einspline_115_69_69_288.f32 -d 7935 69 288 -eb rel {error_bound}"
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


def run_cesm_atm(error_bound):
    cesm_atm_fields = os.listdir(datasets_path + "cesm_atm")
    base_cmd = f" -d 26 1800 3600 -eb rel {error_bound}"
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


def run_miranda(error_bound):
    base_cmd = f"miranda_1024x1024x1024_float32.raw -d 1024 1024 1024 -eb rel {error_bound}"
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


def run_syntruss(error_bound):
    base_cmd = f"synthetic_truss_with_five_defects_1200x1200x1200_float32.raw -d 1200 1200 1200 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/syntruss/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/syntruss/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["syntruss"][0] * dds["syntruss"][1] * dds["syntruss"][2] * dds["syntruss"][3] * dds["syntruss"][4] * 4
    print("SynTruss compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_hcci(error_bound):
    base_cmd = f"hcci_oh_560x560x560_float32.raw -d 560 560 560 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/hcci/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/hcci/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["hcci"][0] * dds["hcci"][1] * dds["hcci"][2] * dds["hcci"][3] * dds["hcci"][4] * 4
    print("HCCI compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_rtm(error_bound):
    rtm_fields = os.listdir(datasets_path + "rtm")
    base_cmd = f" -d 1008 1008 352 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in rtm_fields:
        if(field.endswith("000")):
            vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/rtm/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in rtm_fields:
        if(field.endswith("000")):
            vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/rtm/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["rtm"][0] * dds["rtm"][1] * dds["rtm"][2] * dds["rtm"][3] * dds["rtm"][4] * 4
    print("RTM compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_magrec(error_bound):
    base_cmd = f"magnetic_reconnection_512x512x512_float32.raw -d 512 512 512 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/magrec/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/magrec/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["magrec"][0] * dds["magrec"][1] * dds["magrec"][2] * dds["magrec"][3] * dds["magrec"][4] * 4
    print("MagRec compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_hacc(error_bound):
    hacc_fields = os.listdir(datasets_path + "hacc")
    base_cmd = f" -t f32 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in hacc_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path[:-1]} -m plain -i {datasets_path}/hacc/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in hacc_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path[:-1]} -m outlier -i {datasets_path}/hacc/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["hacc"][0] * dds["hacc"][1] * dds["hacc"][2] * dds["hacc"][3] * dds["hacc"][4] * 4
    print("HACC compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_scale(error_bound):
    scale_fields = os.listdir(datasets_path + "scale")
    base_cmd = f" -d 98 1200 1200 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in scale_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}2D_float_plain -i {datasets_path}/scale/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in scale_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}2D_float_outlier -i {datasets_path}/scale/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["scale"][0] * dds["scale"][1] * dds["scale"][2] * dds["scale"][3] * dds["scale"][4] * 4
    print("SCALE compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_nyx(error_bound):
    nyx_fields = os.listdir(datasets_path + "nyx")
    base_cmd = f" -d 512 512 512 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in nyx_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/nyx/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in nyx_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/nyx/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["nyx"][0] * dds["nyx"][1] * dds["nyx"][2] * dds["nyx"][3] * dds["nyx"][4] * 4
    print("NYX compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_jetin(error_bound):
    base_cmd = f"jicf_q_1408x1080x1100_float32.raw -d 1100 1080 1408 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/jetin/" + base_cmd
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_size = 0
    for line in result_d.stdout.splitlines():
        if "compression size" in line:
            vgc_d_cmp_size = line.split()[-2]
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/jetin/" + base_cmd
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_size = 0
    for line in result_o.stdout.splitlines():
        if "compression size" in line:
            vgc_o_cmp_size = line.split()[-2]
    vgc_ori_size = dds["jetin"][0] * dds["jetin"][1] * dds["jetin"][2] * dds["jetin"][3] * dds["jetin"][4] * 4
    print("JetIn compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_s3d():
    s3d_fields = os.listdir(datasets_path + "s3d")
    base_cmd = f" -d 5500 500 500 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in s3d_fields:
        if(field.endswith(".d64")):
            vgc_d_cmd = f"{vgc_path}3D_double_plain -i {datasets_path}/s3d/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in s3d_fields:
        if(field.endswith(".d64")):
            vgc_o_cmd = f"{vgc_path}3D_double_outlier -i {datasets_path}/s3d/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = dds["s3d"][0] * dds["s3d"][1] * dds["s3d"][2] * dds["s3d"][3] * dds["s3d"][4] * 4
    print("S3D compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


def run_nwchem(error_bound):
    nwchem_fields = os.listdir(datasets_path + "nwchem")
    base_cmd = f" -t f64 -eb rel {error_bound}"
    vgc_d_cmp_size = 0
    for field in nwchem_fields:
        if(field.endswith(".d64")):
            vgc_d_cmd = f"{vgc_path[:-1]} -m plain -i {datasets_path}/nwchem/{field}" + base_cmd
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression size" in line:
                    vgc_d_cmp_size += int(line.split()[-2])
    vgc_o_cmp_size = 0
    for field in nwchem_fields:
        if(field.endswith(".d64")):
            vgc_o_cmd = f"{vgc_path[:-1]} -m outlier -i {datasets_path}/nwchem/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression size" in line:
                    vgc_o_cmp_size += int(line.split()[-2])
    vgc_ori_size = (dds["nwchem"][0] + dds["nwchem"][1] + dds["nwchem"][2]) * dds["nwchem"][4] * 4
    print("NWChem compression ratio testing completed:")
    print(f"VGC_N: {float(vgc_ori_size)/float(vgc_d_cmp_size)}")
    print(f"VGC_O: {float(vgc_ori_size)/float(vgc_o_cmp_size)}")


error_bound = 1e-4

print(f"Running VGC on QMCPack with error bound {error_bound}...")
run_qmcpack(error_bound)
print()

print(f"Running VGC on CESM_ATM with error bound {error_bound}...")
run_cesm_atm(error_bound)
print()

print(f"Running VGC on Miranda with error bound {error_bound}...")
run_miranda(error_bound)
print()

print(f"Running VGC on SynTruss with error bound {error_bound}...")
run_syntruss(error_bound)
print()

print(f"Running VGC on HCCI with error bound {error_bound}...")
run_hcci(error_bound)
print()

print(f"Running VGC on RTM with error bound {error_bound}...")
run_rtm(error_bound)
print()

print(f"Running VGC on MagRec with error bound {error_bound}...")
run_magrec(error_bound)
print()

print(f"Running VGC on HACC with error bound {error_bound}...")
run_hacc(error_bound)
print()

print(f"Running VGC on SCALE with error bound {error_bound}...")
run_scale(error_bound)
print()

print(f"Running VGC on NYX with error bound {error_bound}...")
run_nyx(error_bound)
print()

print(f"Running VGC on JetIn with error bound {error_bound}...")
run_jetin(error_bound)
print()

print(f"Running VGC on S3D with error bound {error_bound}...")
run_s3d()
print()

print(f"Running VGC on NWChem with error bound {error_bound}...")
run_nwchem(error_bound)
print()

print("All compression ratio tests completed.")