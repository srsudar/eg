
To backup all the postgres databases

su - postgres -c 'pg_dumpall' >pg-dumpall.sql 2>$ferr
gzip pg-dumpall.sql


