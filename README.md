# eg

> Example usages for command line tools.

## Overview

`eg` provides examples of common uses of command line tools.

Man pages are great. How does `find` work, again? `man find` will tell you. But
all too often you need a little bit more. How do you use `find` to find a file
in a directory? Pore through the man pages looking for the right flags, be
frustrated, eventually turn to the internet for an example.

No more!

`eg` will give you useful examples right at the command line. Think of it as a
companion tool for `man`.

> `eg` comes from _exempli gratia_, and is pronounced like the letters: "ee
gee".

## Usage

`eg <tool> <subsection>`

`eg` takes an argument that is the name of a program for which it contains
examples.

`eg find` will provide examples for the `find` command.

A second argument will attempt to jump to a relevant subsection on the page.
`eg find directory` will jump to the subsection for finding directories using
`find`.

## How it Works

Files full of examples live in `examples/`. A naming convention is followed
such that the file is the name of the tool with `.txt`. E.g. the example for
`find` is in `find.txt`.

`eg find` will pipe the contents of `find.txt` through the pager (see below for
how the pager is resolved).

Subsections are resolved using by looking for a subsection or alias for a
subsection and finding the line number for that section. Output is then piped
through pager starting at that subsection.

## Pagers

`eg` tries to use your preferred pager by looking at the `$PAGER` environment
variable. If `$PAGER` is not set, it defaults to `less`. If your pager does not
support jumping to a line number `eg` will try not to fail.

## Example Format

The example files ust follow a strict format in order to be parsed by `eg`.
