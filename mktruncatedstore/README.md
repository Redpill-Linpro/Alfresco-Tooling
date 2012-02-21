#Create a truncated contentstore

This script creates an Alfresco contentstore with all the files intact which is needed for 
Alfresco to function and all other files as 0 byte files.

Example usage:

    # This will create a file named archive.tar.gz under the current directory
    $ ./mkdtrunc.py \
         -s /srv/contentstore \
         -d /tmp/alfresco 
         -u http://localhost:8080/alfresco/service/admin/excludelist \
         -U admin \
         -P admin \
         -p archive.tar.gz
