import os
import re
import pickle
import pandas as pd
from models import *

def predict(data_file, host, N=4):
    # load models and scaler
    models_dir = 'models'
    svc = pickle.load(open('{}/svm.pkl'.format(models_dir), 'rb'))
    logreg = pickle.load(open('{}/logreg.pkl'.format(models_dir), 'rb'))
    scaler = pickle.load(open('{}/scaler.pkl'.format(models_dir), 'rb'))
    # load data
    data = pd.read_csv(data_file)
    # get features
    X = data.iloc[:, 1:10].copy()
    # normalize
    X_norm, _ = normalize(X, scaler=scaler)
    # predict
    svc_y_pred = svc.predict(X_norm)
    logreg_y_pred = svc.predict(X_norm)
    # see N sequential observation windows
    ensemble = list(svc_y_pred & logreg_y_pred)
    detected_obs_ids= []
    for obs_id, pred in enumerate(ensemble):
        if sum(ensemble[obs_id:obs_id+N]) == N:
            detected_obs_ids.append(obs_id)
    return detected_obs_ids

# parse pcap
pcap_file = 'tpr-proj/project-files/captures/demo.pcap'
os.system('python extract_features.py {} > /dev/null'.format(pcap_file))

# get datasets for each host
files = [f for f in os.listdir('.') if re.match(r"dataset_[0-9]+.[0-9].[0-9].[0-9].*\.csv", f)]

# classify each host
for f in files:
    host = re.findall(r'[0-9]+.[0-9]+.[0-9]+.[0-9]+',f)[0]
    print('host:\t{}'.format(host))
    res = []
    try:
        res = predict(f, host)
    except Exception:
        pass
    print('class:\t{}'.format('attack' if res else 'normal'))
    print('ids of detected observation windows:')
    print(res)
