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
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/qmcpack/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_cesm_atm(error_bound):
    cesm_atm_fields = os.listdir(datasets_path + "cesm_atm")[-5:] # evaluating total 33 takes too much time, use the last 5 for simplicity to save reviewer's time
    field_count = len([f for f in cesm_atm_fields if f.endswith(".f32")])
    base_cmd = f" -d 26 1800 3600 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in cesm_atm_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}2D_float_plain -i {datasets_path}/cesm_atm/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression   end" in line:
                    vgc_d_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_d_dec_throughput += float(line.split()[-2])
    vgc_d_cmp_throughput /= field_count
    vgc_d_dec_throughput /= field_count
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for field in cesm_atm_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}2D_float_outlier -i {datasets_path}/cesm_atm/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_miranda(error_bound):
    base_cmd = f"miranda_1024x1024x1024_float32.raw -d 1024 1024 1024 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/miranda/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/miranda/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_syntruss(error_bound):
    base_cmd = f"synthetic_truss_with_five_defects_1200x1200x1200_float32.raw -d 1200 1200 1200 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/syntruss/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/syntruss/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_hcci(error_bound):
    base_cmd = f"hcci_oh_560x560x560_float32.raw -d 560 560 560 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/hcci/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/hcci/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_rtm(error_bound):
    rtm_fields = os.listdir(datasets_path + "rtm")
    field_count = len([f for f in os.listdir(datasets_path + "rtm") if f.endswith("000")])
    base_cmd = f" -d 1008 1008 352 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in rtm_fields:
        if(field.endswith("000")):
            vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/rtm/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression   end" in line:
                    vgc_d_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_d_dec_throughput += float(line.split()[-2])
    vgc_d_cmp_throughput /= field_count
    vgc_d_dec_throughput /= field_count
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for field in rtm_fields:
        if(field.endswith("000")):
            vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/rtm/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_magrec(error_bound):
    base_cmd = f"magnetic_reconnection_512x512x512_float32.raw -d 512 512 512 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/magrec/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/magrec/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_hacc(error_bound):
    hacc_fields = os.listdir(datasets_path + "hacc")
    field_count = len([f for f in hacc_fields if f.endswith(".f32")])
    base_cmd = f" -t f32 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in hacc_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path[:-1]} -m plain -i {datasets_path}/hacc/{field}" + base_cmd
            # for i in range(3): # avoid warm up to save time
            #     subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression   end" in line:
                    vgc_d_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_d_dec_throughput += float(line.split()[-2])
    vgc_d_cmp_throughput /= field_count
    vgc_d_dec_throughput /= field_count
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for field in hacc_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path[:-1]} -m outlier -i {datasets_path}/hacc/{field}" + base_cmd
            # for i in range(3): # avoid warm up to save time
            #     subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_scale(error_bound):
    scale_fields = os.listdir(datasets_path + "scale")
    field_count = len([f for f in scale_fields if f.endswith(".f32")])
    base_cmd = f" -d 98 1200 1200 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in scale_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}2D_float_plain -i {datasets_path}/scale/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression   end" in line:
                    vgc_d_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_d_dec_throughput += float(line.split()[-2])
    vgc_d_cmp_throughput /= field_count
    vgc_d_dec_throughput /= field_count
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for field in scale_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}2D_float_outlier -i {datasets_path}/scale/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_nyx(error_bound):
    nyx_fields = os.listdir(datasets_path + "nyx")
    field_count = len([f for f in nyx_fields if f.endswith(".f32")])
    base_cmd = f" -d 512 512 512 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in nyx_fields:
        if(field.endswith(".f32")):
            vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/nyx/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
            for line in result_d.stdout.splitlines():
                if "compression   end" in line:
                    vgc_d_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_d_dec_throughput += float(line.split()[-2])
    vgc_d_cmp_throughput /= field_count
    vgc_d_dec_throughput /= field_count
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for field in nyx_fields:
        if(field.endswith(".f32")):
            vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/nyx/{field}" + base_cmd
            for i in range(3):
                subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_jetin(error_bound):
    base_cmd = f"jicf_q_1408x1080x1100_float32.raw -d 1100 1080 1408 -eb rel {error_bound}"
    vgc_d_cmd = f"{vgc_path}3D_float_plain -i {datasets_path}/jetin/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    result_d = subprocess.run(vgc_d_cmd, shell=True, capture_output=True, text=True)
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for line in result_d.stdout.splitlines():
        if "compression   end" in line:
            vgc_d_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_d_dec_throughput = float(line.split()[-2])
    vgc_o_cmd = f"{vgc_path}3D_float_outlier -i {datasets_path}/jetin/" + base_cmd
    for i in range(3):
        subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
    vgc_o_cmp_throughput = 0.0
    vgc_o_dec_throughput = 0.0
    for line in result_o.stdout.splitlines():
        if "compression   end" in line:
            vgc_o_cmp_throughput = float(line.split()[-2])
        elif "decompression end" in line:
            vgc_o_dec_throughput = float(line.split()[-2])
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


avg_d_cmp_throughput = 0.0
avg_d_dec_throughput = 0.0
avg_o_cmp_throughput = 0.0
avg_o_dec_throughput = 0.0

print(f"Running VGC on QMCPack...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_qmcpack(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"QMCPack VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"QMCPack VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"QMCPack VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"QMCPack VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on CESM_ATM...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_cesm_atm(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"CESM_ATM VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"CESM_ATM VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"CESM_ATM VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"CESM_ATM VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on Miranda...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_miranda(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"Miranda VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"Miranda VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"Miranda VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"Miranda VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on SynTruss...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_syntruss(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"SynTruss VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"SynTruss VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"SynTruss VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"SynTruss VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on HCCI...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_hcci(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"HCCI VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"HCCI VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"HCCI VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"HCCI VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on RTM...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_rtm(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"RTM VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"RTM VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"RTM VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"RTM VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on MagRec...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_magrec(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"MagRec VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"MagRec VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"MagRec VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"MagRec VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on HACC...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_hacc(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"HACC VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"HACC VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"HACC VGC_O compression throughput:  {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"HACC VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on Scale...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_scale(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"Scale VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"Scale VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"Scale VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"Scale VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on Nyx...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_nyx(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"Nyx VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"Nyx VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"Nyx VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"Nyx VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on JetIn...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_jetin(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"JetIn VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"JetIn VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"JetIn VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"JetIn VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print("All single-precision throughput tests completed.")
print(f"Average VGC_D compression throughput: {avg_d_cmp_throughput/11:.2f} GB/s")
print(f"Average VGC_D decompression throughput: {avg_d_dec_throughput/11:.2f} GB/s")
print(f"Average VGC_O compression throughput: {avg_o_cmp_throughput/11:.2f} GB/s")
print(f"Average VGC_O decompression throughput: {avg_o_dec_throughput/11:.2f} GB/s")