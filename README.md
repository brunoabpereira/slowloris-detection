# slowloris-detection

# Apache 2.4.38 (debian)
## default config (/etc/apache2/apache2.conf): 
```
Timeout 300
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 15         # default Apache 2.0
```

# datasets

Packet captures for two scenarios: attack and normal.

## attack

1 machine attacking 2 hosts for 30 mins. The attack performed is [slowloris](https://github.com/gkbrk/slowloris):

```
slowloris host -ua -s x --sleeptime y
```

- host = random host (tmp.tpr.local or tmp2.tpr.local)
- sockets = random x in 150-250
- sleeptime = random y in [4,9,14], must be less than Apache's KeepAliveTimeout (15 seconds in this case)
- attack duration = 2-7 mins random interval

## normal
1 machine browsing for 15 mins:

- Youtube
- Reddit
- Facebook
- Wikipedia
- Google images
- tmp.tpr.local
- tmp2.tpr.local

# feature extraction

filter by:
- tcp packets
- egressing packets
- source ip

for each source ip (host):
- get observation windows (sequential or sliding)

for each observation window:
- number of TCP packets
- number of TCP SYN packets
- mean TCP packet length
- std TCP packet length
- normalized shannon entropy of TCP destination IP
- normalized shannon entropy of TCP destination port
- total silence
- average of silence
- std of silence