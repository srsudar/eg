# renice

change the priority of a running process with id 2230

    renice -n -15 -p 2230


change priorities of all the process owned by user foo

    renice -n 5 -u foo



# Basic Usage

Alter priority of a running process:

    renice -n <priority> -p <processID>


Niceness values range from -20 (highest priority) to 19 (lowest priority).


