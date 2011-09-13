#!/usr/bin/python

import os.path as path
from subprocess import call


class Alfresco(object):
    def __init__(self,tomcat,share,repo,notification=None):
        self.tomcat = path.abspath(tomcat)
        self.share  = path.abspath(share)
        self.repo   = path.abspath(repo)
        self.notification = notification

    def notify(self,msg):
        """Send out a notification message"""
        if self.notification is not None:
            call(self.notification % msg,shell=True)

    def call(self,*args,**kwargs):
        print "Executing: ",args[0]
        call(*args,**kwargs)

    def sync(self,scope):
        if scope == "repo":
            self.sync_repo()
        elif scope == "share":
            self.sync_repo()
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
            self.reload_repo()
        elif scope == "all":
            self.reload_repo()
            self.reload_share()

    def reload_repo(self):
        """ Reload repo webscripts using it's webservice (with curl)"""
        self.call('curl --user admin:admin --data-urlencode "reset=on" http://localhost:8080/alfresco/service/index > /dev/null 2>&1',shell=True)

    def reload_share(self):
        """ Reload share webscripts using it's webservice (with curl)"""
        self.call('curl --user admin:admin --data-urlencode "reset=all" http://localhost:8080/share/page/console > /dev/null 2>&1',shell=True)
        
    def sync_repo(self):
        """ rsync repo webscripts"""
        self.call("rsync -avh %s %s" % (path.join(self.repo,'config/'),path.join(self.tomcat,'shared/classes/')),shell=True)

    def sync_webapp(self):
        """ rsync webbapp, i.e. client side js,css and images """
        self.call("rsync -avh %s %s" % (path.join(self.share,'webapp/'),path.join(self.tomcat,'webapps/share/')),shell=True)
        
    def sync_share(self):
        """ rsync share webscripts"""
        self.call("rsync -avh %s %s" % (path.join(self.share,'config/'),path.join(self.tomcat,'shared/classes/')),shell=True)

    def sync_all(self):
        """Syncs both repo and share """
        self.sync_webapp()
        self.sync_repo()
        self.sync_share()

    def reload_all(self):
        """reloads share and repo """
        self.reload_repo()
        self.reload_share()
        
        
if __name__ == "__main__":
    import sys
    import argparse

    def using(tomcat,repo,share):
            print """Using:
tomcat: %s 
repo:   %s
share:   %s
        """ % (tomcat,repo,share)

    
    parser = argparse.ArgumentParser(description="Hotdeployment skript for alfresco")
    parser.add_argument('-q','--quiet' ,help="Disable notfications",default=False)
    parser.add_argument('-n','--notification',default="notify-send --hint=int:transient:1 %s",help="Notification binary, change on mac os x")
    parser.add_argument('-t','--tomcat',default="../alfresco-3.3.5/tomcat"     ,help="Path to tomcat, default is ../../tomcat")
    parser.add_argument('-s','--share' ,default="trunk/share/src/main/",help="Path to share src , default is ./share/src/main/")
    parser.add_argument('-r','--repo'  ,default="trunk/repo/src/main/" ,help="Path to tomcat, default is ./repo/src/main/")
    sub = parser.add_subparsers(help="Action subparser")


    sync = sub.add_parser('sync',help="Sync files with rsync")
    sync.add_argument('scope',choices=['repo','share','webapp','all'])

    def sync_func(args):
        using(args.tomcat,args.repo,args.share)
        a = Alfresco(args.tomcat,args.share,args.repo,not args.quiet and args.notification or None )
        a.sync(args.scope)
        a.notify("Synced %s" % args.scope)
        
    sync.set_defaults(func=sync_func)

    rel = sub.add_parser('reload',help="Reload wbescript with curl")
    rel.add_argument('scope',choices=['repo','share','all'])
    
    def rel_func(args):
        using(args.tomcat,args.repo,args.share)
        a = Alfresco(args.tomcat,args.share,args.repo,not args.quiet and args.notification or None )
        a.reload(args.scope)
        a.notify("Reloaded %s" % args.scope)

    rel.set_defaults(func=rel_func)

    both = sub.add_parser('both',help="Sync and reload")
    both.add_argument('scope',choices=['repo','share','all'])

    def both_func(args):
        using(args.tomcat,args.repo,args.share)
        a = Alfresco(args.tomcat,args.share,args.repo,not args.quiet and args.notification or None )
        a.sync(args.scope)
        a.reload(args.scope)
        a.notify("Synced and reloaded %s" % args.scope)

    both.set_defaults(func=both_func)

    args = parser.parse_args()
    args.func(args)

    
    
    

