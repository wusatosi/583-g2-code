#!/bin/bash

cd /home/jespark/taffo/TAFFO/python_script

#rm /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
#cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
#python optimize.py --iterations=50 --num_components=3 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.5 --no_jump_threshold=1.0

#mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run1.csv
#cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
#python optimize.py --iterations=50 --num_components=4 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.5 --no_jump_threshold=1.0

#mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run2.csv
#cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
#python optimize.py --iterations=50 --num_components=5 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.5 --no_jump_threshold=1.0

#mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run3.csv
#cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
#python optimize.py --iterations=50 --num_components=6 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.5 --no_jump_threshold=1.0

#mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run4.csv
#cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=3 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run5.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=4 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run6.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=5 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run7.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=6 --range_low=0.666666 --range_high=1.500000 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run8.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=3 --range_low=0.5 --range_high=2.0 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run9.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=4 --range_low=0.5 --range_high=2.0 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run10.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=5 --range_low=0.5 --range_high=2.0 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run11.csv
cp /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_default.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv
python optimize.py --iterations=50 --num_components=6 --range_low=0.5 --range_high=2.0 --prob_jump=0.25 --no_jump_threshold=0.5

mv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a.csv /home/jespark/taffo/TAFFO/tool/taffo/ILP/cost/eecs583a_run12.csv