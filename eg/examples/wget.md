# wget

download a single file

    wget http://www.example.com/index.html


download file and save it as download.html

    wget -O download.html http://www.example.com/index.html


download a page with all resources for offline viewing

    wget -EHkKp http://www.example.com


download a file only if it is newer than a local version

    wget -N http://www.example.com/index.html


get files up to two pages deep with names ending in png but not containing foo

    wget -r 2 -A png -R "*foo*" http://www.example.com



# Basic Usage

Download a file:

    wget <url>



# Download a Site for Offline Viewing

There are numerous ways to try and get `wget` to download a website for offline
viewing. One of the more robust is the combination of flags `-EHkKp`. Though
verbose, the command is recommended by the `wget` manual. Note that this will
only make the top-level page suitable for offline viewing, not all the pages
it links to. It converts pages to html from dynamically generated pages like
.asp or .php (`-E`), allows the request to access multiple hosts to satisfy
resource requirements (`-H`), converts resource links to paths appropriate for
local viewing (`-k`), creates files with .orig suffixes if conversions were
performed (`-K`), and gets embedded resources (`-p`):

    wget -EHkKp http://www.example.com


To make an entire site viewable offline, add the `-m` flag, which stands for
mirroring, and allows recursion to infinite depth. If this is allowed to span
hosts (`-H`) it can generate a huge number of requests. It should always be
used carefully. This will download an entire site (`-m`) in a way suitable for
offline viewing (`-EkKp`) without spanning hosts:

    wget -EkKpm http://www.example.com


`wget` tries to be a good citizen and respects `/robots.txt`, which can prevent
some resources from being downloaded. The following command will disregard
`/robots.txt` (`-e robots=off`) and potentially download a more complete page:

    wget -EHkKp -e robots=off http://www.example.com


Such commands can issue a large number of requests that may impact the server.
This command will wait on average 20 seconds (`--wait=10`) between requests and
limit bandwidth usage to 15k (`--limit-rate=15k`):

    wget -EHkKp --wait=10 --limit-rate=15k http://www.example.com



# Inspecting Websites

See if a file exists at the URL, but download nothing (`--spider`):

    wget --spider http://www.example.com/index.html


Look for broken links (`--spider`) anywhere on a site by following all the
links on the page recursively (`-r`):

    wget -r --spider http://www.example.com


Save cookies to a file (`--save-cookies cookies.txt`) and save session cookies
(`--keep-session-cookies`):

    wget --save-cookies cookies.txt --keep-session-cookies www.google.com


