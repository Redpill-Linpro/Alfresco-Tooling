#!/usr/bin/env python
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
import shutil
from subprocess import call


class Alfresco(object):
    def __init__(self,args):
        self.tomcat = path.abspath(args.tomcat)
        self.tomcat_share = args.tomcat_share and path.abspath(args.tomcat_share) or path.abspath(args.tomcat) #if not set defualt to repo tomcat
        self.share  = path.abspath(args.share)
        self.repo   = path.abspath(args.repo)
        self.notification = args.no_notification and None or args.notification
        self.quiet = args.quiet
        self.host = args.tomcat_host 
        self.share_host = args.tomcat_share_host
        

    def notify(self,msg):
        """Send out a notification message"""
        if self.notification is not None:
            call(self.notification % msg,shell=True)

    def call(self,*args,**kwargs):
        if not self.quiet:
            print "Executing: ",args[0]
        call(*args,**kwargs)

    def sync(self,scope):
        if scope == "repo":
            self.sync_repo()
        elif scope == "share":
            self.sync_share()
            self.sync_webapp()
        elif scope == "webapp":
            self.sync_webapp()
        elif scope == "all":
            self.sync_webapp()
            self.sync_repo()
            self.sync_share()


    def reload(self,scope):
        if scope == "repo":
            self.reload_repo()
        elif scope == "share":
            self.reload_share()
        elif scope == "all":
            self.reload_repo()
            self.reload_share()

    def reload_repo(self):
        """ Reload repo webscripts using it's webservice (with curl)"""
        self.call('curl -o /tmp/curl.html --user admin:admin --data-urlencode "reset=on" %s/alfresco/service/index %s' %  (self.host,self.quiet and '> /dev/null 2>&1' or ''),shell=True)

    def reload_share(self):
        """ Reload share webscripts using it's webservice (with curl)"""
        self.call('curl -o /tmp/curl.html --user admin:admin --data-urlencode "reset=all" %s/share/page/console %s' % (self.share_host,self.quiet and '> /dev/null 2>&1' or ''),shell=True)
        
    def sync_repo(self):
        """ rsync repo webscripts"""
        self.call("rsync -avh %s %s %s" % (path.join(self.repo,'config/'),path.join(self.tomcat,'shared/classes/'),self.quiet and '> /dev/null 2>&1' or ''),shell=True)

    def sync_webapp(self):
        """ rsync webbapp, i.e. client side js,css and images """
        self.call("rsync -avh %s %s %s" % (path.join(self.share,'webapp/'),path.join(self.tomcat_share,'webapps/share/'),self.quiet and '> /dev/null 2>&1' or ''),shell=True)
        
    def sync_share(self):
        """ rsync share webscripts"""
        self.call("rsync -avh %s %s %s" % (path.join(self.share,'config/'),path.join(self.tomcat_share,'shared/classes/'),self.quiet and '> /dev/null 2>&1' or ''),shell=True)

    def sync_all(self):
        """Syncs both repo and share """
        self.sync_webapp()
        self.sync_repo()
        self.sync_share()

    def reload_all(self):
        """reloads share and repo """
        self.reload_repo()
        self.reload_share()
        
    def override(self,pth):
        """Override a file in alfresco, i.e copy it to our source tree in a proper place"""
        pth = path.abspath(pth)
        if not path.isfile(pth):
            print "Can't find file: %s" % pth
            return
        
        def copy(src_pth):
            #there might not be a proper folder for it
            folder = path.dirname(src_pth)
            if not path.exists(folder):
                os.makedirs(folder)
            
            print "Copying file"
            print "From:",pth
            print "To:",src_pth
            shutil.copy(pth,src_pth)
        
            
        
        #check if it's share or repo
        if '/share/' in pth:
            #is it in config or in 
            if '/WEB-INF/classes/alfresco/' in pth:
                copy(path.join(self.share,'config/alfresco/web-extension' ,pth.split('/WEB-INF/classes/alfresco/')[1]))                    
            elif '/WEB-INF/classes' in pth:
                print "I don't know how to override that, sorry"
            else:
                #must be web
                copy(path.join(self.share,'webapp' ,pth.split('/share/')[1]))
        
        else: #hence repo 
            print "Overriding repo webscript, you might need to manually copy these to webapps alfresco since overriding doesn't always work here"
            copy(path.join(self.repo,'config',pth.split('/WEB-INF/classes/')[1]))
        
        
        
if __name__ == "__main__":
    import sys
    import argparse

    def using(tomcat,tomcat_share,repo,share):
            print """Using:
tomcat: %s 
tomcat share: %s
repo:   %s
share:   %s
        """ % (tomcat,tomcat_share or 'Not set',  repo,share)

    #some mac os x love
    notification_cmd = sys.platform.startswith('darwin') and 'growlnotify -m "%s"' or 'notify-send --hint=int:transient:1 "%s"'
    
    parser = argparse.ArgumentParser(description="Hotdeployment script for alfresco")
    parser.add_argument('-q','--quiet',action="store_true", default=False,help="Disable output")
    parser.add_argument('-N','--no-notification',action="store_true", default=False,help="Disable notfications")
    parser.add_argument('-n','--notification',default=notification_cmd,help="Notification binary")
    parser.add_argument('-t','--tomcat',default="/opt/alfresco/tomcat"     ,help="Path to tomcat")
    parser.add_argument('-ts','--tomcat-share',default=None ,help="Path to tomcat used for share if it's different than repo. Only required when using two tomcats and 'reload' or 'deploy' 'all'")
    parser.add_argument('-th','--tomcat-host',default="http://localhost:8080",help="Host used for tomcat, i.e. http://localhost:8080")
    parser.add_argument('-tsh','--tomcat-share-host',default="http://localhost:8080",help="Host used for alfresco share tomcat, i.e. http://localhost:8080")
    parser.add_argument('-s','--share' ,default="trunk/share/src/main/",help="Path to share src")
    parser.add_argument('-r','--repo'  ,default="trunk/repo/src/main/" ,help="Path to repo src")
    sub = parser.add_subparsers(help="Action subparser")

    #sync
    sync = sub.add_parser('sync',help="Sync files with rsync")
    sync.add_argument('scope',choices=['repo','share','webapp','all'],help="What to sync, 'share' will also sync webapp and 'all' syncs them all")

    def sync_func(args):
        if not args.quiet:
            using(args.tomcat,args.tomcat_share,args.repo,args.share)
        a = Alfresco(args )
        a.sync(args.scope)
        a.notify("Synced %s" % args.scope)
        
    sync.set_defaults(func=sync_func)
    
    #reload
    rel = sub.add_parser('reload',help="Reload wbescript with curl")
    rel.add_argument('scope',choices=['repo','share','all'],help="What to reload, 'repo','share' or 'all'")
    
    def rel_func(args):
        if not args.quiet:
            using(args.tomcat,args.tomcat_share,args.repo,args.share)
        a = Alfresco(args)
        a.reload(args.scope)
        a.notify("Reloaded %s" % args.scope)

    rel.set_defaults(func=rel_func)

    #deploy
    deploy = sub.add_parser('deploy',help="Sync and reload")
    deploy.add_argument('scope',choices=['repo','share','all'],help="What to sync and reload: 'repo','share' or 'all'")

    def deploy_func(args):
        if not args.quiet:
            using(args.tomcat,args.tomcat_share,args.repo,args.share)
        a = Alfresco(args)
        a.sync(args.scope)
        a.reload(args.scope)
        a.notify("Synced and reloaded %s" % args.scope)

    deploy.set_defaults(func=deploy_func)
    
    #override
    override = sub.add_parser('override',help="Override a file in Alfresco")
    override.add_argument('file',help="Path to file to overide")

    def override_func(args):
        if not args.quiet:
            using(args.tomcat,args.tomcat_share,args.repo,args.share)
        a = Alfresco(args)
        a.override(args.file)
        
    override.set_defaults(func=override_func)

    args = parser.parse_args()
    args.func(args)
    
    
    

