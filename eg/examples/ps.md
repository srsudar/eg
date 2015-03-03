# ps

show all processes

    ps -ef


show process with id 37

    ps -p 37


show all processes with verbose information, including memory and CPU usage

    ps -ev


show processes belonging to user tyrion

    ps -u tyrion


show all threads

    ps -efM



# Basic Usage

Print processes for all users (`-e`) with a more detailed format (`-f`):

    ps -ef


`ps` can be more usable if you pipe it to `less`:

    ps -ef | less


Print all processes belonging to a specific user (`-u`):

    ps -u <username>



# Showing Detailed Information

Print verbose output for all (`-e`) processes with both memory and CPU usage
(`-v`), as well as the extended information provided by `-f`:

    ps -evf



# Finding by Process Name

This command uses `ps` to show all processes (`-e`) that Google Chrome
(`grep "Google Chrome"`) is running:

    ps -e | grep "Google Chrome"


