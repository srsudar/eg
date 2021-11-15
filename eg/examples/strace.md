# strace

trace syscalls of a command and follow child pids

    strace -f ls



# Basic Usage

Trace syscalls of a command:

    strace <command>


See the syscalls of an already-running process:

    strace -p <pid>


See only `network` type syscalls (and/or `file`,`stat`, `process`, or any
specific syscall, comma separated):

    strace -e trace=%network <command>


See only system calls accessing a specific path:

    strace -P <path> <command>


Increase default preview string size to 256:

    strace -s 256 <command>


Show timestamps:

    strace -t <command>


Show time spent in syscalls:

    strace -T <command>


Only show a summary of syscalls (equivalent to `-c`):

    strace --summary-only <command>


Attach to a running process with the id of 1234 (`-p 1234`), follow child
processes (`-f`), print 256 string characters (`-s 256`), and show the time
spent in calls (`-T`):

    $ strace -f -s 256 -p <pid> -T


Run the command `echo "hi"`, follow child processes (`-f`), print 256 string
characters (`-s 256`), and show the time spent in calls (`-T`):

    $ strace -f -s 256 -T echo "hi"
    execve("/usr/bin/echo", ["echo", "hi"], 0x7fff519c2db8 /* 57 vars */) = 0 <0.003416>
    brk(NULL)                               = 0x561667bc7000 <0.000013>
    arch_prctl(0x3001 /* ARCH_??? */, 0x7ffd1ca4cec0) = -1 EINVAL (Invalid argument) <0.000012>
    access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory) <0.000023>
    openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3 <0.000046>
    fstat(3, {st_mode=S_IFREG|0644, st_size=237628, ...}) = 0 <0.000015>
    mmap(NULL, 237628, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f42a29f9000 <0.000017>
    close(3)                                = 0 <0.000012>
    [...]
