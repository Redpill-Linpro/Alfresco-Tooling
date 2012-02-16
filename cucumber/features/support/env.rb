require 'capybara' 
require 'capybara/dsl' 
require 'capybara/cucumber'
require 'test/unit/assertions'
require 'httpclient'
require 'crack'

HOST = 'http://localhost:8080'
Capybara.default_driver = :selenium
Capybara.app_host = HOST 

World(Capybara)
