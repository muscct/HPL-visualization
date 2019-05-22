
import pandas as pd
import numpy as np
import matplotlib
import sys
from os import listdir, getcwd
from os.path import join
import seaborn as sns
import math
import matplotlib.pyplot as plt


FIGURE_DIR = './figure'

def read_outfile(outpath):
    with open(outpath, 'r') as f:
        currentline = None
        runs = []
        counter = 0
        while True:
            currentline = f.readline()
            if currentline == '':
                counter+=1
            if counter > 50:
                break
            if currentline == 'T/V                N    NB     P     Q               Time                 Gflops\n':
                out = f.readline()
                out = f.readline()
                out = out.split()
                runs.append(out)
        dtype = {'T/V': str, 'N': np.int64, 'NB': np.int64, 'P': int, 'Q':int, 'Time': float, 'Gflops': float}
        runs = pd.DataFrame(data=runs, columns=['T/V', 'N', 'NB', 'P', 'Q', 'Time', 'Gflops'])
        for k, v in dtype.items():
            runs[k] = runs[k].astype(v)
        return runs
def read_hpl_ouptut(folderpath):
    outfiles = listdir(join(getcwd(), folderpath))
    run_df = []
    for i in outfiles:
        if i.endswith('.out'):
            run_df.append(read_outfile(join(folderpath, i)))
    return run_df


def plot_line(hpl_df):
    groupby = ['P', 'Q']
    hpl_df = hpl_df.groupby(groupby)
    for _, (k, df) in enumerate(hpl_df):
        sns.lineplot(x=df['N'], y=df['Gflops'],
                     legend='full', label='P={} Q={}'.format(str(k[0]), str(k[1])))
    plt.savefig(join(FIGURE_DIR, 'lineplot.png'))
    plt.close()



def plot_scatter(hpl_df, groupby=['P', 'Q'], x='N', y='NB'):
    hpl_df = hpl_df.groupby(groupby)
    _, scatter_ax = plt.subplots(math.ceil(len(hpl_df)/2), 2, figsize=(15, 15))
    for i, (k, df) in enumerate(hpl_df):
        ax_index = np.unravel_index(i, scatter_ax.view().shape)

        df.plot.scatter(x=x, y=y, c=df['Gflops'], logy=True,
                        legend=True, ax=scatter_ax[ax_index], title='_'.join(map(str, k)))

    plt.savefig(join(FIGURE_DIR, 'scatter.png'))
    plt.close()

def plot_correlation(hpl_df):
    sns.heatmap(hpl_df.corr())
    plt.savefig(join(FIGURE_DIR, 'correlations.png'))
    plt.close()


if __name__ == '__main__':
    outfolder = './hpl_output'
    run_df = read_hpl_ouptut(outfolder)
    run_df = pd.concat(run_df)
    plot_line(run_df)
    plot_scatter(run_df)
    plot_correlation(run_df)
