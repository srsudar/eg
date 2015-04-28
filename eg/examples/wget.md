# wget

Download a single file:

    wget <URL>


Download a file in the background:

    wget -b <URL>


Download and "Save as":

    wget -O <new_filename> <URL>
    
    
Continue an incomplete download:

    wget -c <URL>


Download a single file if it is newer than a local copy:

    wget -c -‐timestamping <URL>
    
    
Download a complete website:

    wget --mirror -p --convert-links -P <DIR> <URL>
    
    
Download all files with a specific file type (png, for example):

    wget -r -A.png <URL>
    
    
Download a specific directory:

    wget -r --no-parent <URL>
    
    
Display a file without saving it:

    wget ‐‐output-document – ‐‐quiet <URL>


Limit download speed:

    wget --limit-rate=100k <URL>
