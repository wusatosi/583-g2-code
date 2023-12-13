import torch
import getLoss as gl
import numpy as np
import pandas as pd
import os
import validate_func as vf
import modify_csv as mc
import subprocess
import argparse
import pathlib
import logging
import datetime

current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
logging.basicConfig(level=logging.INFO, 
                    #filename=f"logs_{current_time}.log", 
                    #filemode="w", 
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler(f"logs_{current_time}.log", mode='a'),
                        logging.StreamHandler()
                    ]) #%(name)s
logging.info(f"Started logging at {current_time}")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations to run")
    parser.add_argument("--num_components_min", type=int, default=1, help="Min number of components to modify")
    parser.add_argument("--num_components_max", type=int, default=20, help="Max number of components to modify")
    parser.add_argument("--seed", type=int, default=-1, help="Numpy random seeds")

    parser.add_argument("--range_low", type=float, default=0.666666, help="Lower bound of range to modify")
    parser.add_argument("--range_high", type=float, default=1.5000015, help="Upper bound of range to modify")
    parser.add_argument("--prob_jump", type=float, default=0.5, help="Probability of jumping to new minima")
    parser.add_argument("--no_jump_threshold", type=float, default=0.25, help="Threshold for jumping to new minima")

    args=parser.parse_args()
    return args

#pathlib.Path(__file__).parent.parent.absolute() should be TAFFO directory. This script should be in TAFFO/python_script
class PerfModelOptimizer():
    def __init__(
            self, 
            current_time=current_time,
            path_to_polybench=pathlib.Path(__file__).absolute().parent.parent / "test/polybench-cpu", 
            path_to_perfCsv=pathlib.Path(__file__).absolute().parent.parent / "tool/taffo/ILP/cost/eecs583a.csv", 
            weight_low=1, 
            weight_high=0,
            num_components_min=1,
            num_components_max=20,
            range_low=0.5,
            range_high=2,
            prob_jump=0.5,
            no_jump_threshold=0.25,
            verbose=True):
        self.current_time = current_time
        self.path_to_polybench = path_to_polybench
        self.path_to_perfCsv = path_to_perfCsv
        self.weight_low = weight_low
        self.weight_high = weight_high
        #ADD_FIX, SUB_FIX
        self.components = "ADD_FLOAT, ADD_DOUBLE, SUB_FLOAT, SUB_DOUBLE, MUL_FIX, MUL_FLOAT, MUL_DOUBLE, DIV_FIX, DIV_FLOAT, DIV_DOUBLE, REM_FIX, REM_FLOAT, REM_DOUBLE, CAST_FIX_FIX, CAST_FIX_FLOAT, CAST_FIX_DOUBLE, CAST_FLOAT_FIX, CAST_FLOAT_DOUBLE, CAST_DOUBLE_FIX, CAST_DOUBLE_FLOAT".split(", ")
        self.num_components_min = num_components_min
        self.num_components_max = num_components_max
        self.range_low = range_low
        self.range_high = range_high
        self.prob_jump = prob_jump
        self.verbose = verbose
        self.no_jump_threshold = no_jump_threshold
        logging.info(f"Hyperparameters: \nnum_components_min: {self.num_components_min}\nnum_components_max: {self.num_components_max}\nrange_low: {self.range_low}\nrange_high: {self.range_high}\nprob_jump: {self.prob_jump}\nno_jump_threshold: {self.no_jump_threshold}\n")
        

    def compile_and_run(self):
        polybench_compile_path = os.path.join(self.path_to_polybench, "compile.sh")
        polybench_run_path = os.path.join(self.path_to_polybench, "run.sh")
        os.system(f"bash {polybench_compile_path}")
        os.system(f"bash {polybench_run_path}")
    
    def only_run(self):
        polybench_run_path = os.path.join(self.path_to_polybench, "run.sh")
        os.system(f"bash {polybench_run_path}")
        
    def get_loss(self):
        #df_val = vf.calc_validate_dataframe(self.path_to_polybench)
        loss = gl.calcLoss(self.weight_low, self.weight_high, self.verbose)
        return loss
    
    def get_random_component(self, components=None):
        if components is None:
            return np.random.choice(self.components)
        else:
            return np.random.choice(components)

    def get_multiple_random_components(self, components=None, num_components_min=1, num_components_max=20):
        num_components = np.random.randint(num_components_min, num_components_max+1)
        if components is None:
            num_choices = min(num_components, len(self.components))
            return np.random.choice(self.components, num_choices, replace=False)
        else:
            num_choices = min(num_components, len(components))
            return np.random.choice(components, num_choices, replace=False)

    def get_random_value(self, low=0.1, high=2):
        return np.random.uniform(low, high)

    def generate_modifications(self, component_list):
        modifications = []
        for component in component_list:
            modifications.append((component, self.get_random_value(self.range_low, self.range_high)))
        return modifications

    def reverse_modifications(self, modifications):
        reverse_modifications = []
        for modification in modifications:
            reverse_modifications.append((modification[0], 1/modification[1]))
        return reverse_modifications

    def remove_components(self, current_components, selected_component_list):
        for component in selected_component_list:
            current_components.remove(component)
        return current_components

    def jump_prob_calculator(self, loss, loss_prev, threshold=0.25, itr=10, itrmax=10):
        current_probability = self.prob_jump * ((itrmax - (itr+1)) / itrmax)
        loss_diff = loss - loss_prev
        loss_percentile = loss_diff/loss
        if loss_percentile > threshold:
            current_probability = 0 # do not jump if loss is too high
        else:
            current_probability *= (1-loss_percentile) # make it less likely to jump if loss is higher
        
        logging.info(f"Current jump probability: {current_probability}")
        return np.random.uniform(0, 1) < current_probability
            

    def optimize(self, maxitr=10):
        """
        Run optimization by maxitr.
        """
        #np_benchmarks = gl.read_text()
        #gl.write_text(np_benchmarks)
        logging.info(f"Benchmarking for {maxitr} indices")
        #logging.info(f"Compiling and running for idx {0}")
        #self.compile_and_run()
        #logging.info(f"Running for idx {0}\n")
        #self.only_run()
        #logging.info(f"Calculating loss for idx {0}\n")
        #loss_prev, np_benchmarks_selected, mean_perfGain_prev = self.get_loss()
        #current_components = self.components.copy()
        #mean_perfGain=None
        #mean_perfGain_prev=None
        for i in range(0, maxitr):
            if i%10==0: # every 10 iterations, reset benchmark to everything, and reset prev_loss
                np_benchmarks = gl.read_text()
                gl.write_text(np_benchmarks)
                logging.info(f"Resetting benchmark to everything for idx {i}")
                logging.info(f"Compiling and running for idx {i}")
                self.compile_and_run()
                #logging.info(f"Running idx {i}\n")
                #self.only_run()
                logging.info(f"Calculating loss for idx {i}\n")
                loss_prev, np_benchmarks_selected, mean_perfGain_prev = self.get_loss()
                current_components = self.components.copy()
                continue

            if len(current_components) == 0:
                logging.info(f"No more components to modify. Resetting components.")
                current_components = self.components.copy()
            component_list = self.get_multiple_random_components(current_components, self.num_components_min, self.num_components_max)
            modifications = self.generate_modifications(component_list)
            logging.info(f"Modifying components {component_list} with modifications {modifications}")
            modified_df = mc.convert_to_dataframe(self.path_to_perfCsv, modifications=modifications)
            mc.write_dataframe_to_file(modified_df, self.path_to_perfCsv)
            logging.info(f"Compiling and running for idx {i}")
            self.compile_and_run()
            #logging.info(f"Running idx {i}\n")
            #self.only_run()
            logging.info(f"Calculating loss for idx {i}\n")
            loss, np_benchmarks_selected, mean_perfGain = self.get_loss()
            logging.info(f"\nloss: {loss}, prev_loss: {loss_prev}\n")
            checkpoint_path = os.path.join(str(pathlib.Path(__file__).absolute().parent.parent), f"tool/taffo/ILP/cost/checkpoints/model_{self.current_time}")
            mc.write_checkpoints(modified_df, checkpoint_root=checkpoint_path, itr=i, mean_perfGain=mean_perfGain, loss=loss)
            if loss < loss_prev:
            #if mean_perfGain > mean_perfGain_prev:
                logging.info(f"Loss decreased from {loss_prev} to {loss}. Resetting components.")
                #logging.info(f"Mean performance gain increased from {mean_perfGain_prev} to {mean_perfGain}. Resetting components.")
                loss_prev = loss
                #mean_perfGain_prev = mean_perfGain
                current_components = self.components.copy()
                gl.write_text(np_benchmarks_selected)
            elif self.jump_prob_calculator(loss, loss_prev, self.no_jump_threshold, i, maxitr):
            #elif self.jump_prob_calculator(mean_perfGain, mean_perfGain_prev, self.no_jump_threshold, i, maxitr):
                logging.info(f"Loss increased from {loss_prev} to {loss}. Jumping to search new minima.")
                #logging.info(f"Mean performance gain decreased from {mean_perfGain_prev} to {mean_perfGain}. Jumping to search new minima.")
                loss_prev = loss
                #mean_perfGain_prev = mean_perfGain
                current_components = self.components.copy()
                gl.write_text(np_benchmarks_selected)
            else: # maybe elif & probabilty jump
                logging.info(f"Loss increased from {loss_prev} to {loss}. Removing components {component_list} and reversing modifications.")
                #logging.info(f"Mean performance gain decreased from {mean_perfGain_prev} to {mean_perfGain}. Removing components {component_list} and reversing modifications.")
                mc.write_dataframe_to_file(mc.convert_to_dataframe(self.path_to_perfCsv, modifications=self.reverse_modifications(modifications)), self.path_to_perfCsv)
                #self.remove_components(current_components, component_list)

def main():
    args = parse_arguments()
    if args.seed > 0:
        np.random.seed(args.seed)
        logging.info(f"Setting seed to {args.seed}")
    pmo = PerfModelOptimizer(
        current_time=current_time,
        weight_low=1, weight_high=0, 
        range_high=args.range_high,
        range_low=args.range_low, 
        num_components_min=args.num_components_min, 
        num_components_max=args.num_components_max, 
        prob_jump=args.prob_jump,
        no_jump_threshold=args.no_jump_threshold, 
        verbose=True)
    pmo.optimize(maxitr=args.iterations)

if __name__ == "__main__":
    main()