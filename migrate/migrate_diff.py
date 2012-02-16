#!/usr/bin/python
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

import os
import os.path as path

from subprocess import PIPE,Popen

pth = '/home/david/Projekt/alfresco/vgr/'
old_src = path.join(pth,'workspace/alfresco-src-3.3.5/root/')
new_src = path.join(pth,'alfresco-enterprise-3.4.4/')
src = path.join(pth,'workspace/trunk');


folders = [
    { 
        "name": 'Share webapp',
        "old":'projects/slingshot/source/web',
        "new":'projects/slingshot/source/web',
        "src":'share/src/main/webapp'
    },
    { 
        "name": 'Share webapp (web common parts)',
        "old":'projects/web-framework-commons/source/web/',
        "new":'projects/web-framework-commons/source/web/',
        "src":'share/src/main/webapp'
    },
    { 
        "name": 'Share config (web common parts)',
        "old":'projects/web-framework-commons/config/alfresco/site-webscripts/',
        "new":'projects/web-framework-commons/config/alfresco/site-webscripts/',
        "src":'share/src/main/config/alfresco/web-extension/site-webscripts'
    },
    { 
        "name": 'Share config (slingshot parts)',
        "old":'projects/slingshot/config/alfresco/site-webscripts',
        "new":'projects/slingshot/config/alfresco/site-webscripts',
        "src":'share/src/main/config/alfresco/web-extension/site-webscripts'
    },
    { 
        "name": 'Repo remote-api slingshot',
        "old":'projects/remote-api/config/alfresco/templates/webscripts/',
        "new":'projects/remote-api/config/alfresco/templates/webscripts/',
        "src":'repo/src/main/config/alfresco/templates/webscripts/'
    },
    {
        "name": 'Repo remote api repository',
        "old":  'projects/remote-api/config/alfresco/templates/webscripts/org/alfresco/repository',
        "new":  'projects/remote-api/config/alfresco/templates/webscripts/org/alfresco/repository',
        "src":  'repo/src/main/config/alfresco/templates/webscripts/'
     }
    
]



def diff(old,new):
    """
        Do a diff of two src trees, parse out file names, returns a dict
        with lists
        { new: [...], differ: [...], removed: [...] }
    """
        #do a diff of old and new
    cmd = 'LC_ALL=C diff -rq %s %s | grep -v .svn' % (old,new)    
    res = Popen(cmd,shell=True,stdout=PIPE).communicate()[0]

    differ  = []
    new     = []
    removed = []
    for l in res.splitlines():
        if l.endswith('differ'):
            differ.append(l.split()[3])
        elif l.startswith('Only'):
            s = l.split()
            fpth = path.join(s[2][:-1],s[3])

            if 'alfresco-enterprise-3.4.4' in l:
                new.append(fpth)
            else:
                removed.append(fpth)
                
    return { 'differ': differ, 'removed':removed, 'new':new }
    


for f in folders:
    full_old = path.join(old_src,f['old'])
    full_new = path.join(new_src,f['new'])
    files = diff(full_old,full_new)
    
    changed = []
    removed = []
    rm_len = len('/home/david/projects/alfresco/vgr/workspace/trunk')
    #Let's check which we have overloaded and has been changed
    full_new_len = len(full_new)+1
    src_pth = path.join(src,f['src'])
    for pth in files['differ']:
        #differs always have the new path
        foo = path.join(src_pth,pth[full_new_len:])
        if path.isfile( foo ):
            #we have a source file!
            changed.append({
                "short":foo[rm_len:],
                "old": path.join(full_old,pth[full_new_len:]),
                "new": pth,
                "our": foo
            })    
        #else: 
        #    print "no diff ",foo
        
        
    full_old_len = len(full_old)+1
    for pth in files['removed']:
        #removed always have the old path        
        foo = path.join(src_pth,pth[full_old_len:])
        if path.isfile( foo ):
            #we have a removed source file
            removed.append({
                "short":foo[rm_len:],
                "old": pth,
                "new": "",
                "our": foo
            })   
        #else:
        #    print "not removed ",foo
        
    #print f['name']
    if removed != []:
        #print "Removed"
        for obj in removed:
            print  'meld %(old)s %(our)s' % obj
    #else:
    #    print "No files were removed"
        
    if changed != []:
        #print "Changed files that need to be diffed"
        for obj in changed:
            print  'meld --diff %(old)s %(our)s --diff %(old)s %(new)s  --diff %(old)s %(our)s %(new)s --diff %(our)s %(new)s' % obj 
    #else:
    #    print "No files where changed"
        
    #print 
    #print
    


            
            
