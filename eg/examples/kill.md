# kill

politely kill process with id 25371

    kill 25371


send non-catchable, non-ignorable kill to process with id 22204

    kill -9 22204


kill background job with id 1

    kill %1


kill most recent background job

    kill %%


interrupt process 25929

    kill -s INT 25929



# Basic Usage

Stop a target process using a polite `TERM` signal that allows for resource
cleanup:

    kill <target>


Stop a target processing impolitely using the `KILL` signal:

    kill -9 <target>



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
be specified with the `-s` flag and their name. Signals can also be referred to
by their numeric code. This will send (`-s`) an interrupt (`INT`) signal to
process 26089:

    kill -s INT 26089


The `INT` signal is code `2`, so this command is equivalent to the above:

    kill -2 26089


The strongest signal is `KILL`, which has code `9`. This is non-catchable and
non-ignorable. It may fail for a zombie process or for under unusual
circumstances, but in the vast majority of cases it will force stop a process.
Processes won't be made aware of the kill request and won't have a chance to
clean up resources. This will send a `KILL` signal to (`-9`) process 22604:

    kill -9 22604


