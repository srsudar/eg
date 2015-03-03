# top

show and update system information

    top


order by CPU usage and limit to 10 processes

    top -o cpu -n 10


order first by memory and then by CPU usage

    top -o mem -O cpu


accumulate statistics since top was launched

    top -a


only show process with PID 333 and 444

    top -pid 333


# Basic Usage

Display system information:

    top


