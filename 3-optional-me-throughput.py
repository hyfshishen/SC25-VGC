import os, sys
import subprocess

# compilation
os.chdir("./vgc/vgc-versatility/memory-efficient")
os.system("mkdir build")
os.chdir("./build")
os.system("cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install/ ..")
os.system("make -j && make install")
os.chdir("../../../")

# execution
vgc_path_f32_d = "./vgc/vgc-versatility/memory-efficient/install/bin/memory-efficient-plain_f32 -m plain -t f32"
vgc_path_f32_o = "./vgc/vgc-versatility/memory-efficient/install/bin/memory-efficient-plain_f32 -m outlier -t f32"
vgc_path_f64_d = "./vgc/vgc-versatility/memory-efficient/install/bin/memory-efficient-plain_f64 -m plain -t f64"
vgc_path_f64_o = "./vgc/vgc-versatility/memory-efficient/install/bin/memory-efficient-plain_f64 -m outlier -t f64"
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
        if "compression   end" in line:
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




print(f"Running VGC Memory-Efficient (ME) on QMCPack...")
vgc_d_me, vgc_o_me = run_single("qmcpack")
print(f"QMCPack VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"QMCPack VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on CESM-ATM...")
vgc_d_me, vgc_o_me = run_single("cesm_atm")
print(f"CESM-ATM VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"CESM-ATM VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on Miranda...")
vgc_d_me, vgc_o_me = run_single("miranda")
print(f"Miranda VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"Miranda VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on SynTruss...")
vgc_d_me, vgc_o_me = run_single("syntruss")
print(f"SynTruss VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"SynTruss VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on HCCI...")
vgc_d_me, vgc_o_me = run_single("hcci")
print(f"HCCI VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"HCCI VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on RTM...")
vgc_d_me, vgc_o_me = run_single("rtm")
print(f"RTM VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"RTM VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on MagRec...")
vgc_d_me, vgc_o_me = run_single("magrec")
print(f"MagRec VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"MagRec VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on HACC...")
vgc_d_me, vgc_o_me = run_single("hacc")
print(f"HACC VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"HACC VGC_O_ME compression throughput: {vgc_o_me} GB/s") 
print()

print(f"Running VGC Memory-Efficient (ME) on SCALE...")
vgc_d_me, vgc_o_me = run_single("scale")
print(f"SCALE VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"SCALE VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on NYX...")
vgc_d_me, vgc_o_me = run_single("nyx")
print(f"NYX VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"NYX VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on JetIn...")
vgc_d_me, vgc_o_me = run_single("jetin")
print(f"JetIn VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"JetIn VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()   

print(f"Running VGC Memory-Efficient (ME) on S3D...")
vgc_d_me, vgc_o_me = run_double("s3d")
print(f"S3D VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"S3D VGC_O_ME compression throughput: {vgc_o_me} GB/s")
print()

print(f"Running VGC Memory-Efficient (ME) on NWChem...")
vgc_d_me, vgc_o_me = run_double("nwchem")
print(f"NWChem VGC_D_ME compression throughput: {vgc_d_me} GB/s")
print(f"NWChem VGC_O_ME compression throughput: {vgc_o_me} GB/s")