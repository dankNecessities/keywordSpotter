#!/bin/bash
export kws=$(pwd)
export token_dir="$kws/tokens"
export tmp_dir="${kws}/tmp"
export data_dir="${kws}/data"

mkdir $data_dir 
mkdir $tmp_dir 

# Normalize audios
./scripts/sh/normalize.sh || exit 1

# Pad audios
./scripts/sh/pad.sh || exit 1

# Dump padded audios to npy files
./scripts/sh/dumper.sh $1 || exit 1
