Feature: Remove task
  As a user, I wish to be able to delete my task list

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
    
    Given The following lists exist:
      | list_name           | owner                     |
      | train people        | obi-wan.kenobi@gar.gov    |
      | fight people        | obi-wan.kenobi@gar.gov    |
      | doubting the order  | anakin.skywalker@gar.gov  |
      | fight people        | anakin.skywalker@gar.gov  |

    Given The following tasks exist:
      | email                    | task_name                        | task_list_name     | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | train people       | 1576800    | 90                 | 40     |Not started  |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | train people       | NULL       | NULL               | 100    | Not started |
      | obi-wan.kenobi@gar.gov   | fight darth vader                | fight people       | NULL       | NULL               | 50     | Not started |
      | obi-wan.kenobi@gar.gov   | fight palpatine                  | fight people       | NULL       | 400                | 100    | Not started |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | doubting the order | 2022-02-07 | 30                 | 75     | In progress |
      | anakin.skywalker@gar.gov | Kill the younglings              | doubting the order | 2022-02-07 | 5                  | 25     | Complete    |
      | anakin.skywalker@gar.gov | fight darth maul                 | fight people       | 2022-02-07 | 30                 | 75     | In progress |
      | anakin.skywalker@gar.gov | Luke Skywalker                   | fight people       | 2022-02-07 | 5                  | 25     | Complete    |
  
  
  Scenario Outline: Successfully remove a task list (normal flow)
    Given "<email>" is logged in to their account
    When the user "<email>" attempts to delete the task list "<task_list_name>"
    Then the task list "<task_list_name>" shall be deleted
    And the user "<email>" shall have no task list "<task_list_name>"
    And The message "Task list deleted successfully." shall be displayed

    Examples:
      | email                   | task_list_name    |
      | obi-wan.kenobi@gar.gov  | train people      | 
      | obi-wan.kenobi@gar.gov  | fight people      |
      | anakinskywalker@gar.gov | doubting the order|
      | anakinskywalker@gar.gov | fight people      |   

  Scenario Outline: Attempt to delete a task list with invalid parameters (error flow)
    Given "<email>" is logged in to their account
    When the user "<email>" attempts to delete the task list "<task_list_name>"
    Then the no task list shall be deleted
    And an error message "<error>" shall be raised
    Examples:
      | email                        | task_list_name      | error                                 |
      | obi-wan.kenobi@gar.gov       | say memorable quotes| This task list does not exist.        |
      | anakin.skywalker@gar.gov     | remembering past    | This task list does not exist.        |
      | obi-wan.kenobi@gar.gov       | NULL                | This field is blank.                  |
      | anakin.skywalker@gar.gov     |                     | This field is blank.                  |

  Scenario Outline: Attempt to delete a task list with invalid parameters (error flow)
    Given All users are logged out
    When the user "<email>" attempts to delete the task list "<task_list_name>"
    Then the no task list shall be deleted
    And the error message "Authentication credentials were not provided." shall be displayed
    Examples:
      | email                        | task_list_name   |
      | obi-wan.kenobi@gar.gov       | train people     |
      | anakin.skywalker@gar.gov     | fight people     |
      