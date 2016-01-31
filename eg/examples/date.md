# date

display current date and time

    date


display current date and time in UTC

    date -u


display current date and time with custom format

    date +'%Y-%m-%d %H:%M:%S'


display current date for a given timezone (find timezone name with `tzselect`)

    TZ='Europe/Paris' date


convert seconds since the epoch (1970-01-01 UTC) to a date

    date -d @2147483647



# Basic Usage

Display the current date and time in a particular format:

    date +'<format>'


The format argument can be omitted to display the current date and time in the
default format. For detailed descriptions of the arguments, see the Common Date
Formats section below.



# Set the System Clock

The `date` command also lets you set the system clock. Syntax for this varies
across operating systems. Only the superuser can set the date, so all examples
begin with `sudo`. The format of the string is `mmddHHMMccyy.ss` To refer to
the date December 24th, 2014 at 2:45 in the afternoon you would use the string
`122414452014`.


## Linux

Set the system clock to December 24th, 2014 at 2:45 in the afternoon:

    sudo date --set='122414452014'


## OSX

Set the system clock to 5:15 in the afternoon on the current day:

    sudo date 1715



# A Note on Versions

The Linux version of `date` supports more functionality than the OSX version.
Similar functionality can be obtained on OSX by installing `coreutils` (install
with `brew install coreutils`) and then using `gdate`.



# Manipulate Dates and Times

`date` can be used to change the formats of dates and times. Reformat the human
readable date (`--date='Mar 27, 2016 2:45PM'`) to a conventional mm-dd-yy HH:MM
machine readable format (`+'%y-%m-%d %H:%M'`):

    date --date='<date string>' +'<format>'



# Common Date Formats

Valid arguments in format strings passed to `date` are summarized here.


## Date

`%Y`: year (e.g., 2015)
`%m`: month (01..12)
`%d`: day of month (01..31)
`%F`: full date; same as %Y-%m-%d


## Time

`%H`: hour (00..23)
`%M`: minute (00..59)
`%S`: second (00..60)
`%T`: time, same as %H:%M:%S
`%I`: hour (01..12)
`%p`: locale's equivalent of either AM or PM; blank if not known
`%r`: locale's 12-hour clock time (e.g., 11:11:04 PM)


## Timestamp

`%s`: seconds since 1970-01-01 00:00:00 UTC



# Advanced examples

Show the current date and time using built-in standards:

    date --iso-8601
    date --rfc-2822
    date --rfc-3339=seconds
    date --utc


Print the local time for 9PM next Friday on the west coast of the US:

    date --date='TZ="America/Los_Angeles" 09:00 PM next Friday'


Convert a date string into timestamp:

    date --date='Tue, 23 Jun 2015 11:21:42 +0200' +%s


Print the date of the day three months and one day in the future:

    date --date='3 months 1 day'


Print the day of the week of Christmas in the current year:

    date --date='25 Dec' +%A


Set the system clock forward by two minutes:

    date --set='+2 minutes'


A very complete documentation with a lot of examples is available at
http://www.gnu.org/software/coreutils/date or with the command
`info coreutils 'date invocation'`.


