# keytool

list detailed info about entries in keystore

    keytool -v -list -keystore keys.keystore


list only info about release alias

    keytool -v -list -keystore keys.keystore -alias release


view a certificate

    keytool -v -printcert -file certificate.crt


delete the alias deleteme from the keystore

    keytool -delete -alias deleteme -keystore keys.keystore


change the top level password of the keystore

    keytool -storepasswd -keystore keys.keystore


change the password for the changeme alias

    keytool -keypasswd -alias changeme -keystore keys.keystore



# Basic Usage

List the contents of a keystore:

    keytool -v -list -keystore <keystore>



# Generate a Key Pair

`keytool` can give rise to many long commands. This command generates a key
pair (`-genkey`) inside `keys.keystore`, creating if it doesn't exist. It also
generates an alias called `release` (`-alias release`) using the RSA algorithm
(`-keyalg RSA`). The key will be of size 2048 (`-keysize 2048`) and be valid
for 10,000 years (`-validity 10000`):

    keytool -genkey -v -keystore keys.keystore -alias release \
    -keyalg RSA -keysize 2048 -validity 10000


You will be prompted to enter a password for both the keystore itself (entering
it twice if you are creating the keystore for the first time) a password for
the alias, and information about your organization. This keystore can be used
to sign JAR files and Android apk files.


