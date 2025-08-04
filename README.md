# SC25-VGC

This repository is for AD/AE process for SC'25 accepted paper "GPU Lossy Compression for HPC Can Be Versatile and Ultra-fast".


## 1. Introduction

VGC is an error-bounded lossy compression library specifically designed for NVIDIA GPUs to compress floating-point data.
This repository is for SC'25 AD/AE process.
The official and final version of VGC will be updated into cuSZp repository [[LINK](https://github.com/szcompressor/cuSZp)] -- that's the reason you may see some "cuSZp" texts in compilation/execution phases.
_For simplicity, we will still use the name VGC in this repository README, to align with what is reported in the submission_.

In short, this repository contains three sections:
- **2. Configuring VGC and Datasets**: In this section, reviewer can check software/hardware dependencies, compile VGC to executable binaries, and set up HPC datasets evaluated in the original paper.
- **3. Reproducing Main Evaluation Results**: In this section, reviewer can reproduce main paper results that are related to the key metrics of VGC compressor, including throughput and compression ratios.
- **4. (Optional) Other Evaluation Results**: In this section, reviewer can selectively reproduce other results lie in discussion/case study sections. Note that this section contains extra environment and datasets setups.

## 2. Configuring VGC and Datasets

### 2.1 Software/Hardware Dependencies

Following software and hardware dependencies are neccessary to compile, execute, and evaluate VGC.

- A Linux Machine (e.g., Ubuntu 22.04, but other OSs should work)
- Git 2.15 or newer
- CMake 3.21 or newer
- CUDA 11.0 or newer
- One NVIDIA A100 GPU (both 40 GB and 80 GB vmem capacities work)
- Python 3 (this is for executing our wrapped up reproducing scripts)

### 2.2 Compilng VGC

VGC can be compiled and installed by following commands.

```shell
# First, git clone this repository.
$ git clone https://github.com/hyfshishen/SC25-VGC.git

# Then, change directory to this repository.
$ cd SC25-VGC

# Finally, compile VGC via following commands.
$ python3 0-compile-vgc.py
```

All compiled executable binaries used to evaluate this work can be found in folder ```./vgc/vgc-compression/install/bin/```.
To verify whether installation is succesful, you can execute command ```./vgc/vgc-compression/install/bin/cuSZp_test_f32```.
If results are shown like text block below:
```shell
$ ./vgc/vgc-compression/install/bin/cuSZp_test_f32 
Generating test data...

=================================================
=========Testing cuSZp-p-f32 on REL 1E-2=========
=================================================
cuSZp-p finished!
cuSZp-p compression   end-to-end speed: 348.937382 GB/s
cuSZp-p decompression end-to-end speed: 362.122041 GB/s
cuSZp-p compression ratio: 6.286837
Pass error check!
Done with testing cuSZp-p on REL 1E-2!

=================================================
=========Testing cuSZp-o-f32 on REL 1E-2=========
=================================================
cuSZp-o finished!
cuSZp-o compression   end-to-end speed: 315.854401 GB/s
cuSZp-o decompression end-to-end speed: 304.921636 GB/s
cuSZp-o compression ratio: 11.985018
Pass error check!
Done with testing cuSZp-o on REL 1E-2!
```
That means VGC installation is succesful, please proceed to the next step.

### 2.3 Downloading Datasets

There are 13 HPC datasets (11 single-precision and 2 double-precision) in total that are used to evaluate VGC.
*The total size for those datasets requires 100 GB storage space.*
12 of them (except RTM) can be automatially downloaded via following script.
And these datasets will be downloaded into different folders under ```./datasets/```. 

```shell
$ python3 1-download-datasets.py
# This command helps you download and arrange 12/13 HPC datasets (except RTM, RTM requires manually download from Google shared link).
```


RTM dataset, which has three fields *pressure_1000*, *pressure_2000*, and *pressure_3000*, cannot be downloaded through direct link access using ```wget```.
We apologize for any inconvenience this may cause.
As a result, we uploaded RTM in Google Drive. 
The download links can be found here: *pressure_1000* ([link](https://drive.google.com/file/d/1EyhvfKHlLlJiDwqQ28XXn5Dbqiz8Zn3M/view?usp=sharing)), *pressure_2000* ([link](https://drive.google.com/file/d/1StITO-BxW4JHocx9-Pwe6jUy12j68Tva/view?usp=sharing)), *pressure_3000* ([link](https://drive.google.com/file/d/1FlKKw5HJQIi64vgeQ47GQWi-4BrlWRAJ/view?usp=sharing)).
After you finish download it, please create a new folder ```rtm``` under ```./datasets/``` and move three RTM fields inside.

After this step, your local repository should have the following structure.
```shell
-- vgc
    -- vgc-compression/
    -- # ... (other code base for optional evaluations)
-- datasets
    -- cesm_atm/
        -- # ... (all cesm_atm fields)
    -- hacc/
        -- # ... (all hacc fields)
    -- hcci/
        -- # ... (all hcci fields)
    -- jetin/
        -- # ... (all jetin fields)
    -- magrec/
        -- # ... (all magrec fields)
    -- miranda/
        -- # ... (all miranda fields)
    -- nwchem/
        -- # ... (all newchem fields)
    -- nyx/
        -- # ... (all nyx fields)
    -- qmcpack/
        -- # ... (all qmcpack fields)
    -- rtm/
        -- pressure_1000
        -- pressure_2000
        -- pressure_3000
    -- s3d/
        -- # ... (all s3d fields)
    -- scale/
        -- # ... (all scale fields)
    -- syntruss/
        -- # ... (all syntruss fields)
-- README.md
-- 0-compile-vgc.py
-- 1-download-datasets.py
- # ... (other Python scripts)
```

To double check downloaded datasets, you can try the following command.
```shell
$ du -sh ./datasets/*
21G     ./datasets/cesm_atm
24G     ./datasets/hacc
670M    ./datasets/hcci
6.3G    ./datasets/jetin
513M    ./datasets/magrec
4.1G    ./datasets/miranda
13G     ./datasets/nwchem
3.1G    ./datasets/nyx
1.2G    ./datasets/qmcpack
4.0G    ./datasets/rtm
52G     ./datasets/s3d
6.4G    ./datasets/scale
6.5G    ./datasets/syntruss
```
That means dataset preparation is successful. Please proceed to the next step.

## 3. Reproducing Main Evaluation Results

This section provides instructions on reproducing the main evaluation results for VGC.
Since VGC is a GPU lossy compressor for single-precision and double-precision HPC datasets, the main evaluation for VGC is the **compression/decompression throughput** and **compression ratios**.
For other optional evaluations, reviewers can selectively execute them in Section 4.

### 3.1 Single-precision Throughput (Figure 12, Figure 13)

Executing following prepared Python script can reproduce VGC single-precision compression/decompression throughput results.

```shell
$ python3 2-main-throughput-single.py 
Running VGC on QMCPack...
QMCPack VGC_D compression throughput: 246.54 GB/s
QMCPack VGC_D decompression throughput: 313.39 GB/s
QMCPack VGC_O compression throughput: 225.11 GB/s
QMCPack VGC_O decompression throughput: 254.06 GB/s

Running VGC on CESM_ATM...
CESM_ATM VGC_D compression throughput: 248.62 GB/s
CESM_ATM VGC_D decompression throughput: 402.17 GB/s
CESM_ATM VGC_O compression throughput: 269.78 GB/s
CESM_ATM VGC_O decompression throughput: 389.63 GB/s

Running VGC on Miranda...
Miranda VGC_D compression throughput: 302.02 GB/s
Miranda VGC_D decompression throughput: 582.03 GB/s
Miranda VGC_O compression throughput: 300.22 GB/s
Miranda VGC_O decompression throughput: 378.78 GB/s

Running VGC on SynTruss...
SynTruss VGC_D compression throughput: 385.66 GB/s
SynTruss VGC_D decompression throughput: 854.16 GB/s
SynTruss VGC_O compression throughput: 341.13 GB/s
SynTruss VGC_O decompression throughput: 499.50 GB/s

Running VGC on HCCI...
HCCI VGC_D compression throughput: 266.39 GB/s
HCCI VGC_D decompression throughput: 595.74 GB/s
HCCI VGC_O compression throughput: 204.99 GB/s
HCCI VGC_O decompression throughput: 484.10 GB/s

Running VGC on RTM...
RTM VGC_D compression throughput: 380.41 GB/s
RTM VGC_D decompression throughput: 818.64 GB/s
RTM VGC_O compression throughput: 332.31 GB/s
RTM VGC_O decompression throughput: 603.31 GB/s

Running VGC on MagRec...
MagRec VGC_D compression throughput: 206.54 GB/s
MagRec VGC_D decompression throughput: 158.93 GB/s
MagRec VGC_O compression throughput: 165.64 GB/s
MagRec VGC_O decompression throughput: 308.57 GB/s

Running VGC on HACC...
HACC VGC_D compression throughput: 310.88 GB/s
HACC VGC_D decompression throughput: 393.34 GB/s
HACC VGC_O compression throughput:  333.08 GB/s
HACC VGC_O decompression throughput: 395.94 GB/s

Running VGC on Scale...
Scale VGC_D compression throughput: 212.66 GB/s
Scale VGC_D decompression throughput: 400.93 GB/s
Scale VGC_O compression throughput: 212.81 GB/s
Scale VGC_O decompression throughput: 354.12 GB/s

Running VGC on Nyx...
Nyx VGC_D compression throughput: 240.59 GB/s
Nyx VGC_D decompression throughput: 303.34 GB/s
Nyx VGC_O compression throughput: 206.04 GB/s
Nyx VGC_O decompression throughput: 291.93 GB/s

Running VGC on JetIn...
JetIn VGC_D compression throughput: 523.29 GB/s
JetIn VGC_D decompression throughput: 2011.71 GB/s
JetIn VGC_O compression throughput: 551.28 GB/s
JetIn VGC_O decompression throughput: 1726.97 GB/s

All single-precision throughput tests completed.
Average VGC_D compression throughput: 302.14 GB/s
Average VGC_D decompression throughput: 621.31 GB/s
Average VGC_O compression throughput: 286.58 GB/s
Average VGC_O decompression throughput: 516.99 GB/s
```

The throughput results should match or close to what is reported in Figure 12 (single-precision compression) and Figure 13 (single-precision decompression). 
Note that throughput may vary due to several factors (Dynamic Frequency Scaling, Thermal Throttling, etc); reviewers can re-run this script to obtain consistent results.


### 3.2 Double-precision Throughput (Figure 14)

Executing following prepared Python script can reproduce VGC double-precision compression/decompression throughput results.

```shell
$ python3 2-main-throughput-double.py 
Running VGC on S3D...
S3D VGC_D compression throughput: 606.34 GB/s
S3D VGC_D decompression throughput: 1485.90 GB/s
S3D VGC_O compression throughput: 662.89 GB/s
S3D VGC_O decompression throughput: 1502.96 GB/s

Running VGC on NWChem...
NWChem VGC_D compression throughput: 530.62 GB/s
NWChem VGC_D decompression throughput: 1142.95 GB/s
NWChem VGC_O compression throughput: 506.43 GB/s
NWChem VGC_O decompression throughput: 999.34 GB/s

All double-precision throughput tests completed.
Average VGC_D compression throughput: 568.48 GB/s
Average VGC_D decompression throughput: 1314.42 GB/s
Average VGC_O compression throughput: 584.66 GB/s
Average VGC_O decompression throughput: 1251.15 GB/s
```

The throughput results should match or close to what is reported in Figure 14 (left for compression, right for decompression). 
Note that throughput may vary due to several factors (Dynamic Frequency Scaling, Thermal Throttling, etc); reviewers can re-run this script to obtain consistent results.

### 3.3 Compression Ratios (Table 2)

Executing following prepared Python script can reproduce VGC compression ratio results.

```shell
$ python3 2-main-compression-ratio.py 
Running VGC on QMCPack with error bound 0.0001...
QMCPack compression ratio testing completed:
VGC_D: 4.39780037913534
VGC_O: 4.410282750659778

Running VGC on CESM_ATM with error bound 0.0001...
CESM_ATM compression ratio testing completed:
VGC_D: 5.853428092435023
VGC_O: 13.078436499408149

Running VGC on Miranda with error bound 0.0001...
Miranda compression ratio testing completed:
VGC_D: 2.3453982191692035
VGC_O: 4.246087390984657

Running VGC on SynTruss with error bound 0.0001...
SynTruss compression ratio testing completed:
VGC_D: 4.431762081837473
VGC_O: 4.514645277080295

Running VGC on HCCI with error bound 0.0001...
HCCI compression ratio testing completed:
VGC_D: 10.87289236173368
VGC_O: 16.638339773825884

Running VGC on RTM with error bound 0.0001...
RTM compression ratio testing completed:
VGC_D: 13.421132248645558
VGC_O: 14.367026386659173

Running VGC on MagRec with error bound 0.0001...
MagRec compression ratio testing completed:
VGC_D: 5.505416992148885
VGC_O: 6.557747022515887

Running VGC on HACC with error bound 0.0001...
HACC compression ratio testing completed:
VGC_D: 2.925713818243781
VGC_O: 4.56036599655104

Running VGC on SCALE with error bound 0.0001...
SCALE compression ratio testing completed:
VGC_D: 5.001284668377916
VGC_O: 11.975460446868524

Running VGC on NYX with error bound 0.0001...
NYX compression ratio testing completed:
VGC_D: 5.928949381249487
VGC_O: 10.342027929977576

Running VGC on JetIn with error bound 0.0001...
JetIn compression ratio testing completed:
VGC_D: 194.6607659935775
VGC_O: 198.43005510018264

Running VGC on S3D with error bound 0.0001...
S3D compression ratio testing completed:
VGC_D: 13.238351677437644
VGC_O: 55.75890665478384

Running VGC on NWChem with error bound 0.0001...
NWChem compression ratio testing completed:
VGC_D: 21.29462197891387
VGC_O: 21.304424613043153

All compression ratio tests completed.
```

Compression results reported in command line environment should match what is reported in **Table-2**.

## 4. (Optional) Other Evaluation Results

memory efficient compression

selective decompression

RTM ratios





