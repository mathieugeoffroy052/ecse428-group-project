Feature: Add task to list
  To keep my task list in order
  As a user
  I wish to edit the properties of my tasks.

  Background:
    Given The following users exist:
      | email                    | password      |
      | obi-wan.kenobi@gar.gov   | jedimaster123 |

    Given The following tasks exist:
      | email                    | task_name        | due_date   | estimated_duration | weight | state       | list_name         |
      | obi-wan.kenobi@gar.gov   | Train Anakin     | 2022-02-06 | 1576800            | 90     | Not started | NULL              |
      | obi-wan.kenobi@gar.gov   | Train Luke       | NULL       | NULL               | 100    | Not started | Students to train |

    Given The following lists exist:
      | list_name            | owner                  |  
      | Students to train    | obi-wan.kenobi@gar.gov |
      | Things for Luke      | obi-wan.kenobi@gar.gov |


  Scenario: Successfully add a task to a list (normal flow)
    Given "obi-wan.kenobi@gar.gov" is logged in
    When The user attempts to add the task of "obi-wan.kenobi@gar.gov" called "Train Anakin" to the list with name "Students to train"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Anakin" in the list with name "Students to train"
    And The message "Task created succesfully." shall be displayed

  Scenario: Successfully add a task to a list from another list (alternate flow)
    Given "obi-wan.kenobi@gar.gov" is logged in
    When The user attempts to add the task of "obi-wan.kenobi@gar.gov" called "Train Luke" to the list with name "Things for Luke"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Luke" in the list with name "Things for Luke"
    Then "obi-wan.kenobi@gar.gov" shall not have a task called "Train Luke" in the list with name "Students to train"
    And The message "Task created succesfully." shall be displayed
