# date

Display current date in the given format

      date +'%Y-%m-%d %H:%M:%S'


Display current date for a given timezone (use tzselect to find TZ)

      TZ='Europe/Paris' date


Convert seconds since the epoch (1970-01-01 UTC) to a date

      date --date='@<timestamp>'


Show the local time for 9PM next Friday on the west coast of the US

      date --date='TZ="America/Los_Angeles" 09:00 PM next Friday'



# Basic Usage

Display a date in the given format

      date --date='<date>' +'<format>'



# Common date formats

- %Y : year (e.g., 2015)
- %m : month (01..12)
- %d : day of month (01..31)
- %F : full date; same as %Y-%m-%d

- %H : hour (00..23)
- %M : minute (00..59)
- %S : second (00..60)
- %T : time; same as %H:%M:%S

- %I : hour (01..12)
- %p : locale's equivalent of either AM or PM; blank if not known
- %r : locale's 12-hour clock time (e.g., 11:11:04 PM)

- %s : seconds since 1970-01-01 00:00:00 UTC


