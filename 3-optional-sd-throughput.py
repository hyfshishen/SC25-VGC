import os, sys
import subprocess

# execution
vgc_path_f32_d = "./vgc/vgc-versatility/random-access/install/bin/cuSZp -m plain -t f32"
vgc_path_f32_o = "./vgc/vgc-versatility/random-access/install/bin/cuSZp -m outlier -t f32"
vgc_path_f64_d = "./vgc/vgc-versatility/random-access/install/bin/cuSZp -m plain -t f64"
vgc_path_f64_o = "./vgc/vgc-versatility/random-access/install/bin/cuSZp -m outlier -t f64"
datasets_path = "./datasets/"

dds = {
    "qmcpack": "qmcpack/einspline_288_115_69_69.pre.f32",
    "cesm_atm": "cesm_atm/CMFDQR_1_26_1800_3600.f32",
    "miranda": "miranda/miranda_1024x1024x1024_float32.raw",
    "syntruss": "syntruss/synthetic_truss_with_five_defects_1200x1200x1200_float32.raw",
    "hcci": "hcci/hcci_oh_560x560x560_float32.raw",
    "rtm": "rtm/pressure_2000",
    "magrec": "magrec/magnetic_reconnection_512x512x512_float32.raw",
    "hacc": "hacc/vx.f32",
    "scale": "scale/QS-98x1200x1200.f32",
    "nyx": "nyx/baryon_density.f32",
    "jetin": "jetin/jicf_q_1408x1080x1100_float32.raw",
    "s3d": "s3d/stat_planar.1.7000E-03.field.d64",
    "nwchem": "nwchem/acd-tst.bin.d64"
}

def capture_output(raw):
    for line in raw.splitlines():
        if "decompression end" in line:
            return float(line.split()[-2])
        
def run_single(dataset):
    error_bounds = ["1e-2", "1e-3", "1e-4"]
    vgc_d_me = 0.0
    vgc_o_me = 0.0
    base_cmd_f32_d = f"{vgc_path_f32_d} -i {datasets_path + dds[dataset]} -eb rel"
    for error_bound in error_bounds:
        cmd_f32_d = base_cmd_f32_d + " " + error_bound
        for i in range(3):
            subprocess.run(cmd_f32_d, shell=True, capture_output=True, text=True)
        result = subprocess.run(cmd_f32_d, shell=True, capture_output=True, text=True)
        vgc_d_me += capture_output(result.stdout)
    vgc_d_me = vgc_d_me/len(error_bounds)
    base_cmd_f32_o = f"{vgc_path_f32_o} -i {datasets_path + dds[dataset]} -eb rel"
    for error_bound in error_bounds:
        cmd_f32_o = base_cmd_f32_o + " " + error_bound
        for i in range(3):
            subprocess.run(cmd_f32_o, shell=True, capture_output=True, text=True)
        result = subprocess.run(cmd_f32_o, shell=True, capture_output=True, text=True)
        vgc_o_me += capture_output(result.stdout)
    vgc_o_me = vgc_o_me/len(error_bounds)
    return vgc_d_me, vgc_o_me


def run_double(dataset):
    error_bounds = ["1e-2", "1e-3", "1e-4"]
    vgc_d_me = 0.0
    vgc_o_me = 0.0
    base_cmd_f64_d = f"{vgc_path_f64_d} -i {datasets_path + dds[dataset]} -eb rel"
    for error_bound in error_bounds:
        cmd_f64_d = base_cmd_f64_d + " " + error_bound
        for i in range(3):
            subprocess.run(cmd_f64_d, shell=True, capture_output=True, text=True)
        result = subprocess.run(cmd_f64_d, shell=True, capture_output=True, text=True)
        vgc_d_me += capture_output(result.stdout)
    vgc_d_me = vgc_d_me/len(error_bounds)
    base_cmd_f64_o = f"{vgc_path_f64_o} -i {datasets_path + dds[dataset]} -eb rel"
    for error_bound in error_bounds:
        cmd_f64_o = base_cmd_f64_o + " " + error_bound
        for i in range(3):
            subprocess.run(cmd_f64_o, shell=True, capture_output=True, text=True)
        result = subprocess.run(cmd_f64_o, shell=True, capture_output=True, text=True)
        vgc_o_me += capture_output(result.stdout)
    vgc_o_me = vgc_o_me/len(error_bounds)
    return vgc_d_me, vgc_o_me




print(f"Running VGC Selective Decompression (SD) on QMCPack...")
vgc_d_me, vgc_o_me = run_single("qmcpack")
print(f"QMCPack VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"QMCPack VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on CESM-ATM...")
vgc_d_me, vgc_o_me = run_single("cesm_atm")
print(f"CESM-ATM VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"CESM-ATM VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on Miranda...")
vgc_d_me, vgc_o_me = run_single("miranda")
print(f"Miranda VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"Miranda VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on SynTruss...")
vgc_d_me, vgc_o_me = run_single("syntruss")
print(f"SynTruss VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"SynTruss VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on HCCI...")
vgc_d_me, vgc_o_me = run_single("hcci")
print(f"HCCI VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"HCCI VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on RTM...")
vgc_d_me, vgc_o_me = run_single("rtm")
print(f"RTM VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"RTM VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on MagRec...")
vgc_d_me, vgc_o_me = run_single("magrec")
print(f"MagRec VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"MagRec VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on HACC...")
vgc_d_me, vgc_o_me = run_single("hacc")
print(f"HACC VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"HACC VGC_O decompression throughput: {vgc_o_me} GB/s") 
print()

print(f"Running VGC Selective Decompression (SD) on SCALE...")
vgc_d_me, vgc_o_me = run_single("scale")
print(f"SCALE VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"SCALE VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on NYX...")
vgc_d_me, vgc_o_me = run_single("nyx")
print(f"NYX VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"NYX VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on JetIn...")
vgc_d_me, vgc_o_me = run_single("jetin")
print(f"JetIn VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"JetIn VGC_O decompression throughput: {vgc_o_me} GB/s")
print()   

print(f"Running VGC Selective Decompression (SD) on S3D...")
vgc_d_me, vgc_o_me = run_double("s3d")
print(f"S3D VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"S3D VGC_O decompression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Selective Decompression (SD) on NWChem...")
vgc_d_me, vgc_o_me = run_double("nwchem")
print(f"NWChem VGC_D decompression throughput: {vgc_d_me} GB/s")
print(f"NWChem VGC_O decompression throughput: {vgc_o_me} GB/s")