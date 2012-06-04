package org.springframework.extensions.webscripts;
/**
    This file is part of NewRelic Module for Alfresco.

    NewRelic Module for Alfresco is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with NewRelic Module for Alfresco.  If not, see <http://www.gnu.org/licenses/>.
**/

import org.springframework.extensions.webscripts.processor.BaseProcessorExtension;
import org.apache.log4j.Logger;

/**
 * Bean for tracking browser timings with newrelic
 * Based on blog entry: http://blog.alfrescian.com/?p=174 
 * 
 * @author Marcus Svensson - Redpill Linpro AB <marcus.svensson@redpill-linpro.com>
 *
 */
public class NewRelicMethod extends BaseProcessorExtension {
	private static final Logger logger = Logger.getLogger(NewRelicMethod.class);

	public NewRelicMethod() {
		super();
		if (logger.isInfoEnabled()) {
			logger.info("NewRelic module initialized");
		}
	}
	
    public String getBrowserTimingHeader() {
    	return com.newrelic.api.agent.NewRelic.getBrowserTimingHeader();
	}

 	public String getBrowserTimingFooter() {
		return com.newrelic.api.agent.NewRelic.getBrowserTimingFooter();
	}
}
