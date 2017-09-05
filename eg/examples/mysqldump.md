
To backup all mysql databases:

mysqldump -u root -p$(head -1 /root/.mysqlpass) --all-databases --flush-logs --single-transaction --events | gzip > /var/backups/mysql.sql.gz

It assumes you have the mysql root password saved in /root/.mysqlpass

