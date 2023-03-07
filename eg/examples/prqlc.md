# prqlc

Run the compiler interactively:

    prqlc compile


Compile a .prql file standard output:
 
    prqlc compile file.prql


Compile a .prql file to a .sql file:

    prqlc compile source.prql target.sql


Compile a query:

    echo "from employees | filter has_dog | select salary" | prqlc compile


Watch a directory and compile on file modification:

    prqlc watch path/to/directory
