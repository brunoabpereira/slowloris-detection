import re
import pandas as pd
import matplotlib.pyplot as plt

def plot_features(attack_series, normal_series, slide, start_obs, N, title, ylabel, dir):
    """
        plot and save attack and normal features.
        
        Args:
            attack_series: pandas.core.series.Series
            normal_series: pandas.core.series.Series
            slide: observation window length
            start_obs: initial observation window
            N: number of observation windows to plot
    """
    a = attack_series[start_obs:start_obs+N]
    n = normal_series[start_obs:start_obs+N]
    time = range(start_obs*slide, (start_obs+N)*slide, slide) # seconds
    plt.clf()
    plt.plot(time,a,label='attack')
    plt.plot(time,n,label='normal')
    plt.legend(loc="upper left")
    plt.xlabel('Time (seconds)')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(False)
    plt.tight_layout()
    plt.savefig('{}/{}'.format(dir, re.sub('\s+', '_', title.strip())))

plots_dir = 'imgs'
data_dir = 'dataset'

# load data
attack_data = pd.read_csv('{}/attack_dataset.csv'.format(data_dir))
normal_data = pd.read_csv('{}/normal_dataset.csv'.format(data_dir))

#
# Number of TCP packets
#
column = 'pkt_num'
plot_features(attack_data[column], 
              normal_data[column], 
              slide=5, start_obs=0, N=100, 
              title='TCP packets', ylabel='Number of packets', dir=plots_dir)

#
# Number of TCP SYN packets
#
column = 'syn_num'
plot_features(attack_data[column], 
              normal_data[column], 
              slide=5, start_obs=0, N=100, 
              title='SYN packets', ylabel='Number of packets', dir=plots_dir)

#
# Entropy of destination IP
#
column = 'ip_ent'
plot_features(attack_data[column], 
              normal_data[column], 
              slide=5, start_obs=0, N=100, 
              title='Normalized Shannon entropy of destination IP', ylabel='Entropy', dir=plots_dir)

#
# Mean packet length
#
column = 'mu_len'
plot_features(attack_data[column], 
              normal_data[column], 
              slide=5, start_obs=0, N=100, 
              title='Mean TCP packet length', ylabel='Packet length', dir=plots_dir)