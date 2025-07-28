import os, sys

os.chdir("./vgc/vgc-compression/")

os.system("mkdir build")

os.chdir("./build")

os.system("cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../install/ ..")

os.system("make -j && make install")