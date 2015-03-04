# eg

> Example usage for commands at the command line.

## Overview

`eg` provides examples of common uses of command line tools.

Man pages are great. How does `find` work, again? `man find` will tell you, if
you have 30 minutes. How do you use `find` to find only directories? How about
bigger than 500kb and no more than two levels deep? Pore through the man pages
looking for the right flags, be frustrated, eventually turn to the internet for
an example.

And what about using `tar`? Even with the man pages `tar` is [famously
inscrutable without the internet](http://xkcd.com/1168/).

No more! `eg tar` and save the world.

`eg` will give you useful examples right at the command line. Think of it as a
companion tool for `man`.

> `eg` comes from _exempli gratia_, and is pronounced like the letters: "ee
gee".


## Installation

Clone the repo and create a symlink to `eg.py`. Make sure the location you
choose for the symlink is on your path:

```shell
git clone https://github.com/srsudar/eg ./
link -s ./eg/eg.py /usr/local/bin/eg
```

`eg` is in beta and doesn't ship with a binary. You'll have to have python
2.x installed on your machine. Dependencies are very modest and should not
require you to install anything (other than Nose if you want to run the tests).
If you find otherwise, open an issue.


## Usage

`eg <program>`

`eg` takes an argument that is the name of a program for which it contains
examples.

`eg find` will provide examples for the `find` command.

`eg --list` will show all the commands for which `eg` has examples.


## How it Works

Files full of examples live in `examples/`. A naming convention is followed
such that the file is the name of the tool with `.md`. E.g. the examples for
`find` are in `find.md`.

`eg find` will pipe the contents of `find.md` through the `less` (although it
tries to respect the `PAGER` environment variable.


## Configuration and Extension

`eg` works out of the box, no configuration required.

If you want to get fancy, however, `eg` can be fancy.

For example, maybe a team member always sends you bzipped tarballs and you can
never remember the flag for bzipping--why can't that guy just use gzip
like everybody else? You can create an example for untarring and unzipping
bzipped tarballs, stick it in a file called `tar.md`, and tell `eg` where to
find it.

The way to think about what `eg` does is just that it takes a program name, for
example `find`, and looks for two files named `find.md` in the default
directory and a custom directory. If it finds them, it pipes them through
`less`, with the custom file at the top. Easy.

The default and custom directories can be specified at the command line like
so: 

```shell
eg --examples-dir='the/default/dir' --custom-dir='my/fancy/dir' find
```

Instead of doing this every time, you can define a configuration file. By
default it is expected to live in `~/.egrc`. It must begin with a section
called `eg-config` and can contain two keys: `custom-dir` and `examples-dir`.
Here is an example of a valid config file:

    [eg-config]
    examples-dir = ~/examples-dir
    custom-dir = ~/my/fancy/custom/dir

Although by default the file is looked for at `~/.egrc`, you can also specify a
different location at the command line like so: 

```shell
eg --config-file=myfile find
```


## Format and Content of Examples

Example documents are written in [markdown](http://daringfireball.net/projects/markdown/syntax).
Documents in markdown are easily read at the command line as well as online.
They all follow the same basic format.

This section explains the format so that you better understand how to quickly
grok the examples.

Contributors should also pay close attention to these guidelines to keep
examples consistent.


## Overview

Anything indented four spaces or surrounded by backticks \`like this\` are
meant to be input or output at the command line. A single line indented four
spaces is a user-entered command. If a block is indented four spaces, only the
lines beginning with `$` are user-entered--anything else is output.


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

This section shouldn't show output and should not include the `$` to indicate
that we are at the command line.

**This section should be a quick glance for users that know what the tool does,
know a basic usage is what they are trying to do, and are just looking for a
reminder.**


### Basic Usage

Next a Basic Usage section explains the most basic usage without using real
file names. This section gives users that might not know the usual syntax a
more abstract example than the first section. It is intended to provide a more
useful explanation than the first entry in the man page, which typically shows
all possible flags and arguments in a way that is not immediately obvious to
new users of the command. The SYNOPSIS section of the man page for `cp`, for
example, shows:

    cp [-R [-H | -L | -P]] [-fi | -n] [-apvX] source_file ... target_directory

**The Basic Usage is intended to provide less verbose, more immediately
practical versions of the man page's SYNOPSIS section.**

Commands and flags that will affect the behavior are shown as would be entered
in the command line, while user-entered filenames and arguments that do not
alter the command's behaviors are shown in `< >`. Examples in the Basic Usage
section for the `cp` command, for instance, might be:

    cp -R <original_directory> <copied_directory>

In this command the `cp -R` indicate the command and behavior and thus are not
given in `< >`. Case-dependent components of the command, in this case the
directory to be copied and the name of the copy, are surrounded with `< >`.
Each is wrapped in separate `< >` to make clear that it is in fact two
distinct arguments.

### Additional Sections

Subsequent subsections can be added for common uses of the tools, as
appropriate.

### Formatting

Although markdown is readable, it can still be tricky without syntax
highlighting. We use spacing to help the eye.

1. All code snippets are followed by at two blank lines, unless overruled by 2.

2. Each line beginning a section (i.e. the first character on the line is `#`)
should be preceded by exactly three lines.

3. Files should end with two blank lines.

4. Lines should not exceed 80 characters, unless to accommodate a necessarily
   long command or long output.


## Contributing

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


### Building and Running Tests

`eg` depends only on standard libraries and Python 2.x, so building should be a
simple matter of cloning the repo and running the executable `eg/eg.py`.

`eg` uses Nose for testing, so you'll have to have Nose installed to run tests.
Once you have Nose, run `nosetests` from **the root directory of the repo**.

Tests should always be expected to pass. If they fail, please open an issue,
even if only so that we can better elucidate `eg`'s dependencies.


## Grace Hopper Approves

Alias `eg` to `woman` for something that is like `man` but a little more
practical:

```shell
$ alias woman=eg
$ man find
$ woman find
```

## TODO

The following commands still need entries. The list is incomplete. Feel free to
suggest more that are missing, and feel even freer to submit examples for them.

* gcc
* ar
