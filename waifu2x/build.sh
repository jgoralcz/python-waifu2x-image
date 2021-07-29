#!/bin/sh

# get path 
BEFORE=$(pwd)

set -eux && git clone https://github.com/DeadSix27/waifu2x-converter-cpp /waifu2x-cpp

# build
cd /waifu2x-cpp
cmake .
make -j4

cd $BEFORE

# get noise files
mkdir /usr/local/share/waifu2x-converter-cpp/
cd waifu2x/noise_files
cp *.* /usr/local/share/waifu2x-converter-cpp/

mkdir /data
