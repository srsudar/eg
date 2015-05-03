# renice

change the priority of a running process 

    renice -n -15 -p 2230


change priorities of all the process owned by user foo

    renice -n 5 -u foo


# Basic Usage

alter priority of a running process

    renice -n <priority> <processID>
    

niceness values range from -20 (highest priority) to 19 (lowest priority)
