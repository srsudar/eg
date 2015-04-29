# df

In the following examples, `path` is optional.

Report filesystem disk space usage:

    df [path]


Include all filesystems:

    df -a


Show information in a human-readable format:

    df -h [path]
    
    
Report filesystem I-node space usage:

    df -i [path]


Limit listing to local filesystems:

    df -l [path]
    

Include filesystem type:

    df -T [path]
    
    
Show only certain filesystem type:

    df -t ext3
    
    
Exclude only certain filesystem type:

    df -x ext3

