package org.redpilllinpro.alfresco.acs;

import org.alfresco.repo.jscript.BaseScopableProcessorExtension;
import org.alfresco.service.ServiceRegistry;
import org.alfresco.service.cmr.model.FileFolderService;
import org.alfresco.service.cmr.repository.NodeRef;

public class ContentUrlResolver extends BaseScopableProcessorExtension {

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
    	
    public String getContentUrl(final NodeRef nodeRef) throws java.lang.NullPointerException {
    	
    	final FileFolderService ffs = services.getFileFolderService();
    	
    	if(nodeRef != null) {
    		return ffs.getFileInfo(nodeRef).getContentData().getContentUrl();
    	}
    	
    	throw new NullPointerException("Could not resolve content url for node == null!");
    	
    }
    
    
}
