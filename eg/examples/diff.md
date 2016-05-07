# diff

output the differences between two files

    diff a.txt b.txt


show differences with unified context (like git)

    diff -u a.txt b.txt


show differences between two directories

    diff -r dir1/ dir2/


save a diff to a patch file called diff.patch

    diff -u a.txt b.txt >diff.patch



# Basic Usage

Show the differences between two files:

    diff <original> <modified>


Output generated with unified context (`-u`) is simpler to understand for many
users. It is also the output used by many version control systems. This will
output changes with surrounding unchanged lines for context, as well as show
additions with `+` and subtractions with `-`:

    diff -u <original> <modified>


More precisely, `diff` tries to output the minimal number of line insertions
and line deletions that would transform one file into another.



# Basic Output

By default, output from the `diff` command consists of an action (either an
addition `a`, a change `c`, or a deletion `d`), the contents of the original
file, and the contents of the modified file.

The action is shown as the line number in the original file followed by an `a`,
`c`, or `d`, and followed by the line number in the modified file. Output of
the two files is separated by `---`.

For example, this output means that line five was `line five` in the original
file, and has been changed to `line five modified` in the modified file:

    5c5
    < line five
    ---
    > line five modified


For additions and deletions, only output from the modified or original file is
shown.



# Unified Context

Unified context is the format commonly used for creating patch files that can
then be applied using the `patch` command. It is also the output format used by
many version control systems, including git. Unified context means that `diff`
will show changes surrounded by three unchanged lines to show context. This
output from the file is called a hunk. The output will also show the file names
of the two files being compared as well as where in the file the displayed hunk
comes from. Consider the following files.

The original file, `a.txt`:

    this is line one
    and line two
    here is line three
    line four
    fifth is line five
    line six
    line seven is heaven
    line eight
    line nine is fine
    finally, line ten


And a modified version called `b.txt`:

    this is line one
    and line two
    here is line three
    line four
    line five in b.txt
    line six
    line seven is heaven
    line eight
    line nine is fine


In `b.txt` the 5th line is modified and the 10th line is deleted. Observe how
`diff` generates unified context with the `-u` option:

    $ diff -u a.txt b.txt
    --- a.txt 2015-05-30 17:29:57.000000000 -0700
    +++ b.txt 2015-05-30 17:30:31.000000000 -0700
    @@ -2,9 +2,8 @@
     and line two
     here is line three
     line four
    -fifth is line five
    +line five in b.txt
     line six
     line seven is heaven
     line eight
     line nine is fine
    -finally, line ten


Lines beginning with a space are present in both files. Lines beginning with
a single `-` occur only in the original file, while those beginning with a
single `+` occur only in the modified file. In other words, lines beginning
with a single `-` have been deleted while those beginning with a single `+`
have been added.

The line beginning with `---` shows the name of the original file to which we
are comparing, while the line beginning with `+++` shows the name of the
modified file.

The line beginning with `@@` shows the ranges of the hunks being displayed. The
range beginning with `-` is the range in the original file (`-2,9`) while the
address beginning with `+` shows the range in the modified file (`+2,8`).

The first number of the range shows where the given hunk begins in the file.
`-2` means that the hunk shown begins at line 2 in the original file, while
`+2` means the hunk begins at line two in the modified file.

The second number of the range shows how many total lines of the output are
from the file. In `-2,9`, the 9 means that of all the lines of the hunk shown,
9 are from the original file. In other words, the number of lines beginning
with a space or a single `-` sum to 9. In `+2,8`, meanwhile, the 8 means that
the lines beginning with a space or a single `+` total to 8.


