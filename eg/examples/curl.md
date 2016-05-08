# curl

issue a GET request to a URL

    curl http://www.example.com


issue a PUT request with a JSON payload

    curl -X PUT http://www.example.com -d '{"key": "value"}'


POST data.txt to a URL

    curl -X POST http://www.example.com --data-binary @data.txt


issue a GET request with a header Key paired to Value

    curl -X PUT http://www.example.com -H "Key:Value"



# Basic Usage

Issue an HTTP request of a particular method type to a URL. By default `curl`
issues a GET request. The `-X` flag lets you specify other methods, like PUT
and POST:

    curl -X <method> <url>



# Cookies

`curl` can use cookies. The `--cookie` flag allows you to set name=value pairs
at the command line. This command will issue a GET request, print verbose
output (`-v`), and pass a cookie where TOKEN is set to data
(`--cookie "TOKEN=data"`):

    curl -v --cookie "TOKEN=data" http://www.example.com


# Querying Sets and Ranges

`curl` can be used to issue requests to numerous URLs simultaneously, issued in
sequential order. This command will issue requests to both the www and admin
subdomains (`{www,admin}`) of example.com:

    curl http://{www,admin}.example.com


It can also query sequential ranges by placing numbers in square brackets. This
will issue requests for resources 1.txt, 2.txt, 3.txt, and 4.txt (`[1:4]`) from
example.com:

    curl http://www.example.com/[1:4].txt


You can also specify a step. This will query letters of the alphabet (`a-z`),
but only every second letter (`:2`):

    curl http://www.example.com?letter=[a-z:2]


