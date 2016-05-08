# git

pull changes into the local repository from the master branch at origin

    git pull origin master


change the previous commit

    git commit --amend


show all branches with the current indicated by an asterisk

    git branch


discard all changes and return to the last commit

    git reset --hard HEAD


unstage changes to foo.py that have been added

    git reset path/to/foo.py


show the contents of bar.java at revision e8883f

    git show e8883f:path/to/bar.java


show diff of baz.go between commits affbc and 6d680

    git diff affbc 6d680 -- path/to/baz.go


push all branches to the origin

    git push origin --all


show all remotes

    git remote -v


switch to the branch named bugfix

    git checkout bugfix


view the commit history

    git log



# Basic Usage

Execute a command:

    git <command>


View the manpages for a command:

    git help <command>


`git` is complex. It takes a number of verb-like commands that control `git`
repositories and files. Examples are shown in sections for commands and for
specific scenarios.



# add

`add` is used to make files and changes known to git.

Add `foo.py`:

    git add foo.py


Add all changes in the repository (`-A`), adding, modifying, and removing as
necessary:

    git add -A



# branch

Display all local branches with the current branch indicated by `*`:

    git branch


Display all remote (`-r`) branches:

    git branch -r


Display all (`-a`) branches, including remote branches:

    git branch -a


Delete (`-d`) the branch `dead`:

    git branch -d dead


Display verbose (`-v`) information local branches:

    git branch -v


Rename or move (`-m`) the current branch to be named `newname`:

    git branch -m newname


Rename or move (`-m`) the branch `oldname` to be named `newname`:

    git branch -m oldname newname



## Remote Tracking Branches

Tracking branches are those that are associated with a remote branch.
Differences between remote and local branches are shown with commands similar
to `git status` if the branch is tracking. A branch can be made to track a
particular remote using the `-u` or equivalent `--set-upstream-to` flag.

This command will cause the current branch to track the branch named `trackme`
at the remote named `origin`:

    git branch -u origin/trackme



# checkout

`checkout` is used to switch between branches.

Switch to the `master` branch:

    git checkout master


Create a new branch (`-b`) called `bugfix` and switch to it:

    git checkout -b bugfix



## Checking Out a Remote Branch

Checking out a remote branch is somewhat more complicated. First you must make
sure your local repository has downloaded the remote branch using `git fetch`.
At that point you can refer to the branch using `remote-name/branch-name`
syntax. A full sequence of commands to create a new branch named `rem-feature`
starting at a branch named `feature` from a remote named `origin` would be the
following:

    git fetch
    git checkout -b rem-feature origin/feature



# clean

`clean` is used to delete or purge untracked files and directories from your
repository.

Show but do not delete (`--dry-run`) files that would be deleted with by
calling the `clean` command:

    git clean -fd --dry-run


The force (`-f`) flag is used to force files to be deleted, while `-d`
indicates that directories should also be deleted. Note that this is
irreversible and should be used carefully, generally after seeing what would
happen by using the `--dry-run` flag:

    git clean -f -d



# clone

`clone` is used to copy a repository, especially from remote locations.

Clone the `eg` repository into the current directory:

    git clone git@github.com:srsudar/eg.git


Clone the `eg` repository into a new directory called `mydir`:

    git clone https://github.com/srsudar/eg.git mydir



# commit

Commit staged changes:

    git commit


Commit staged changes with the message "Update readme" (`-m "Update readme"`):

    git commit -m "Update readme"


Update the last commit (`--amend`). An editor will open giving you a chance to
edit the commit message. Staged changes will be combined with the changes of
the previous commit:

    git commit --amend



# config

`config` is used to display and set configuration variables. The `--global`
command is used to refer to global variables, while `--local` refers to
repository-specific versions. Without a final argument the variable is
displayed. Adding a final argument sets the value to that variable.

Display the global (`--global`) name of the user (`user.name`):

    git config --global user.name


Set the global (`--global`) name of the user (`user.name`) to Tyrion Lannister:

    git config --global user.name "Tyrion Lannister"


List (`--list`) all the global (`--global`) variables:

    git config --list --global



# diff

Show the differences in the working tree:

    git diff


Show the differences that have been added to the index via `git add`:

    git diff --cached


Show the differences in the file `baz.go` between commits `affbc` and `6d680`:

    git diff affbc 6d680 -- path/to/baz.go


Show the differences between `foo.txt` on commit `6d680` and `bar.txt` on
commit `af8cea`:

    git diff 6d680:path/to/foo.txt af8cea:path/to/bar.txt



# pull

`pull` is used to get and merge changes from a remote repository into a local
repository. It is roughly equivalent to running `git fetch` to get changes
followed by a `git merge` to merge those changes into the local commit history.

Get and merge changes from the `mybranch` branch at `origin` into the current
branch:

    git pull origin mybranch



# push

`push` is used to send changes to a remote location. In these examples the name
of the remote is always `origin`. This will push changes from the local
`master` branch to the `master` branch at `origin`:

    git push origin master


All branches can be pushed using the `--all` flag:

    git push --all origin


All tags can be pushed with the `--tags` flag:

    git push --tags origin


Changes can also be pushed from one branch to a branch with a different name.
This will push changes from the local `pushme` branch onto the remote `accept`
branch at `origin`:

    git push origin pushme:accept


Delete the remote branch `oldbranch` at the `origin`:

    git push --delete oldbranch


Push a local branch named `feature` to `origin` for the first time, setting up
tracking (`-u`) to ensure that differences are displayed with commands such as
`git status`:

    git push -u origin feature



# reset

`reset` moves the `HEAD` to a different commit, effectively reverting or
undoing commits. The commits themselves are left intact and can still be seen
with `git reflog`.

Restore the `HEAD` to the third most recent commit (`HEAD~2`), updating the
working tree to be identical to that commit (`--hard`):

    git reset --hard HEAD~2


Restore the `HEAD` to the third most recent commit (`HEAD~2`), leaving all
changes until that point staged and in the working tree (`--soft`):

    git reset --soft HEAD~2



# stash

`stash` is used to remove but save changes to the working directory. Stashes
are referred to using a `stash@{0}` syntax, where `stash@{0}` is the most
recent stash. Note that some shells, including zsh, require that the stash be
escaped to something like `stash\@\{0\}`.

Show all stashes:

    git stash list


Apply the most recent stash:

    git stash apply


Apply the second to most recent stash (`stash@{1}`):

    git stash apply stash@{1}


Delete (`drop`) the third most recent stash (`stash@{2}`):

    git stash drop stash@{2}



# submodule

Submodules are git repositories within a repository. They are frequently used
if you need to include code from another git repository within your own
repository.

Adding a submodule for the first time is simple using the `git submodule add`.
This example adds the `eg` repository as submodule in the current directory:

    git submodule add git@github.com:srsudar/eg.git


If you are cloning a repository that contains submodules you will need to issue
two commands to ensure that the submodules are up to date (`update`) and
initialized (`--init`). The `--recursive` flag is also used to ensure that
submodules at all levels are also initialized:

    git submodule update --init --recursive


Deleting submodules is not so simple. Recent versions of git have a `deinit`
command that can be passed to `submodule`, but unfortunately it leaves
references to the submodule in git config files. To completely delete a
submodule, run this sequence of commands to remove the submodule from most of
the config files (`deinit`), delete the local directory (`git rm`), and remove
the last references to the submodule (`rm -rf`). This assumes that a submodule
named `eg` is at the top level of the repository and that the current working
directory contains the `.git` directory:

    git submodule deinit eg
    git rm eg
    rm -rf .git/submodules/eg



# tag

`tag` is used to mark a specific commit. Unlike branches, tags do not move as
additional commits are made. Tags come in two flavors, annotated or basic. In
general annotated tags should be used, as they behave as full objects and can
contain useful information like a message and the name of the committer.

List (`--list`) all tags:

    git tag --list


When an annotated tag is created an editor opens to compose a tag message. This
command creates an annotated (`-a`) tag named `v1.0` pointing at the current
commit:

    git tag -a v1.0


Create an annotated (`-a`) tag named `v2.0` pointing at the commit with the
hash `u76a7s`:

    git tag -a v2.0 u76a6s


Delete (`-d`) the tag `badtag`:

    git tag -d badtag


Tags must be pushed separately, using the `--tags` flag to `push`:

    git push origin --tags



# Restoring Deleted Files

Files that have been committed can be restored even if they are later deleted.
This will restore a file that has been deleted locally but that was still
present on the `HEAD` commit:

    git checkout HEAD path/to/file.txt


This will checkout a file that was deleted an arbitrary number of commits
previously but that was present at the commit with the hash `ef8bca`:

    git checkout ef8bca path/to/file.txt


If the file was deleted at an unknown time, the commit when it was deleted must
first be found. The first command (`git rev-list`) will output the hash of a
single commit (`-n 1`), starting at the `HEAD`, that affected the file
`path/to/file.txt`. In this example the hash is `af8abe`. Since this commit
deleted the file, the parent comment (`af8abe^`) is the last commit where the
file was intact. `checkout` is used to restore the file at that revision:

    $ git rev-list -n 1 HEAD -- path/to/file.txt
    af8abe
    $ git checkout af8abe^ -- path/to/file.txt



# Combining Commits

There are several ways to combine or squash commits together. The option using
`git reset` is likely the simplest to understand, but each can be used to
accomplish the same thing.

All these examples show how to merge the previous three commits into a single
commit. It is assumed that there are no changes shown by `git status`. Recall
that `HEAD~3` refers to the fourth most recent commit, as `HEAD` is equivalent
to `HEAD~0`.



## Using reset

You can combine commits them simply by using `reset`. The first command will
move the `HEAD` to the fourth most recent commit (`HEAD~3`), leaving all the
changes that had been made intact (`--soft`). The working tree will not differ
from before the `git reset` command, and all the changes will be staged as if
they had been made at one time. `git commit` will commit these changes:

    git reset --soft HEAD~3
    git commit



## Using merge

Commits can also be combined using `merge` with the `--squash` command. This
command will merge the branch `squashme` into the current branch.  However, no
changes will be committed. Every change will be staged and ready to commit:

    git merge --squash mergeme


At this point, calling `git commit` will prepare a detailed commit message with
the hashes and messages of the previous commits.



## Using rebase

Finally, you can also accomplish this using the `rebase` command and the `-i`
or `--interactive` flag. This command will start an interactive (`-i`) rebase,
starting with all commits more recent than the commit pointed to by `HEAD~4`.
An editor will open with instructions of how to edit the rebase script. The
order is oldest to newest, the opposite of `git log`, and should be thought of
as being applied from top to bottom. As opened, saving the script will replay
the commit history without changing. Changing `pick` to `squash` will combine
the edits in the commit with the previous commit.

This will start an interactive (`-i`) rebase starting at the fifth to last
commit (`HEAD~4`):

    rebase -i HEAD~4


Editing the script to look like the following and saving will cause the commits
to be merged into the first commit. Note that the first command is a `pick`:

    pick hash1
    squash hash2
    squash hash3
    squash hash4



# Undoing a Commit

As with almost everything in git, there are several ways to undo a commit.

If you need to make a change to only the commit message, you can use the commit
command with the `--amend` flag:

    git commit --amend


If you want to completely throw away a commit, reverting to the state of the
previous commit, use `reset` with the `--hard` flag, which updates the working
tree to the state at the target commit. In this case we use `HEAD~1` to
indicate the second to last commit:

    git reset --hard HEAD~1


If you want to keep most of the changes in the last commit and just make a few
changes, use `reset` with the `--soft` flag, which keeps the changes staged:

    git reset --soft HEAD~1


Simply calling `reset` without a flag will keep the changes in the working tree
without staging them:

    git reset HEAD~1



# Discarding Unstaged Changes

If you have staged changes that you want to keep and want only to discard
unstaged changes, you can't use `reset`. Instead you need two commands. The
first will delete untracked files (`git clean -f`) and directories (`-d`). The
second will checkout the current branch's version of all files in the current
directory (`.`):

    git clean -d -f
    git checkout -- .


Keep in mind that you should consider running `git clean` with the `--dry-run`
flag first to make sure you don't irreversibly delete something you don't mean
to.



# Initializing a Repository

`git init` is used to create a repository. This sequence of commands is common
when initializing a repository for the first time. It initializes the
repository (`git init`), adds an existing file (`git add`), commits this change
(`git commit`), adds a remote repository (`git remote`), and pushes the
`master` branch to this repository (`git push`):

    git init
    git add README.md
    git commit -m "first commit"
    git remote add origin https://github.com/me/myrepo.git
    git push -u origin master


