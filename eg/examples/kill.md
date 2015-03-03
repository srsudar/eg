# kill

kill process 25371

    kill 25371


kill background job with id 1

    kill %1


kill most recent background job

    kill %%


interrupt process 25929

    kill -s INT 25929



# Basic Usage

Stop a target process:

    kill <target>



# Specifying Targets

By default `kill` expects a process id. This will kill the process with PID
25371:

    kill 25371


Background jobs can be referred to by with a preceding `%`. This will kill the
background job 1 (`%1`):

    $ jobs
    [1]  + suspended  node
    $ kill %1
    [1]  + 25854 exit 143   node
    $ jobs
    $



# Sending Other Signals

`kill` sends a software termination `TERM` signal by default. Other signals can
be specified with the `-s` flag. This will send (`-s`) and interrupt (`INT`)
signal to process 26089:

    kill -s INT 26089


