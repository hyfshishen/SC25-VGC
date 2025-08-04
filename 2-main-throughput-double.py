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


def run_s3d(error_bound):
    s3d_fields = os.listdir(datasets_path + "s3d")
    field_count = len([f for f in s3d_fields if f.endswith(".d64")])
    base_cmd = f" -d 5500 500 500 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in s3d_fields:
        if(field.endswith(".d64")):
            vgc_d_cmd = f"{vgc_path}3D_double_plain -i {datasets_path}/s3d/{field}" + base_cmd
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
    for field in s3d_fields:
        if(field.endswith(".d64")):
            vgc_o_cmd = f"{vgc_path}3D_double_outlier -i {datasets_path}/s3d/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


def run_nwchem(error_bound):
    nwchem_fields = os.listdir(datasets_path + "nwchem")
    field_count = len([f for f in nwchem_fields if f.endswith(".d64")])
    base_cmd = f" -t f64 -eb rel {error_bound}"
    vgc_d_cmp_throughput = 0.0
    vgc_d_dec_throughput = 0.0
    for field in nwchem_fields:
        if(field.endswith(".d64")):
            vgc_d_cmd = f"{vgc_path[:-1]} -m plain -i {datasets_path}/nwchem/{field}" + base_cmd
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
    for field in nwchem_fields:
        if(field.endswith(".d64")):
            vgc_o_cmd = f"{vgc_path[:-1]} -m outlier -i {datasets_path}/nwchem/{field}" + base_cmd
            result_o = subprocess.run(vgc_o_cmd, shell=True, capture_output=True, text=True)
            for line in result_o.stdout.splitlines():
                if "compression   end" in line:
                    vgc_o_cmp_throughput += float(line.split()[-2])
                elif "decompression end" in line:
                    vgc_o_dec_throughput += float(line.split()[-2])
    vgc_o_cmp_throughput /= field_count
    vgc_o_dec_throughput /= field_count
    return vgc_d_cmp_throughput, vgc_d_dec_throughput, vgc_o_cmp_throughput, vgc_o_dec_throughput


avg_d_cmp_throughput = 0.0
avg_d_dec_throughput = 0.0
avg_o_cmp_throughput = 0.0
avg_o_dec_throughput = 0.0

print(f"Running VGC on S3D...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_s3d(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"S3D VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"S3D VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"S3D VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"S3D VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print(f"Running VGC on NWChem...")
temp_d_cmp_throughput = 0.0
temp_d_dec_throughput = 0.0
temp_o_cmp_throughput = 0.0
temp_o_dec_throughput = 0.0
for eb in [1e-2, 1e-3, 1e-4]:
    d_cmp, d_dec, o_cmp, o_dec = run_nwchem(eb)
    temp_d_cmp_throughput += float(d_cmp)
    temp_d_dec_throughput += float(d_dec)
    temp_o_cmp_throughput += float(o_cmp)
    temp_o_dec_throughput += float(o_dec)
print(f"NWChem VGC_D compression throughput: {temp_d_cmp_throughput/3:.2f} GB/s")
print(f"NWChem VGC_D decompression throughput: {temp_d_dec_throughput/3:.2f} GB/s")
print(f"NWChem VGC_O compression throughput: {temp_o_cmp_throughput/3:.2f} GB/s")
print(f"NWChem VGC_O decompression throughput: {temp_o_dec_throughput/3:.2f} GB/s")
avg_d_cmp_throughput += temp_d_cmp_throughput / 3
avg_d_dec_throughput += temp_d_dec_throughput / 3
avg_o_cmp_throughput += temp_o_cmp_throughput / 3
avg_o_dec_throughput += temp_o_dec_throughput / 3
print()

print("All double-precision throughput tests completed.")
print(f"Average VGC_D compression throughput: {avg_d_cmp_throughput/2:.2f} GB/s")
print(f"Average VGC_D decompression throughput: {avg_d_dec_throughput/2:.2f} GB/s")
print(f"Average VGC_O compression throughput: {avg_o_cmp_throughput/2:.2f} GB/s")
print(f"Average VGC_O decompression throughput: {avg_o_dec_throughput/2:.2f} GB/s")