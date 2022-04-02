Feature: Add task to list
  To keep similar tasks together,
  As a user
  I wish to add tasks to a specific task list.

  Background:
    Given The following users exist:
      | email                    | password      |
      | obi-wan.kenobi@gar.gov   | jedimaster123 |

    Given The following lists exist:
      | list_name            | owner                  |  
      | Students to train    | obi-wan.kenobi@gar.gov |
      | Things for Luke      | obi-wan.kenobi@gar.gov |


  Scenario: Successfully add a task to a list (normal flow)
    Given "obi-wan.kenobi@gar.gov" is logged in
    When The user attempts to add the task of "obi-wan.kenobi@gar.gov" called "Train Anakin" to the list with name "Students to train"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Anakin" in the list with name "Students to train"
    Then "obi-wan.kenobi@gar.gov" shall not have a task called "Train Anakin" in the list with name "Things for Luke"
    And The message "Task created succesfully." shall be displayed
