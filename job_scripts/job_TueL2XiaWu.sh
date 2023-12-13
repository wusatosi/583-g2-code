#!/bin/bash

cd /home/jespark/taffo/TAFFO/python_script

rm /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components_min=1 --num_components_max=20 --range_low=0.5 --range_high=2.000000 --prob_jump=1.0 --no_jump_threshold=5.0 --seed=1

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run1.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components_min=1 --num_components_max=20 --range_low=0.5 --range_high=2.000000 --prob_jump=0.8 --no_jump_threshold=3.0 --seed=2