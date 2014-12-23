__author__="paolo.latella@interact.it"
__date__ ="$19-ago-2013 15.06.12$"

#Quota in GB dello spazio AWS (default pari a 20 TB)
LIMITE = 20000

total_size = 0
total_volumes_size = 0
total_volumes_available_size = 0
total_snapshots_size = 0

warning = 75 #Percentuale di warning
soglia = (LIMITE * warning)/100

import boto.ec2
import sys
import time
connection = boto.ec2.connect_to_region("eu-west-1")

#Check volumi
volumes_list = connection.get_all_volumes()
total_volumes = len(volumes_list)
for volume in volumes_list:
     total_volumes_size = total_volumes_size + volume.size
     if volume.volume_state() == 'available':
        total_volumes_available_size = total_volumes_available_size + volume.size

#Check snapshots
snapshots_list = connection.get_all_snapshots(owner='847091595066')
total_snapshots = len(snapshots_list)
for snapshot in snapshots_list:
    total_snapshots_size = total_snapshots_size + snapshot.volume_size
total_size = total_snapshots_size + total_volumes_size
today = time.time()
print (today)
if total_size < soglia:
    print "[%lu] PROCESS_SERVICE_CHECK_RESULT;ec2-prd-interact-manager;AWS Storage Usage;0;Total Size:%s Total Volumes:%s Total Snapshots:%s Total volumes size:%s Total Snapshots size:%s" % (today, total_size, total_volumes, total_snapshots, total_volumes_size, total_snapshots_size)
    sys.exit(0)
else:
    print "[%lu] PROCESS_SERVICE_CHECK_RESULT;ec2-prd-interact-manager;AWS Storage Usage;2;Total Size:%s Total Volumes:%s Total Snapshots:%s Total volumes size:%s Total Snapshots size:%s" % (today, total_size, total_volumes, total_snapshots, total_volumes_size, total_snapshots_size)
    sys.exit(1)
