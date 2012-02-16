Given /^I am on the home page$/ do
  visit('/share') 
end

Given /^I am on the login page$/ do
  visit('/share/page/site-index')
end

Given /^I have entered "([^"]*)" into the "([^"]*)" field$/ do |text, field|
  fill_in field, :with => text
end

Given /^I want to get the version of Alfresco running$/ do
	@http_client = HTTPClient.new
	@http_client.set_auth("#{HOST}/alfresco/service", "admin", "admin")
	@response = @http_client.get("#{HOST}/alfresco/service/api/server")
end

Then /^I should see key "([^"]*)"$/ do |key|
  @response.body.should include(key)
end

When /^I click the "([^"]*)" button$/ do |button_text|
  click_button button_text
end

Then /^I should see "([^"]*)"$/ do |text|
  page.should have_content(text)
end




