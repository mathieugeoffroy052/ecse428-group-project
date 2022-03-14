Feature: Add task to list
  To keep my task list in order
  As a user
  I wish to edit the properties of my tasks.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |

    Given The following tasks exist:
      | email                    | task_name                        | due_date   | estimated_duration | weight | state       | list_name |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started | null      |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | NULL       | NULL               | 100    | Not started | null      |

    Given The following lists exist:
      | list_name                        |
      | Students to train                |
      | Things for Anakin                |


  Scenario: Successfully add a task to a list (normal flow)
    Given "obi-wan.kenobi@gar.gov" is logged in
    When The user attempts to add the task of "obi-wan.kenobi@gar.gov" called "Train Anakin" to the list with name "Students to train"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Anakin" in the list with name "Students to train"
    And The message "Task added to list succesfully." shall be displayed

  Scenario: Successfully add a task to a list from another list (alternate flow)
    Given "obi-wan.kenobi@gar.gov" is logged in
    When The user attempts to add the task of "obi-wan.kenobi@gar.gov" called "Train Anakin" to the list with name "Things for Anakin"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Anakin" in the list with name "Things for Anakin"
    Then "obi-wan.kenobi@gar.gov" shall not have a task called "Train Anakin" in the list with name "Students to train"
    And The message "Task added to list succesfully." shall be displayed

  Scenario: Attempt to add a task to a list that does not exist (error flow)
    Given "__anakin-skywalker__" is logged in
    When The user attempts to edit add the task of "obi-wan.kenobi@gar.gov" called "Train Luke" to the list with name "Things for Luke"
    Then "obi-wan.kenobi@gar.gov" shall have a task called "Train Luke" in the list with name "null"
    And The message "Unable to add task to list" shall be displayed
