package org.redpilllinpro.alfresco.acs;

import org.alfresco.repo.jscript.BaseScopableProcessorExtension;
import org.alfresco.service.ServiceRegistry;
import org.alfresco.service.cmr.repository.ContentReader;
import org.alfresco.service.cmr.repository.ContentService;
import org.alfresco.service.cmr.repository.NodeRef;
import org.alfresco.service.namespace.NamespaceService;
import org.alfresco.service.namespace.QName;

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
    	
    public String getContentUrl(final NodeRef nodeRef, final String qname) throws Exception {
    	
    	if(nodeRef != null) {
    		final NamespaceService namespaceService = services.getNamespaceService();
    		final QName propertyQName = QName.createQName(qname, namespaceService);
    	
    		if(services.getNodeService().getProperty(nodeRef, propertyQName) == null) {
    			throw new Exception("Could not find property " + propertyQName + " on node " + nodeRef);
    		}
    		
    		final ContentService contentService = services.getContentService();
    		final ContentReader reader = contentService.getReader(nodeRef, propertyQName);
    		if(reader != null && reader.exists()) {
    			return reader.getContentUrl();
    		}
    		else {
    			throw new Exception("Could not resolve content url for NodeRef " + nodeRef + " and property " + propertyQName);
    		}
    	}
    	
    	throw new Exception("Could not resolve content url when NodeRef is 'null'! Is index corrupt?");
    	
    }
    
    
}
