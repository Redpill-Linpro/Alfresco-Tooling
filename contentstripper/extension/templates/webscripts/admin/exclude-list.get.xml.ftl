<#list dictionaryNodes as d>
${d?replace('store://?', '', 'r')}
</#list>
<#list siteNodes as s>
${s?replace('store://?', '', 'r')}
</#list>
<#list avmNodes as a>
${a?replace('store://?', '', 'r')}
</#list>