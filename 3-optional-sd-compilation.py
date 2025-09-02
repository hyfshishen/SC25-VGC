import os, sys
import subprocess

# compilation
os.chdir("./vgc/vgc-versatility/random-access")
os.system("mkdir build")
os.chdir("./build")
os.system("cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install/ ..")
os.system("make -j && make install")
os.chdir("../../../")