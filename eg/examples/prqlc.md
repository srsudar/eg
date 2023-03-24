# prqlc

run the compiler interactively

    prqlc compile


compile a .prql file standard output
 
    prqlc compile file.prql


compile a .prql file to a .sql file

    prqlc compile source.prql target.sql


compile a query

    echo "from employees | filter has_dog | select salary" | prqlc compile


watch a directory and compile on file modification

    prqlc watch path/to/directory


