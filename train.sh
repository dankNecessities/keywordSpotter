#!/bin/bash
echo 
echo ".......... TRAINING MODEL .........."
echo

kws=$(pwd)
training_path="$kws/data"
nn="${kws}/scripts/model/final_cnn_model.json"
nn_weights="${kws}/scripts/model/weights_final_cnn.h5"

eval "python3 ${kws}/scripts/py/train.py -i $training_path -n $nn -w $nn_weights"

echo 
echo ".......... TRAINING COMPLETE .........."
echo
