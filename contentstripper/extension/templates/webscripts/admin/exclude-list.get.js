script:
{
	
	var dictionaryNodesQuery = "PATH:\"/app:company_home/app:dictionary//*\" AND TYPE:\"cm:content\"";
	var siteStoreName = "avm://sitestore";
	
	logger.log("site = " + args.site);

	// check if a site has been provided, if so add the site content to the exclude list...
	if (args.site == undefined  || args.site == null || args.site.length == 0 || siteService.getSite(args.site) == null) {
		logger.log("Skipping site content exclusion as no site was provided");
		model.siteNodes = [];
	}
	else {
		logger.log("Excluding content in site " + args.site);
		var siteNodesQuery = "PATH:\"/app:company_home/st:sites/cm:" + args.site + "//*\" AND TYPE:\"cm:content\"";
		var nodes = search.luceneSearch(siteNodesQuery);
		var siteNodes = [];
		for (var i=0; i<nodes.length; i++) {
			siteNodes.push(contentUrlResolver.getContentUrl(nodes[i].nodeRef));
		}
		model.siteNodes = siteNodes;
	}
	
	// add all content in data dictionary to the exclude list
	var nodes = search.luceneSearch(dictionaryNodesQuery);
	var dictionaryNodes = [];
	for (var i=0; i<nodes.length; i++) {
		logger.log("Adding " + nodes[i] + " to dictionary nodes");
		dictionaryNodes.push(contentUrlResolver.getContentUrl(nodes[i].nodeRef));
	}
	model.dictionaryNodes = dictionaryNodes;
	
	//add all content in avm:sitestore to the exclude list (to keep site settings correct)
	var xpathnodes = search.xpathSearch(siteStoreName, "/");
	var siteStoreNodes = [];
	if(xpathnodes[0] == undefined || xpathnodes[0] == null) {
		status.code = 404;
		status.message = "AVM store " + siteStoreName + " not found.";
		status.redirect = true;
		break script;
	}
	else {
		logger.log("Found AVM store " + siteStoreName);
		addAvmNode(xpathnodes[0], siteStoreNodes);		
	}
	
	model.avmNodes = siteStoreNodes;
}

function addAvmNode(parentNode, nodes) {
	if(parentNode.isContainer && parentNode.childAssocs["cm:contains"] != null) {
		for (var i = 0; i<parentNode.childAssocs["cm:contains"].length; i++) {
			addAvmNode(parentNode.childAssocs["cm:contains"][i], nodes);
		}
	}
	else if(parentNode.isDocument){
		nodes.push(contentUrlResolver.getContentUrl(parentNode.nodeRef));
	}
} 