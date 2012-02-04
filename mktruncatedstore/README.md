#Create a truncated contentstore

This little script will take a file list from find or similar
tool and create a truncated content store, meaning that all
files/directories are created but without any data.


Example usage:


    # Live Contentstore: /srv/contentstore
    $ find /srv/contentstore > /tmp/find-filelist.txt
    # This will create a trunctated contentstore under /tmp/test
    # -s will strip the leading path and add -d path
    $ ./mkdtrunc.py -f find-filelist.txt -d /tmp/test/ -s /srv/contentstore/


