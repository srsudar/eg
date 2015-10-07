# git

Tel Git who you are
    
    git config --global user.name "Sam Smith"
    git config --global user.email sam@example.com
    git config --list

Create a new local repository
    
    git init
    
Checkout a repository
    
    git clone /path/to/repository
    git clone username@host:/path/to/repository

Add files

    git add <filename>
    git add *
    git add -A

Commit

    git commit -m "Commit message"
   
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
    
