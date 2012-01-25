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

import sys
import os.path
import argparse as arg

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'w').close()


def truncate(args):
    # Read from stdin
    for line in open(args.file).readlines():
        line = line.strip()
        # Strip the leading path
        if args.strip:
            line = line[len(args.strip):]

        # We know that every file in the contentstore is a .bin file,
        # we also weed out empty directories here.
        if line.find(".bin") != -1:
            # only the path
            tmpdir = os.path.join(args.dest, os.path.dirname(line))
            # Full path to new file
            tmpfile = os.path.join(args.dest, line)
            try:
                # check if we already got the directory.
                if os.path.isdir(tmpdir) is False:
                    if args.noop:
                        print "mkdir:  %s" % tmpdir
                    else:
                         os.makedirs(tmpdir, 0755)
                # Now we should have our directory so lets create
                # an empty file.
                if args.noop:
                    print "touch:  %s" % tmpfile
                else:
                    touch(tmpfile)
            except os.error, e:
                # We send errors to stdout
                print >> sys.stderr. e

def main():
    p = arg.ArgumentParser("Make a truncated content store")
    p.add_argument("-f", '--file', help="read input file")
    p.add_argument("-d", '--dest', help="desitnation base path")
    p.add_argument("-s", '--strip', help="strip path")
    p.add_argument("-n", '--noop', action="store_true", help="do nothing, only print")
    args = p.parse_args()
    if args.dest is None or args.file is None:
        p.print_help()
        sys.exit(0)

    truncate(args)

    
if __name__ == '__main__':
    main()
