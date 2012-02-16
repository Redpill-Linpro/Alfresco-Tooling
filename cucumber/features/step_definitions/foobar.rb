Given /^that I am logged in as admin$/ do
    step 'I am on the login page'
    step 'I have entered "admin" into the "username" field'
    step 'I have entered "admin" into the "password" field'
    step 'I click the "Login" button'
    step 'I should see "My Dashboard"'
end

When /^i select "([^"]*)" from the menu "([^"]*)"$/ do |value, menu|
    click_button menu
    click_link value
end

Then /^I should see a dialog named "([^"]*)"$/ do |title|
    find('div.yui-panel').find('div.hd').should have_content(title)
end

When /^I fill in "([^"]*)" in the name input$/ do |value|
    fill_in "title", :with => value
end

Then /^I should see "([^"]*)" in the URL input$/ do |value|
  find('#alfresco-createSite-instance-shortName').value.should == value
end

