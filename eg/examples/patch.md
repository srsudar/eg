# patch

apply unified.patch containing unified context to the file specified therein

    patch <unified.patch


apply default.patch without unified context to a.txt

    patch a.txt <default.patch


use the whole file path in unified.patch to find the file to patch

    patch -p0 <unified.patch



# Basic Usage

Apply a patch file with unified context:

    patch <<patchfile>


Apply a patch file without unified context:

    patch file-to-patch.txt <<patchfile>


See `eg diff` for more discussion on unified context.



# Accounting for Patch File Location

By default, the file specified by a unified context is assumed to be in the
current directory. However, the file specified in unified context can include
more specific path information. This can be taken into account by `patch` by
using the `-p` command, which allows you to store the patch file at a different
location.

The `-p` command takes a numeric value. It modifies the search path of the file
by stripping a leading string by consuming as many slashes as possible from the
path in the patch file. A value of 0 will cause `patch` to take the entire path
rather than look in the current directory.

If the file name in the patch file is `/absolute/path/to/repo/file.txt`, this
command will cause `patch` to look for the file using the entire path by
stripping no prefix string (`-p0`):

    patch -p0 <unified.patch


If the patch file resided as a sibling of the `repo/` directory, 4 slashes
(`-p4`) would need to be stripped to point `patch` at the file located in
`repo/file.txt`:

    patch -p4 <unified.patch


