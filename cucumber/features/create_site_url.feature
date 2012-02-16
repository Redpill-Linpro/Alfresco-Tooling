Feature: Create site URL suggestion
  When we create a site we want a suitable URL constructed from
  the name we give to the site

  Background:
    Given that I am logged in as admin
    And that I created a testsite


  Scenario: Create site URL suggestion
    When i select "Create Site" from the menu "Sites"
    Then I should see a dialog named "Create Site"
    When I fill in "My test site" in the name input
    Then I should see "my-test-site" in the URL input
