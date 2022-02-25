Feature: Calculate task Urgency
  As a user, I wish order tasks by Priority or Urgency

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
    Given The following tasks exist:
      | email                    | task_name                        | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-25 | 1576800            | 8      | Not started |
      | obi-wan.kenobi@gar.gov   | die                              | 2022-05-07 | 5                  | 7      | Not started |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | 2022-04-25 | 45                 | 5      | Not started |

  Scenario: Successfully order tasks (normal flow)
    Given "<email>" is logged in
    When The user attempts to order their tasks by "Priority"
    Then the ordering will be "Train Anakin, die, Train Luke"
    
    Examples:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
  
  Scenario: Successfully order tasks (alternate flow)
    Given "<email>" is logged in
    When The user attempts to order their tasks by "Importance"
    Then the ordering will be "Train Anakin, die, Train Luke"

    Examples:
    | email                        | password      |
    | obi-wan.kenobi@gar.gov       | jedimaster123 |


  
  Scenario: Successfully order tasks (alternate flow)
    Given "<email>" is logged in
    When The user attempts to order their tasks by "Urgency"
    Then the ordering will be "Train Anakin, Train Luke, die"

    Examples:
    | email                        | password      |
    | obi-wan.kenobi@gar.gov       | jedimaster123 |