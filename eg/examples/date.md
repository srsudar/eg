# date

Display current date and time

      date +'%Y-%m-%d %H:%M:%S'


Display current date for a given timezone (use `tzselect` to find a timezone's name)

      TZ='Europe/Paris' date


Convert seconds since the epoch (1970-01-01 UTC) to a date

      date -d @2147483647



# Basic Usage

Display a date in the given format

    date --date='<date string>' +'<format>'


Set the system clock

    date --set='<date string>'



## Date string

Date string argument is a human readable date string.



## Common date formats

### Date

- %Y : year (e.g., 2015)
- %m : month (01..12)
- %d : day of month (01..31)
- %F : full date; same as %Y-%m-%d

### Time

- %H : hour (00..23)
- %M : minute (00..59)
- %S : second (00..60)
- %T : time; same as %H:%M:%S
- %I : hour (01..12)
- %p : locale's equivalent of either AM or PM; blank if not known
- %r : locale's 12-hour clock time (e.g., 11:11:04 PM)

### Timestamp

- %s : seconds since 1970-01-01 00:00:00 UTC



# Advanced examples

Built-in standards

    date --iso-8601
    date --rfc-2822
    date --rfc-3339=seconds
    date --utc


Print the local time for 9PM next Friday on the west coast of the US

    date --date='TZ="America/Los_Angeles" 09:00 PM next Friday'


Convert a date string into timestamp

    date --date='Tue, 23 Jun 2015 11:21:42 +0200' +%s


Print the date of the day three months and one day hence

    date --date='3 months 1 day'


Print the day of the week of Christmas in the current year

    date --date='25 Dec' +%A


Set the system clock forward by two minutes

    date --set='+2 minutes'



A very complete documentation with a lot of examples is available at http://www.gnu.org/software/coreutils/date or with the command `info coreutils 'date invocation'`


