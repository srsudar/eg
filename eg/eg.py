#!/usr/bin/python
import sys
import eg_util


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 1:
        eg_util.show_usage()
    else:
        eg_util.handle_program(args[1])
