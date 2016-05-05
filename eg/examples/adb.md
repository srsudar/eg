# adb

start a shell on the device

    adb shell


copy a local file onto the remote device

    adb push local.txt /sdcard/remote.txt


copy a remote file off the device

    adb pull /sdcard/remote.txt local.txt


install an apk onto the device

    adb install app.apk


list all attached devices

    adb devices


run ls /sdcard in a shell on the device and return

    adb shell ls /sdcard/


print the complete adb help

    adb help



# Basic Usage

Run one of a huge number of adb commands:

    adb <command>


Copy a local file onto the remote device:

    adb push <local> <remote>


Copy a remote file from the device to the local machine:

    adb pull <remote> <local>


Run a shell command on the device:

    adb shell <command>



# Installing and Uninstalling apk Files

Install an apk whose package does not yet exist on the device:

    adb install app.apk


If a previous version of the app already exists, use the `-r` argument to
perform an upgrade. This will keep existing data and go through the upgrade
procedures as if you were updating the app from the app store:

    adb install -r app.apk


Uninstall the app associated with the package `org.package.app`:

    adb uninstall org.package.app



# Logging

The device's log can be dumped and searched using `adb logcat`.

Dump all of the device's log and continue monitoring until `<CTRL>-c` is
pressed:

    adb logcat


Dump all the of the device's log and disconnect (`-d`):

    adb logcat -d


Log messages are printed with a tag. This command will dump only those log
messages that have the tag ConnectivityService (`-s ConnectivityService`):

    adb logcat -s ConnectivityService


Log messages are printed with a priority level. Requesting a priority level
will return all messages at that level and higher. From low to high, the order
is Verbose (`V`), Debug (`D`), Info (`I`), Warn (`W`), Error (`E`), and Fatal
(`F`). Levels must be passed using a particular tag, with `*` representing all
tags. This will print messages from all tags (`*`) at level Error and higher
(`:E`):

    adb logcat '*:E'


This will print all messages with the tag ConnectivityService at level Debug
and higher:

    adb logcat 'ConnectivityService:D'


Clear the log on the device (`-c`):

    adb logcat -c


Print the help information for `adb logcat` by passing any parameter that
cannot be interpreted as valid command (`:W`):

    adb logcat `:W`



# The Power of `shell`

The `adb shell` command can make use of a number of programs running on Android
devices to provide in-depth information about the system, installed packages,
and more.



# Activity Manager

The `am` command stands for Activity Manager and can be used with `adb shell`
to perform various Activity-related tasks.

This will start an activity named `ExampleActivity` in the `org.package.app`
package. The activity name must be relative, so in this case the fully
qualified name of `ExampleActivity` is `org.package.app.ExampleActivity`:

    adb shell am start org.package.app/.ExampleActivity


Force stop everything associated with the package `org.package.app`:

    adb shell am force-stop org.package.app


Intents can be broadcast to apps using the `broadcast` argument. This will send
the `android.os.action.DISCHARGING` intent to all apps:

    adb shell am broadcast -a android.os.action.DISCHARGING


Print the complete `am` help by passing no arguments:

    adb shell am



# Getting System Information

The `service` and `dumpsys` commands can be combined with `adb shell` to print
status information about the device.

Print a huge amount of system information about all running services:

    adb shell dumpsys


Print current cpu state:

    adb shell dumpsys cpuinfo


List all services running on the device (`list`):

    adb shell service list


See if the wifi service exists on a device (`check wifi`):

    adb shell service check wifi


Information about particular services can be dumped using `dumpsys` to obtain
specific system information.

List information about only the wifi service (`dumpsys wifi`):

    adb shell dumpsys wifi


Show memory information as returned by the `meminfo` service:

    adb shell dumpsys meminfo


Show the memory information of a particular package:

    adb shell dumpsys meminfo org.package.app


Use the `package` service to provide information about specific applications.
This command will show MIME types associated with the application, exported
content resolvers, authorities, permissions, etc:

    adb shell dumpsys package org.package.app



## Advanced Dump Options

Some arguments to `dumpsys` can take the flag `-h` to print additional
help about that particular command. An incomplete but useful list of these
commands is: `activity`, `window`, `meminfo`, `package`, and `batteryinfo`.

This will print all the help for the `activity` argument:

    adb shell dumpsys activity -h



# Package Manager

The `pm` command stands for Package Manager can be used to display information
about packages installed on the device.

To see a list of all installed packages, run:

    adb shell pm list packages


See the installed packages and their associated files:

    adb shell pm list packages -f


List all the permissions known to the device:

    adb shell pm list permissions -d -g


Permissions that have been requested by an applications can be granted
(`grant`) or revoked (`revoke`) by specifying their package name. This will
only work for apps that have requested a particular permission in their
manifest. This command refers to the package `org.package.app` and will revoke
the record audio permission:

    adb shell pm revoke org.package.app android.permission.RECORD_AUDIO


See detailed information about a particular package:

    adb shell pm dump org.package.app


Print the complete `pm` help by passing no arguments:

    adb shell pm



## Pull an apk Off a Device

The `path` command can be used with `pm` to get the path to the package's apk
file. This can be used with `adb pull` to pull a package's apk off of the
device. This sequence of commands discovers the apk path for the
`com.google.android.calendar` package and pulls the apk to the current
directory:

    $ adb shell pm path com.google.android.calendar
    /data/app/com.google.android.calendar-1/base.apk
    $ adb pull /data/app/com.google.android.calendar-1/base.apk



# Inspecting Protected Storage

By default, most apps store their data in protected storage that cannot be
easily accessed without rooting the device. This complicates debugging, as you
can't get access to your app's database. Fortunately this can be circumvented
using the `adb backup` command.

This sequence of commands will create a backup of all app data in protected
storage as specified by the `org.package.app` package name and store it as
`backup.ab`. The backup file format begins with human-readable text to display
the file type and the file version, followed by a compressed tar file. Assuming
a version number of a single byte, the compressed backup content starts after
24 bytes.

We use `dd` to extract only the compressed part of the file and use python to
decompress the content and save it as a tar file. Finally we'll extract the
contents of the file using `tar`, creating the app's directory as it existed on
the phone. Note that the backup will have to be manually approved on the device
after running `adb backup`, and that the `\` characters are line continuations
for use in the shell:

    $ adb backup -f ./backup.ab org.package.app
    $ dd if=./backup.ab bs=1 skip=24 \
      | python -c "import zlib,sys;sys.stdout.write(\
      zlib.decompress(sys.stdin.read()))" >backup.tar
    $ tar vfx backup.tar


