
Given /^that I created a testsite$/ do
    #Check first if site is already created, then we need to remove it
    visit '/share/page/user/admin/dashboard'
    sleep 2 #ajax loading of sites often take time
    if page.has_content?('testsite')
        trs = page.all(:css, '.my-sites .yui-dt-data tr')
        for tr in trs
            link = tr.first(:css,'.site-title a')
            if link.text == 'testsite'
                #ok we got the right site, now lets find the "remove" link
                show = "YAHOO.util.Dom.addClass(YAHOO.util.Dom.get('" + tr['id'] + "'),'yui-dt-highlighted')"
                page.execute_script(show) #show the delete button
                tr.find(:css,'a.delete-site').click
                click_button 'Delete'
                click_button 'Yes'
                sleep 1
                break
            end
        end
    end 
    
    #create site
    click_button 'Sites'
    click_link 'Create Site'
    fill_in 'alfresco-createSite-instance-title', :with => 'testsite'
    find_button('alfresco-createSite-instance-ok-button-button').click
    #wait_until { page.has_no_content? 'Site is being' } #wait for dialog to close
    sleep 3 #give it time to create
    visit '/share/page/user/admin/dashboard' #clean slate
end



