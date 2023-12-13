#!/bin/bash

cd /home/$UNIQNAME/taffo/TAFFO/test/polybench-cpu/checkpoints/$PATH_TO_CKPT

cp /home/$UNIQNAME/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/$UNIQNAME/taffo/TAFFO/test/polybench-cpu/checkpoints/$PATH_TO_CKPT
python combine_csv.py
python ml_model.py
