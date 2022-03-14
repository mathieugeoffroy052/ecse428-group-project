Feature: Add task to list
  To keep my task list in order
  As a user
  I wish to edit the properties of my tasks.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |

    Given The following tasks exist:
      | username             | task_name                        | due_date   | estimated_duration | weight | list_name |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | null    |
      | __obi-wan-kenobi__   | Train Luke                       | NULL       | NULL               | 100    | null    |

    Given The following lists exist:
      | list_name                        |
      | Students to train                |
      | Things for Anakin                |


  Scenario: Successfully add a task to a list (normal flow)
    Given "__obi-wan-kenobi__" is logged in
    When The user attempts to add the task of "__obi-wan-kenobi__" called "Train Anakin" to the list with name "Students to train"
    Then "__obi-wan-kenobi__" shall have a task called "Train Anakin" in the list with name "Students to train"
    And The message "Task added to list succesfully." shall be displayed

  Scenario: Successfully add a task to a list from another list (alternate flow)
    Given "__obi-wan-kenobi__" is logged in
    When The user attempts to add the task of "__obi-wan-kenobi__" called "Train Anakin" to the list with name "Things for Anakin"
    Then "__obi-wan-kenobi__" shall have a task called "Train Anakin" in the list with name "Things for Anakin"
    Then "__obi-wan-kenobi__" shall not have a task called "Train Anakin" in the list with name "Students to train"
    And The message "Task added to list succesfully." shall be displayed

  Scenario: Attempt to add a task to a list that does not exist (error flow)
    Given "__anakin-skywalker__" is logged in
    When The user attempts to edit add the task of "__obi-wan-kenobi__" called "Train Luke" to the list with name "Things for Luke"
    Then "__obi-wan-kenobi__" shall have a task called "Train Luke" in the list with name "null"
    And The message "Unable to add task to list" shall be displayed
