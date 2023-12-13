## Runs polybench-cpu and get the loss value
import validate_func as vf
import os
import numpy as np
import pandas as pd
import pathlib
import logging
logger = logging.getLogger(__name__)

def read_text(filename=pathlib.Path(__file__).absolute().parent.parent / 'test/polybench-cpu/utilities/benchmark_list_default'):
    df_benchmarks = pd.read_csv(filename, header=None)
    np_benchmarks = df_benchmarks.to_numpy()
    np_benchmarks = np_benchmarks.astype(str)
    return np_benchmarks

def select_idx(np_benchmarks, indices_list):
    """
    select components from indices from np_benchmarks
    """
    new_idx = np.array([])
    for idx in indices_list:
        np_idx = np.char.find(np_benchmarks, idx)
        np_idx = np_idx>0
        new_idx = np.append(new_idx, np_benchmarks[np_idx])
        #new_idx.append(np_benchmarks[np_idx])
    return new_idx

def write_text(np_benchmarks, filename=pathlib.Path(__file__).absolute().parent.parent / 'test/polybench-cpu/utilities/benchmark_list'):
    """
    write np_benchmarks to filename
    """
    df_benchmarks = pd.DataFrame(np_benchmarks)
    df_benchmarks.to_csv(filename, header=None, index=None)

def calcLoss(weight_low=2, weight_high=1, verbose=False):
    """
    Loss function for performance model output

    Args:
        weight_low: loss weights for under performing benchmarks
        weight_high: loss weights for over performing benchmarks
        verbose: If True, print out the performance raw values
    """
    # Calculate loss
    #df_perf = vf.calc_validate_dataframe('/home/jespark/taffo/TAFFO/test/polybench-cpu') # pandas dataframe
    df_perf = vf.calc_validate_dataframe(pathlib.Path(__file__).absolute().parent.parent / 'test/polybench-cpu') # pandas dataframe
    #df_perf_faster1 = df_perf['speedup']>1
    #df_perf_faster_idx = df_perf[df_perf_faster1].index
    if verbose:
        logger.info("\n" + df_perf.to_string())
    df_perf_slower = df_perf['speedup']<1
    df_perf_slower_idx = df_perf[df_perf_slower].index
    perf_slower_idx = df_perf_slower_idx.to_list()
    
    np_benchmarks = read_text(pathlib.Path(__file__).absolute().parent.parent / "test/polybench-cpu/utilities/benchmark_list_default")
    np_benchmarks_selected = select_idx(np_benchmarks, perf_slower_idx)
    #write_text(np_benchmarks_selected, pathlib.Path(__file__).absolute().parent.parent / "test/polybench-cpu/utilities/benchmark_list") # write when not reverting

    np_perf = df_perf.to_numpy()
    np_perf = np_perf.astype(np.float32)
    
    # Performance gains
    perfGains = np_perf[:,-1]
    mean_perfGain = np.mean(perfGains)
    if verbose:
        logger.info("Mean performance gains: {}".format(mean_perfGain))
    perfLoss = perfGains-1
    perfLoss_negIdx = perfLoss<0
    perfLoss_posIdx = perfLoss>=0
    perfLoss[perfLoss_negIdx] *= -weight_low # weight for under performing benchmarks
    perfLoss[perfLoss_posIdx] *= -weight_high # weight for over performing benchmarks

    # Calculate Loss
    # L2 error
    perfLoss = np.power(perfLoss, 2)
    #loss =  np.sum(perfLoss) / len(perfLoss_negIdx)
    loss = np.mean(perfLoss[perfLoss_negIdx]) # only consider under performing benchmarks

    return loss, np_benchmarks_selected, mean_perfGain

def write_text_to_file(np_benchmarks_selected):
    write_text(np_benchmarks_selected, pathlib.Path(__file__).absolute().parent.parent / "test/polybench-cpu/utilities/benchmark_list")

def main():
    loss, _ = calcLoss(verbose=True)
    logger.info("Loss: {}".format(loss))

if __name__ == "__main__":
    main()