from utils import *
from scapy.all import *
import numpy as np
import pandas as pd

###
### filter packets by: 
###     - TCP protocol
###     - egressing from network
###     - src ip 
###

# file with raw packets
pcapfile = 'dataset/raw/attack_capture.pcap'
# filter packets egressing from network
network = '10.0.0.64/26'

# store packets by src ip
packets = dict()

def store_pkt(pkt):
    global packets
    ip = pkt[IP].src
    if ip not in packets.keys():
        packets[ip] = []
    packets[ip].append(pkt)

# filter syntax = https://biot.com/capstats/bpf.html
sniff(
    offline=pcapfile,
    store=False,
    filter="tcp and src net {net}".format(net=network),
    prn=store_pkt
)
all_hosts = packets.keys()

###
### sort packets by time
###

for host in all_hosts:
    packets[host] = sorted(packets[host], key=lambda pkt: pkt.time)

###
### get sliding observation windows for each host
###

T = 15      # observation window in seconds (10-30)
slide = 5

obs_windows = dict.fromkeys(all_hosts, 0)

for host in all_hosts:
    smps = samples(packets[host], sample_interval=1)
    obs_windows[host] = slidingObsWindow(smps, T, slide)

###
### extract features for observation windows
###

for host in all_hosts:
    windows = obs_windows[host]

    m = len(windows) # examples
    n = 1 + 8        # id + features
    data = np.zeros((m,n))

    for obs_id, obs_window in enumerate(windows):
        # number of TCP packets
        num_tcp_packets = num_tcp_pkts(obs_window)
        
        # mean and standard deviation TCP packet length
        mu_size, std_size = packet_length(obs_window)
        
        # normalized shannon entropy of TCP destination IP and port
        ip_hist, port_hist = ip_port_hist(obs_window)
        ip_ent = norm_entropy(ip_hist,num_tcp_packets)
        port_ent = norm_entropy(port_hist,num_tcp_packets)
        
        # silence
        act_data = [len(sample) for sample in obs_window]
        s, a = extratctSilenceActivity(act_data)
        # ratio
        total_silence = sum(s)/len(obs_window)
        # mean and std silence
        mean_silence = np.mean(s) if s else 0
        std_silence = np.std(s) if s else 0
        
        # feature vector
        x = np.array([
            obs_id,
            num_tcp_packets, 
            mu_size, 
            std_size, 
            ip_ent, 
            port_ent, 
            total_silence, 
            mean_silence, 
            std_silence
        ])
        
        # add to dataset
        data[obs_id,:] = x

    ###
    ### save dataset
    ###

    df = pd.DataFrame(
        data=data[:,1:],
        index=data[:,0],
        columns=["pkt_num", "mu_len", "std_len", "ip_ent", "port_ent", "silence_ratio", "mu_silence", "std_silence"], 
    )

    print(df.describe())

    df.to_csv('dataset_{}.csv'.format(host))
