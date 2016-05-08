# brew

see all homebrew-installed packages

    brew list


search for an installable package containing the string ack

    brew search ack


install the ack package

    brew install ack


upgrade an installed node to the most recent version

    brew upgrade node


see all installed versions of node

    brew info node


use the installed version 0.10.20 of node instead of the current version

    brew switch node 0.10.20



# Basic Usage

`brew` is the command for Homebrew, a package manager for OSX. It is most
commonly used to install a package or utility:

    brew install <package>


Search for a formula containing a string:

    brew search <string>



# Installing Things

The people maintaining Homebrew curate a list of software that can be installed
using `brew`. The instructions for installing a particular package are called a
formula. Before installing things, it is good practice to make sure you have
the most up to date version of all formulae by running `update`:

    brew update


Once you are dealing with the most recent formulae, install things by giving
`brew` the `install` command and a package name. To see if `node` can be
installed using `brew`, first search all formulae to see if Homebrew offers an
install of `node`:

    brew search node


Homebrew will print all matching formulae. `node` is among them, so install it:

    brew install node


After a package is installed, watch the output for any printed caveats. These
are formula-dependent. Homebrew is good about taking care of things for you,
but sometimes you'll still have to handle something yourself.



## What Does Install Do?

`brew install` does two things. First, it somehow gets an executable onto your
machine. It might download an executable directly (which is referred to as a
"bottle"), or it might build from source.  Second, it adds symlinks to these
executables so that they will be on your path.

By default, `brew` installs things into your Cellar. The location of your
Cellar can be found by:

    brew --cellar


Inside your Cellar, programs are stored according to their package name and
version. This will show where Homebrew installs `node` inside your Cellar:

    $ brew --cellar node
    /usr/local/Cellar/node


Inside that directory are other directories with all the versions of the `node`
package installed on your machine:

    $ ls /usr/local/Cellar/node
    0.10.20/  0.10.36/  0.12.2_1/


After the executable is available, it lives in the Cellar in one of the above
directories. Homebrew then creates symlinks to the executable as well as other
relevant files like man pages in a place that is on your path. Exactly where
these symlinks live varies depending on the formula, but they usually live at
`$(brew --prefix)/bin`.



# Linking

A keg can be installed without being symlinked on your path. This gives you
more flexibility, as you can essentially deactivate a formula without having to
manually curate your path or delete the installed the executable.

This will remove the symlinks to `node`:

    brew unlink node


An installed, unlinked formula is referred to as "keg only". To create symlinks
to the formula, run the `link` command. This will create symlinks to `node`:

    brew link node



# Taps

A tap is a list of formulae that extends the default list provided by Homebrew.
All taps are described as a two part name containing a single slash. For
example, `homebrew/versions` is a list of formulae that allow installation of
specific versions of software.

This naming convention refers to a repository on Github and is of the format:
`<username>/hombrew-<name>`. `homebrew/versions` is therefore shorthand for
`homebrew/homebrew-versions` and the source for the tap can be found on Github
at `https://github.com/homebrew/homebrew-versions`.

See your active taps:

    brew tap


Activate the `homebrew/versions` tap:

    brew tap homebrew/versions


Deactivate the `homebrew/versions` tap:

    brew untap homebrew/versions



# Versions

Kegs for multiple versions of a single formula can exist simultaneously in the
Cellar.

See all installed versions of the node formula:

    brew info node


Switch to a different installed version of a node:

    brew switch node 0.12.20


If you want to install an older version of a tool you'll likely need the
`homebrew/versions` tap. If you have previously installed a newer version of
the tool, you'll need to first unlink that version. This sequence of commands
assumes that you have installed `node` greater than version `010` but want to
install `010`:

    $ brew tap homebrew/versions
    $ brew unlink node
    $ brew search node
    homebrew/versions/node010    homebrew/versions/node08   nodebrew
    hombrew/versions/node04      leafnode                   modenv
    homebrew/versions/node06     node
    $ brew install homebrew/versions/node010



# Casks

A Cask is a `.app` style application that can be installed using Homebrew. This
is an alternative to downloading a `.dmg` file and dragging an icon into your
`Applications/` directory.

Install the `cask` command:

    brew install caskroom/cask/brew-cask


Search for casks containing the string `chrome`:

    brew cask search chrome


Install the `google-chrome` cask:

    brew cask install google-chrome


Print the `cask` help:

    brew cask help



# Terminology

Homebrew's strict adherence to beer-related terms can lead to some confusion.



## Formula

The definition of a package. This is a ruby file that lives at
`/usr/local/Libary/Formula`.

See the formula for `node`:

    less /usr/local/Library/Formula/node.rb



## Keg

The installation prefix of a formula. This can also be thought of as a
particular version of a package. A `node` keg for version `0.10.20` might be
`/usr/local/Cellar/node/0.10.20`.

This indicates there are three `node` kegs on the machine:

    $ ls /usr/local/Cellar/node
    0.10.20/  0.10.36/  0.12.2_1/



## Cellar

Where kegs are installed. Find the location with:

    brew --cellar



## Bottle

A binary keg that can be unpacked. These frequently end in `.tar.gz` and are
referred to as "poured from bottle" or "bottled" when running `brew info` about
a particular package:

    brew info node



## Tap

A list of additional optional formulae that can be used to extend Homebrew's
default list.



## Cask

A `.app` style program that can be installed using Homebrew.


