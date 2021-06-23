from scapy.all import *
import numpy as np
import pandas as pd

def pkt_samples(packets, sample_interval=1, flag=None):
    """ arrange packets in 1 seconds intervals
        Args:
            packets:
            sample_interval:
            flag: SYN = 2
    """
    start_time = np.floor(packets[0].time)
    end_time = np.ceil(packets[-1].time)
    
    packet_samples = []
    
    num_packets = len(packets)
    packet_idx = 0
    for interval_start in np.arange(start_time, end_time, sample_interval):
        sample = []
        while packet_idx < num_packets and packets[packet_idx].time < int(interval_start + sample_interval):
            pkt = packets[packet_idx]
            if flag and pkt[TCP].flags.value == flag:
                sample.append(pkt)
            else:
                sample.append(pkt)
            packet_idx +=1
        packet_samples.append(sample)
            
    return packet_samples

def seqObsWindow(data, lengthObsWindow):
    nSamples = len(data)
    obsWindows = []
    for s in np.arange(0,nSamples,lengthObsWindow):
        subdata=data[s:s+lengthObsWindow]
        if len(subdata) == lengthObsWindow:
            obsWindows.append(subdata)
    return obsWindows

def slidingObsWindow(data, lengthObsWindow, slidingValue):
    nSamples = len(data)
    obsWindows = []
    for s in np.arange(0,nSamples,slidingValue):
        subdata=data[s:s+lengthObsWindow]
        if len(subdata) == lengthObsWindow:
            obsWindows.append(subdata)
    return obsWindows

def num_tcp_pkts(obs_window):
    num = 0
    for sample in obs_window:
        num += len(sample)
    return num

def packet_length(obs_window):
    len_list = []
    for sample in obs_window:
        for pkt in sample:
            len_list.append(pkt[IP].len)
    return (np.mean(len_list),np.std(len_list)) if len_list else (0,0)

def ip_port_hist(obs_window):
    ip_hist = dict()
    port_hist = dict()
    for sample in obs_window:
        for pkt in sample:
            dst_ip = pkt[IP].dst
            dst_port = pkt[TCP].dport
            if dst_ip not in ip_hist.keys():
                ip_hist[dst_ip] = 0
            ip_hist[dst_ip] += 1
            if dst_port not in port_hist.keys():
                port_hist[dst_port] = 0
            port_hist[dst_port] += 1
    return ip_hist, port_hist

def norm_entropy(hist, total_occurrences):
    num_vals = len(hist.keys())
    h = 0
    for val in hist.keys():
        # calc probs
        p_val = float(hist[val])/total_occurrences
        # calc normalized entropy
        norm_factor = np.log2(num_vals) if num_vals != 1 else 1
        h += (p_val * np.log2(p_val)) / norm_factor
    return abs(h)

def extratctSilenceActivity(data,threshold=0):
    if(data[0]<=threshold):
        s=[1]
        a=[]
    else:
        s=[]
        a=[1]
    for i in range(1,len(data)):
        if(data[i-1]>threshold and data[i]<=threshold):
            s.append(1)
        elif(data[i-1]<=threshold and data[i]>threshold):
            a.append(1)
        elif (data[i-1]<=threshold and data[i]<=threshold):
            s[-1]+=1
        else:
            a[-1]+=1
    return(s,a)