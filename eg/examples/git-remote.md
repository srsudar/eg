# git-remote

add a new distant repository `upstream`, hosted at
`git@github.com:srsudar/eg.git`

    git remote add upstream git@github.com:srsudar/eg.git


# Basic Usage

see the set of repositories whose branches you track (including URI to
these repositories)

    git remote -v


add a new distant repository <repo> to your project (very useful when
you want to follow the main code-base when you are a working on a fork)

    git remote add <repo> <uri-to-repo>
