
### resize -- GROW
# stop the VM if it's running
lvresize -L +12GB  /dev/storage/test1-disk
e2fsck -f /dev/storage/test1-disk
resize2fs -p /dev/storage/test1-disk
# start the VM 

### resize -- REDUCE
# stop the VM if it's running
e2fsck -f /dev/polar/root
resize2fs -p /dev/polar/root 80G # new smaller size
lvreduce -L 100G /dev/polar/root # about 10% more than resize2fs size!!!
resize2fs -p /dev/polar/root  # second time, grow to partition size
e2fsck -f /dev/polar/root # just to be sure
# start the VM

