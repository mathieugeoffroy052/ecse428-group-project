Feature: Edit task
  As a user, I wish to edit the properties of my tasks.

  Background:
    Given The following users exist:
      | email                    | password      |
      | obi-wan.kenobi@gar.gov   | jedimaster123 |
      | anakin.skywalker@gar.gov | jediknight456 |
    Given The following tasks exist:
      | email                    | task_name                        | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress |
      | anakin.skywalker@gar.gov | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | NULL       | NULL               | 100    | Not started |

  Scenario Outline: Successfully edit task name (normal flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" to have name "<new_task_name>"
    Then "<email>" shall have a task called "<new_task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then "<email>" shall not have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The message "Task updated successfully." shall be displayed

    Examples:
      | email                    | task_name           | new_task_name      | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin        | Train someone else | 2022-02-06 | 1576800            | 90     | Not started |
      | anakin.skywalker@gar.gov | Kill the younglings | Kill the women     | 2022-02-07 | 5                  | 25     | Complete    |

  Scenario Outline: Successfully edit due date filter (alternative flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" with due date "<due_date>" to have due date "<new_due_date>"
    Then "<email>" shall have a task called "<task_name>" with due date "<new_due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then "<email>" shall not have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The message "Task updated successfully." shall be displayed

    Examples:
      | email                  | task_name    | new_due_date | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov | Train Anakin | 2024-02-06   | 2022-02-06 | 1576800            | 90     | Not started |
      | obi-wan.kenobi@gar.gov | Train Anakin | 2022-04-06   | 2022-02-06 | 1576800            | 90     | Not started |
      | obi-wan.kenobi@gar.gov | Train Anakin | 2022-02-08   | 2022-02-06 | 1576800            | 90     | Not started |

  Scenario Outline: Successfully edit estimated duration filter (alternative flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" with estimated duration "<estimated_duration>" to have estimated duration "<new_estimated_duration>"
    Then "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<new_estimated_duration>", weight "<weight>", and state "<state>"
    Then "<email>" shall not have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The message "Task updated successfully." shall be displayed

    Examples:
      | email                  | task_name    | new_estimated_duration | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov | Train Anakin | 1576801                | 2022-02-06 | 1576800            | 90     | Not started |

  Scenario Outline: Successfully edit weight filter (alternative flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" with weight "<weight>" to have new weight "<new_weight>"
    Then "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<new_weight>", and state "<state>"
    Then "<email>" shall not have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The message "Task updated successfully." shall be displayed

    Examples:
      | email                  | task_name    | new_weight | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov | Train Anakin | 100        | 2022-02-06 | 1576800            | 90     | Not started |

  Scenario Outline: Successfully edit notes field (alternative flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" with note "<note>" to have new note "<new_note>"
    Then "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", state "<state>", and note "<new_note>"
    Then "<email>" shall not have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", state "<state>", and note "<note>"
    Then The number of tasks in the system shall be "4"
    And The message "Task updated successfully." shall be displayed

    Examples:
      | email                  | task_name    | new_weight | due_date   | estimated_duration | weight | state       | note | new_note           |
      | obi-wan.kenobi@gar.gov | Train Anakin | 100        | 2022-02-06 | 1576800            | 90     | Not started |      | something else idk |

  Scenario Outline: Attempt to edit task with invalid parameters for task name (error flow)
    Given "<email>" is logged in
    When "<email>" attempts to edit the task name "<task_name>" to have name "<new_task_name>"
    Then "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then "<email>" shall not have a task called "<new_task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The error message "<error>" shall be displayed

    Examples:
      | email                  | task_name    | new_task_name | due_date   | estimated_duration | weight | state       | error                       |
      | obi-wan.kenobi@gar.gov | Train Anakin |               | 2022-02-06 | 1576800            | 90     | Not started | This field cannot be blank. |
      | obi-wan.kenobi@gar.gov | Train Anakin | NULL          | 2022-02-06 | 1576800            | 90     | Not started | This field cannot be blank. |

  Scenario Outline: Attempt to edit task name and filters without being logged in (error flow)
    Given All users are logged out
    When "<email>" attempts to edit the task name "<task_name>" to have name "<new_task_name>"
    Then "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then "<email>" shall not have a task called "<new_task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>"
    Then The number of tasks in the system shall be "4"
    And The error message "Authentication credentials were not provided." shall be displayed

    Examples:
      | email                    | task_name           | new_task_name      | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin        | Train someone else | 2022-02-06 | 1576800            | 90     | Not started |
      | anakin.skywalker@gar.gov | Kill the younglings | Kill the women     | 2022-02-07 | 5                  | 25     | Complete    |