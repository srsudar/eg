# dig

query a DNS server for the A record of example.com

    dig example.com


display only the answer section containing the IPv4 address of example.com

    dig example.com +noall +answer


display only the IPv4 address of example.com

    dig example.com +short


display only Name Server records belonging to example.com

    dig example.com NS


display the 128-bit IPv6 address of example.com using the AAAA record

    dig example.com AAAA +short


display all DNS records for example.com

    dig example.com ANY


perform a reverse DNS lookup on IP address 192.168.1.42

    dig -x 192.168.1.42


use sns.dns.icann.org as the DNS server instead of the default

    dig @sns.dns.icann.org www.example.com



# Basic Usage

Interrogate a DNS server for all records about a domain:

    dig <domain> ANY


Interrogate a DNS server for a particular type of record about a domain:

    dig <domain> <record-type>


Interrogate a specific DNS server about a domain:

    dig @<DNS-address> <domain>


Return the most concise result of a query:

    dig <domain> <record-type> +short



# Using Google's Public DNS Servers

Google maintains public DNS servers that form the largest public DNS service in
the world. Like other servers, they can be accessed using the `@` syntax. Their
IPv4 addresses are `8.8.8.8` and `8.8.4.4`. Their two IPv6 addresses are
`2001:4860:4860::8888` and `2001:4860:4860::8844`. If a device cannot accept
the `::` syntax, replace it with `:0:0:0:0:`. These can further be expanded to
four zeros each. The following three commands are equivalent, but not all
devices can recognize all forms:

    $ dig @2001:4860:4860::8888 example.com
    $ dig @2001:4860:4860:0:0:0:0:8888 example.com
    $ dig @2001:4860:4860:0000:0000:0000:0000:8888 example.com


