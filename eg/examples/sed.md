# sed

delete the line range

    nl /etc/passwd | sed '2,5d'

add multiple line

    nl /etc/passwd | sed '2a Drink tea or... \
    drink beer?'

change the line range

    nl /etc/passwd | sed '2,5c No 2-5 numbers'

show specific line range

    nl /etc/passwd | sed -n '5,7p'

Change the line

    ifconfig eth0 | grep 'inet addr' | \ 
    sed 's/^.*addr://g' | sed 's/Bcast.*$//g'

Multiple Command

    cat /etc/passwd | \
    sed -e '4d' -e '6c no six line' > passwd.new 
    
    $diff passwd.old passwd.new
