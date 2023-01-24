Running scaper.py to get edge weights from gMaps into edge_weights.txt

To run for paths starting at nodes 5-10:
`nohup python3 scraper.py 5 10 &`

List background processes running scraper:
ps aux | grep scraper.py

IP Address of openstack instance:
134.117.26.79

How to ssh:
ssh student@134.117.26.79 -A

How to transfer files:
Linux -> local
scp -r "student@134.117.26.79:~/Documents/dynamic-fleet-routing/data" "C:/Users/Youss/OneDrive/Documents/courses/Honours Project/dynamic-fleet-routing/transferred_data/backup_dec3"

local -> Linux
scp -r "C:/Users/Youss/OneDrive/Documents/courses/Honours Project/dynamic-fleet-routing/" "student@134.117.26.79:~/Documents/dynamic-fleet-routing/"


WHEN OPENSTACK IS SLOW:
Found many instances of firefox driver still alive (there should only be 1 result here):
ps aux | grep /snap/firefox/
To cleanup:
pkill -f /snap/firefox

This is processes not being terminated, presumably because I don't call driver.quit() when the process is forcefully terminated

Files that are being cached when they shouldnt:
sudo du -am /tmp | sort -n -r | head -n 20
To cleanup:
sudo rm -r /tmp/snap.firefox/

PROGRESS:
Nov 25 (midnight): 110113 total
Nov 27 (midnight): 252376 total
Nov 29 (8pm): 388066 total
Nov 30 (7pm): 448329 total
Dec 05 (4pm): 709922 total
Dec 06 (6pm): 791146 total
Dec 08 (9pm): 937470 total
approx ~65000 per day... this will take a while
Dec 09 (6pm): 992287 total
Dec 11 (4pm): 1116401 total
Dec 14 (8pm): 1315274 total
Dec 16 (1pm): 1420392 total
Dec 17 (11pm): 1525509 total
Dec 20 (3pm): 1705636 total
Dec 20 (7:30pm): 1724003 total
Dec 28 (11:30pm): 2263466 total
Dec 30 (11pm): 2412946 total
Dec 31 (1pm): 2419771 total
Jan 02 (8pm): 2618879 total
Jan 04 (6pm): 2747338 total
Jan 06 (2pm): 2848229 total
Jan 06 (11pm): 2852113 total
Jan 07 (11pm): 2910145 total
Jan 08 (5pm): 2976375 total
Jan 10 (1pm): 3106048 total
After removing -1 vals:
Jan 10 (3pm): 2846104 total
Jan 11 (9:30pm): 2930305 total
Jan 12 (10pm): 2979612 total
Jan 15 (6pm): 3194935 total
Jan 17 (12pm): 3294390 total
Jan 19 (9pm): 3440912 total
Jan 22 (2pm): 3647179 total
Jan 23 (9:30pm): 3741135 total