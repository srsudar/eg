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


Return the most concise result of a query:

    dig <domain> <record-type> +short


