# rsync

Synchronize two different directories, but ignore deleted files:

    rsync -av <directory1> <directory2>

Synchronize two different directories and delete files in `directory2`
if they have been deleted from `directory1` with `--delete`:

    rsync -av --delete <directory1> <directory2>

Run rsync without really doing the synchronization (for checking
purpose) with `--dry-run`:

    rsync --dry-run -av --delete <directory1> <directory2>

# Basic usage

Synchronize your local machine with another:

    rsync -av --delete <localpath> <distantmachine>@<distantpath>
