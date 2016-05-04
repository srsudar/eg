# git

change the previous commit

    git commit --amend


unstage changes to foo.py that have been added

    git reset path/to/foo.py


show the contents of bar.java at revision e8883f

    git show e8883f:path/to/bar.java


show diff of baz.go between commits affbc and 6d680

    git diff affbc 6d680 -- path/to/baz.go


push all branches to the origin

    git push origin --all



# Basic Usage

Execute a command:

    git <command>


View the manpages for a command:

    git help <command>


`git` is a complex command. It takes a number of verb-like commands that
control `git` repositories and files. Examples for some commonly used commands
are shown in their own sections.



# add

`git add` is used to make files and changes known to git.

Add `foo.py`:

    git add foo.py


Add all changes in the repository (`-A`), adding, modifying, and removing as
necessary:

    git add -A



# diff

Show the differences in the working tree:

    git diff


Show the differences that have been added to the index via `git add`:

    git diff --cached


Show the differences in the file `baz.go` between commits `affbc` and `6d680`:
show diff of baz.go between commits affbc and 6d680

    git diff affbc 6d680 -- path/to/baz.go



# commit

Commit staged changes:

    git commit


Commit staged changes with the message "Update readme" (`-m "Update readme"`):

    git commit -m "Update readme"


Update the last commit (`--amend`). An editor will open giving you a chance to
edit the commit message. Staged changes will be combined with the changes of
the previous commit:

    git commit --amend



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



# config

Tell Git who you are

    git config --global user.name "Sam Smith"
    git config --global user.email sam@example.com
    git config --list


Create a new local repository

    git init


Checkout a repository

    git clone /path/to/repository
    git clone username@host:/path/to/repository


Push

    git push origin master



# Basic Usage

    git <command>
    git log

Initialize a repository
    git init
    git add README.md
    git commit -m "first commit"
    git remote add origin https://github.com/me/myrepo.git
    git push -u origin master



# Branches
Create a new branch and switch to it

    git checkout -b <branchname>

Switch from one branch to another

    git checkout <branchname>

List all the branches in your repo

    git branch

List all branch in the remote repo

    git branch -a

Delete a branch

    git branch -d <branchname>

Push the branch to your remote repository

    git push origin <branchname>

Delete a branch on your remote repository:

    git push origin :<branchname>

Delete branch from remote repository

    git push origin --delete <branchname>



# Tags
Create a tag on the last commit

    git tag -a v1.1 -m "Version 1.1 is waiting for review"
    git push --tags

Create a tag on a on a specific commit

    git tag 1.0.0 <commitID>



# Undo
Go back to the last commit

    git reset --hard HEAD

Cancel the last commit

    git reset --soft "HEAD^"


# COMPLETED

Add files

    git add <filename>
    git add *
    git add -A

Commit

    git commit -m "Commit message"

