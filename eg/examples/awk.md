# awk



# Print All Fields

` echo $PATH | awk -F: ' { for (i = 1; i < NF; i++) print $i }'`

Split lines into field on `:` (`-F:`).

Print all fields using a for loop. `NF` is the number of fields in the line,
`print $2` will print the second field.

This command will print your path, assuming it is colon-delimited:

`echo $PATH | awk -F: ' { for (i = 1; i < NF; i++) print $i }'`
