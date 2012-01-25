Instructions for use
--------------------
This is a tool used to get a list with content paths in alf_data for content needed to preserve consistency in the repository.
The content paths listed are 
1) All content in Company Home/Data Dictionary
2) All content in avm:sitestore
or
3) If a site is provided: all content in the site

The tool is exposed as a webscript on /alfresco/service/admin/excludelist you could also add the optional parameter site to
include content from a particular site in the path list. Example: /alfresco/service/admin/excludelist?site=testsite will return 
something like:

2011/10/18/15/16/fb4a374d-1fe3-4a4e-a16d-df2544f5864c.bin
2011/10/18/15/16/536f0e41-17e6-479e-805a-2bf7c95363d9.bin
2011/10/18/15/16/b0537345-1ace-473c-9c14-9b42f03e2e91.bin
2011/10/18/15/16/68563683-d41c-432a-9bf2-be0e31381a40.bin
2011/10/18/15/16/94826d2e-387b-43ae-9b1d-5edc34549757.bin
2011/10/18/15/16/9e6749fb-d41a-4586-8e83-467e03517e53.bin
2011/10/18/15/16/59485495-c409-43ed-9752-be89b975930b.bin
2011/10/18/15/16/d80fcd79-8235-46ae-aaf3-65c814f288ef.bin
...

Instructions for deployment
---------------------------
* Put the content of the extension folder (or zip) in tomcat/shared/classes/alfresco/extension
* Put the ContentUrlResolver.jar in tomcat/webapps/alfresco/WEB-INF/lib
* Restart Tomcat