Feature: Get information about the Alfresco server
  In order to know which version of Alfresco we are using
  As a REST geek
  I want to be able to check the Alfresco version using REST

  Scenario: Get Alfresco version
    Given I want to get the version of Alfresco running
    Then I should see key "edition"
    And I should see key "version"
    And I should see key "schema"
