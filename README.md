# eg

> Example usages for command line tools.

## Overview

`eg` provides examples of common uses of command line tools.

Man pages are great. How does `find` work, again? `man find` will tell you. But
all too often you need a little bit more. How do you use `find` to find only
directories? How about bigger than 500kb and no more than two levels deep? Pore
through the man pages looking for the right flags, be frustrated, eventually
turn to the internet for an example.

No more!

`eg` will give you useful examples right at the command line. Think of it as a
companion tool for `man`.

> `eg` comes from _exempli gratia_, and is pronounced like the letters: "ee
gee".

## Usage

`eg <tool>`

`eg` takes an argument that is the name of a program for which it contains
examples.

`eg find` will provide examples for the `find` command.

## How it Works

Files full of examples live in `examples/`. A naming convention is followed
such that the file is the name of the tool with `.md`. E.g. the example for
`find` is in `find.md`.

`eg find` will pipe the contents of `find.md` through the pager (see below for
how the pager is resolved).

## Format and Content of Examples

Example documents are written in [markdown](http://daringfireball.net/projects/markdown/syntax).
This is due to the fact that markdown is easily readable by both humans and
machines. Documents in markdown are easily read at the command line as well as
online.

The first section should be simply the name of the tool. It should be followed
by the most rudimentary examples. Users that are familiar with the command but
just forget the precise syntax should be able to see what they need without
scrolling.

A Basic Usage section explains the most basic usage in slightly more detail.

Subsequent subsections can be added for common uses of the tools, as
appropriate and as necessary.

## Pagers

`eg` tries to use your preferred pager by looking at the `$PAGER` environment
variable. If `$PAGER` is not set, it defaults to `less`. If your pager does not
support jumping to a line number `eg` will try not to fail.

## Contributing and Guidelines

Additions of new tools and new or more useful examples are welcome. `eg` should
be something that people want to have on their machines. If it has a man page,
it should be included in `eg`.

If you find yourself turning to the internet for the same command again and
again, consider adding it to the examples.

`eg` examples do not intend to replace man pages! `man` is useful in its own
right. `eg` should provide quick examples in practice. Do not list all the
flags for the sake of listing them. Assume that users will have `man`
available.

## For the Ladies

Alias `eg` to `woman` for something that is like `man` but is a little more
practical:

```shell
$ alias woman=eg
$ man find
$ woman find
```
