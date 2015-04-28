# In eg 0.0.x, this file could be used to invoke eg directly, without installing
# via pip. Eg 0.1.x switched to also support python 3. This meant changing the
# way imports were working, which meant this script had to move up a level to be
# a sibling of the eg module directory. This file will exist for a time in order
# to try and give a more friendly error for people that are using the symlink
# approach. This warning will eventually disappear in a future version of eg.

DEPRECATION_WARNING = """
You are invoking eg via the script at <eg-repo>/eg/eg_exec.py. This file has
been deprecated in order to work with both python 2 and 3.

Please instead invoke <eg-repo>/eg_exec.py, or install with pip.

If you're using a symlink and need to update it, try something like the
following:

    rm `which eg`
    ln -s <absolute-path-to-eg-repo>/eg_exec.py /usr/local/bin/eg


Or, simply install with pip:

    sudo pip install eg

"""

print(DEPRECATION_WARNING)
