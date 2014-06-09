script:
{
	
	var dictionaryNodesQuery = "PATH:\"/app:company_home/app:dictionary//*\" AND TYPE:\"cm:content\"";
	var personNodesQuery = "TYPE:\"cm:person\"";
	var siteStoreName = "avm://sitestore";
		
	// check if a site has been provided, if so add the site content to the list...
	if (args.site == undefined  || args.site == null || args.site.length == 0) {
		
		// add all content in data dictionary to the list
		var nodes = search.luceneSearch(dictionaryNodesQuery);
		logger.log("Listing Data Dictionary nodes, found " + nodes.length + " nodes with potential content!");
		var dictionaryNodes = [];
		for (var i=0; i<nodes.length; i++) {
			push(dictionaryNodes, nodes[i], "cm:content");
		}
		model.dictionaryNodes = dictionaryNodes;
		logger.log("Done with Dictionary nodes");
		
		// add all cm:person content to the list
		
		var nodes = search.luceneSearch(personNodesQuery);
		logger.log("Listing User nodes, found " + nodes.length + " nodes with potential content!");;
		var personNodes = [];
		for (var i=0; i<nodes.length; i++) {
			push(personNodes, nodes[i], "cm:preferenceValues");
			push(personNodes, nodes[i], "cm:persondescription");
		}
		model.personNodes = personNodes;
		logger.log("Done with User nodes");
		
		//Ignore sites for now
		model.siteNodes = [];
	}
	else if(siteService.getSite(args.site) != null){
		var siteNodesQuery = "PATH:\"/app:company_home/st:sites/cm:" + args.site + "//*\" AND TYPE:\"cm:content\"";
		var nodes = search.luceneSearch(siteNodesQuery);
		logger.log("Listing nodes in site " + args.site + ", found " + nodes.length + " nodes with potential content!");
		var siteNodes = [];
		for (var i=0; i<nodes.length; i++) {
			push(siteNodes, nodes[i], "cm:content");
		}
		model.siteNodes = siteNodes;
		logger.log("Done with site nodes");
		
		model.dictionaryNodes = [];
		model.personNodes = [];
	}
	else {
		status.code = 404;
		status.message = "Could not find site " + args.site;
		status.redirect = true;
		break script;
	}
	
}

function addAvmNode(parentNode, nodes) {
	if(parentNode.isContainer && parentNode.childAssocs["cm:contains"] != null) {
		for (var i = 0; i<parentNode.childAssocs["cm:contains"].length; i++) {
			addAvmNode(parentNode.childAssocs["cm:contains"][i], nodes);
		}
	}
	else if(parentNode.isDocument){
		push(nodes, parentNode, "cm:content");
	}
} 

function push(urls, node, property) {
	try {
		var contentUrl = contentUrlResolver.getContentUrl(node.nodeRef, property);
		logger.log("Found url " + contentUrl + " for property " + property + " on node " + node.nodeRef);
		urls.push(contentUrl);
	}
	catch(e) {
		logger.log(e);
	}

}
