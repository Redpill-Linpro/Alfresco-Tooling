#!/usr/bin/env python

import os
import fnmatch
import re
import fileinput

from subprocess import PIPE,Popen

"""
  Some hard coded paths to
  - the source files in the project
  - the base directory for the alfresco sources to differ from
  - the base directory for the alfresco sources to differ to
"""
project_src = '/Users/niklas/workspaces/workspace-vgr/alfresco-vgr'
old_src = '/Users/niklas/workspaces/workspace-alfresco/alfresco-enterprise-4.1.8'
new_src = '/Users/niklas/workspaces/workspace-alfresco/alfresco-enterprise-4.2.2'

"""
  Do a diff of two src trees, parse out file names, returns a dict
  with lists
  { new: [...], differ: [...], removed: [...] }
"""
def diff_file(old, new):
  # do a diff of old and new
  cmd = 'LC_ALL=C diff -rqw %s %s | grep -v .svn' % (old, new)    
  res = Popen(cmd, shell=True, stdout = PIPE).communicate()[0]

  differ  = ""
  new     = ""
  removed = ""
  
  for l in res.splitlines():
    if l.endswith('differ'):
      differ = l.split()[3]
    elif l.startswith('Only'):
      s = l.split()
      
      fpth = path.join(s[2][:-1],s[3])
      
      if 'alfresco-enterprise-4.1.6' in l:
        new = fpth
      else:
        removed = fpth
                
  return { 'differ': differ, 'removed': removed, 'new': new }

"""
  Find all files in a directory which contains the tag @overridden.
  Returns a list with dictionary objects:
  { 'old_file' : <path to the file in the old alfresco source tree>, 'new_file' : <path to the file in the new alfresco source tree>, 'project_file' : <path to the file in the project source tree>}
"""
def find_files(directory):
  result = []
  
  for path, dirs, files in os.walk(os.path.abspath(directory)):
    targetdir = os.path.join(directory, "target")
    gitdir = os.path.join(directory, ".git")
    
    for filename in fnmatch.filter(files, '*'):
      filepath = os.path.join(path, filename)
      filedir = os.path.dirname(filepath)

      istarget = filedir.startswith(targetdir)
      isgit = filedir.startswith(gitdir)

      if istarget:
        continue
        
      if isgit:
        continue
      
      overridden_path = None
      
      for line in fileinput.input(filepath):
        if not "@overridden" in line:
          continue

        overridden_path = re.search("(\s@overridden\s)(\S[^ ]+)", line).group(2).strip()
        
      if overridden_path == None:
        continue

      old_file = os.path.join(old_src, overridden_path)
      new_file = os.path.join(new_src, overridden_path)
        
      result.append({ "old_file" : old_file, "new_file" : new_file, "project_file" : filepath })
  
  return result
  
"""
  Compares a file and outputs some meld and kdiff3 commands
"""
def compare_file(file):
  old_file = file['old_file']
  new_file = file['new_file']
  project_file = file['project_file']
  
  diff = diff_file(old_file, new_file)
  
  if diff['removed'] != '':
    print 'meld %(old_file)s %(project_file)s' % file
    #print 'kdiff3 %(old_file)s %(project_file)s' % file
    print ''

  if diff['differ'] != '':
    print 'meld --diff %(old_file)s %(project_file)s --diff %(old_file)s %(new_file)s  --diff %(old_file)s %(project_file)s %(new_file)s --diff %(project_file)s %(new_file)s' % file
    #print 'kdiff3 %(old_file)s %(project_file)s' % file
    #print 'kdiff3 %(old_file)s %(new_file)s' % file
    # print 'ksdiff %(old_file)s %(project_file)s %(new_file)s' % file
    #print 'kdiff3 %(project_file)s %(new_file)s' % file
    #print ''
    
"""
  Compares a list of files and outputs some meld and kdiff3 commands
"""
def compare_files(files):
  for file in files: compare_file(file)
  
"""
  The actual "main" program
"""
files = find_files(project_src)

compare_files(files)