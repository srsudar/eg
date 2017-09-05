
To create software RAID 1 from 2 partitions:
mdadm --create /dev/md3 --level=1 --raid-devices=2 /dev/sdc1 /dev/sdd1


