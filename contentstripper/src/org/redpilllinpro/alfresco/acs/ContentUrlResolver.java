package org.redpilllinpro.alfresco.acs;

import org.alfresco.repo.jscript.BaseScopableProcessorExtension;
import org.alfresco.service.ServiceRegistry;
import org.alfresco.service.cmr.model.FileFolderService;
import org.alfresco.service.cmr.model.FileInfo;
import org.alfresco.service.cmr.repository.NodeRef;
import org.apache.log4j.Logger;

public class ContentUrlResolver extends BaseScopableProcessorExtension {

	private final static Logger LOG = Logger.getLogger(ContentUrlResolver.class);
	
	/** Repository Service Registry */
    private ServiceRegistry services;

    /**
     * Set the service registry
     * 
     * @param serviceRegistry the service registry
     */
    public void setServiceRegistry(ServiceRegistry serviceRegistry)
    {
        this.services = serviceRegistry;
    }
    	
    public String getContentUrl(final NodeRef nodeRef) {
    	
    	final FileFolderService ffs = services.getFileFolderService();
    	
    	if(nodeRef != null) {
    		final FileInfo fileInfo = ffs.getFileInfo(nodeRef);
    		if(fileInfo != null && fileInfo.getContentData() != null) {
    			return ffs.getFileInfo(nodeRef).getContentData().getContentUrl();
    		}
    		else {
    			LOG.warn("Could not get content data url for NodeRef " + nodeRef);
    		}
    	}
    	
    	LOG.warn("Could not resolve content url for node == null!");
    	
    	return "";
    	
    }
    
    
}
