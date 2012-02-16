Feature: Login Share
  In order to use Alfresco Share at all
  As an information seeker
  I want to be able to login to Alfresco Share

  @foo
  Scenario: Login to Share
    Given I am on the login page
    And I have entered "admin" into the "username" field
    And I have entered "admin" into the "password" field
    When I click the "Login" button
    Then I should see "My Dashboard"
