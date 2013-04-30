<#list dictionaryNodes as d>
${d?replace('store://?', '', 'r')}
</#list>
<#list siteNodes as s>
${s?replace('store://?', '', 'r')}
</#list>
<#list personNodes as p>
${p?replace('store://?', '', 'r')}
</#list>
