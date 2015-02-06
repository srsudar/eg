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
Documents in markdown are easily read at the command line as well as online.

### Name of the Command

The first section heading should be simply the name of the tool. It should be
followed by the most rudimentary examples. Users that are familiar with the
command but just forget the precise syntax should be able to see what they need
without scrolling. Example commands should be as real-world as possible, with
file names and arguments as illustrative as possible. Examples for the `cp`
command, for instance, might be:

    cp original.txt copy.txt

Here the `.txt` extensions indicate that these are file names, while the names
themselves make clear which is the already existing file and which will be the
newly created copy.

### Basic Usage

Next a Basic Usage section explains the most basic usage without using real
file names. This section gives users that might not know the usual syntax a
more abstract example than the first section. It is intended to provide a more
useful explanation than the first entry in the man page, which typically shows
all possible flags and arguments in a way that is not immediately obvious to
new users of the command. The SYNOPSIS section of the man page for `cp`, for
example, shows:

    cp [-R [-H | -L | -P]] [-fi | -n] [-apvX] source_file ... target_directory

The Basic Usage is intended to provide a less verbose, more immediately
practical version of the man page's SYNOPSIS section.

Commands and flags that will affect the behavior are shown as would be entered
in the command line, while user-entered filenames and arguments that alter the
what rather than the how are shown in `< >`. Examples in the Basic Usage
section for the `cp` command, for instance, might be:

    cp -R <original_directory> <copied_directory>

In this command the `cp -R` indicate the command and behavior and thus are not
given in `< >`. User-entered components of the command, in this case the
directory to be copied and the name of the copy, are surrounded with `< >`.
Each is wrapped in separate `< >` to make clear that this is in fact two
distinct arguments.

### Additional Sections

Subsequent subsections can be added for common uses of the tools, as
appropriate and as necessary.

## Pagers

`eg` tries to use your preferred pager by looking at the `$PAGER` environment
variable. If `$PAGER` is not set, it defaults to `less`. If your pager does not
support jumping to a line number `eg` will try not to fail.

## Contributor Guidelines

Additions of new tools and new or more useful examples are welcome. `eg` should
be something that people want to have on their machines. If it has a man page,
it should be included in `eg`.

Please read the Format of Examples section and review existing example files to
get a feel for how `eg` pages should be structured.

If you find yourself turning to the internet for the same command again and
again, consider adding it to the examples.

`eg` examples do not intend to replace man pages! `man` is useful in its own
right. `eg` should provide quick examples in practice. Do not list all the
flags for the sake of listing them. Assume that users will have `man`
available.

## Grace Hopper Approves

Alias `eg` to `woman` for something that is like `man` but is a little more
practical:

```shell
$ alias woman=eg
$ man find
$ woman find
```

## TODO

The following commands still need entries:

* locate
* top
* kill
* scp
* gcc
* ar
* sort
* cut
* more
