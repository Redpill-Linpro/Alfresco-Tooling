#!/usr/bin/env python
#
#   This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012, Redpill Linpro
# Fredrik Steen <fredrik.steen@redpill-linpro.com>
# Niklas Ekman <niklas.ekman@redpill-linpro.com>
# David Jensen <david.jensen@redpill-linpro.com>

import sys
import os.path
import argparse as arg
import subprocess as sub
import urllib2
import base64
import shutil

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'w').close()


def truncate(args,files):
    # Read from stdin
    for line in files.splitlines():
        line = line.strip()
        
        # We know that every file in the contentstore is a .bin file,
        # we also weed out empty directories here.
        if line.find('.bin') != -1:
            #strip path up to and including contentstore
            store = os.path.abspath(args.store)
            line = line[len(store):]
            line = line[0] == '/' and line[1:] or line
            
            # only the path
            tmpdir = os.path.join(args.dest, os.path.dirname(line))
            # Full path to new file
            tmpfile = os.path.join(args.dest, line)
            try:
                # check if we already got the directory.
                if os.path.isdir(tmpdir) is False:
                    if args.noop:
                        print 'mkdir:  %s' % tmpdir
                    else:
                         os.makedirs(tmpdir, 0755)
                # Now we should have our directory so lets create
                # an empty file.
                if args.noop:
                    print 'touch:  %s' % tmpfile
                else:
                    touch(tmpfile)
            except os.error, e:
                # We send errors to stdout
                print >> sys.stderr. e

def create_list(store):
    pth = os.path.abspath(store)
    return sub.Popen('find %s' % pth, shell=True, stdout=sub.PIPE).communicate()[0]

def fetch_list(url, username, password):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header('Authorization', 'Basic %s' % base64string)
    res = urllib2.urlopen(request, timeout=10*60).read().splitlines()
    
    return filter(lambda x: x != '',res)

def copy_files(store, files, dest, noop=False):
    for f in files:
        if noop:
            print 'Copying file %s to %s' % (f, os.path.join(dest, f))
        else:
            shutil.copy2(os.path.join(store, f),os.path.join(dest, f))
    
def main():
    p = arg.ArgumentParser('Make a truncated content store')
    
    p.add_argument('-s', '--store', help='path to contentstore')
    p.add_argument('-d', '--dest', default='/tmp/contentstore',help='desitnation base path')
    p.add_argument('-n', '--noop', action='store_true', help='do nothing, only print')
    p.add_argument('-u', '--url', default='http://localhost:8080/alfresco/service/admin/excludelist',help='url to fetch list from webscript')
    p.add_argument('-U', '--username', default='admin',help='username for authentication')
    p.add_argument('-P', '--password', default='admin',help='password for authentication')
    p.add_argument('-nz', '--nogzip', action='store_true',help='do not tar, gzip and clean up afterwards')
    p.add_argument('-p', '--package', default='contentstore.tar.gz', help='filename to use when creating a tar and gzip package')
    
    args = p.parse_args()
    if args.dest is None or args.store is None:
        p.print_help()
        sys.exit(0)
        
    # create dest dir if not found
    print('Checking for destination directory and creating if needed...\n')
    if not os.path.isdir(args.dest):
        os.mkdir(os.path.abspath(args.dest))
    
    # create a list of the files in the contentstore
    print('Creating list of files to create 0 byte files for...\n')
    files = create_list(args.store)
    
    # create 0 byte files and directories of the files
    print('Creating 0 byte files...\n')
    truncate(args,files)
    
    # get a list of files to copy from a URL
    print('Getting list from server representing actual files to copy...\n')
    files_to_copy = fetch_list(args.url,args.username,args.password)
    
    # copy the files to the destination
    print('Copy the actual files...\n')
    copy_files(args.store,files_to_copy,args.dest,args.noop)
    
    # if gzip is needed, execute that
    if not args.nogzip:
        if args.noop:
            print 'packaging %s' % args.package
        else:
            print('Packaging result as tar.gz file and clean up...\n')
            dest = args.dest[:-1] == '/' and args.dest or args.dest+'/'
            sub.call('tar -czf %s %s' % (args.package, dest) ,shell=True)
            sub.call('rm -r %s' % dest,shell=True)

if __name__ == '__main__':
    main()
