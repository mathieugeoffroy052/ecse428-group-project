Feature: Update task status
  As a user, I wish to update the status of my task.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |
      | Anakin Skywalker | __anakin-skywalker__ | jediknight456 |
      | Luke   Skywalker | __luke-skywalker__   | jediknight457 |
    Given The following tasks exist:
      | username             | task_name                        | due_date   | estimated_duration | weight | state       |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started |
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress |
      | __anakin-skywalker__ | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    |
      | __obi-wan-kenobi__   | Train Luke                       | NULL       | NULL               | 100    | Not started |

  Scenario Outline: Successfully update the task status (normal flow)
    Given "<username>" is logged in
    When The user "<username>" attempts to update the task "<name>", with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<state>" to "new_state<>"
    Then the task "<name>" shall be updated to "<new_state>"
    Then "<username>" shall have a task called "<name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<new_state>"
    And The message "Task updated succesfully." shall be displayed

    Examples: 
      | username             | name                             | due_date   | estimated_duration | weight | state       | new_state   |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started | In progress |
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress | Complete    |
      | __anakin-skywalker__ | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    | Complete    |
      | __obi-wan-kenobi__   | Train Luke                       | NULL       | NULL               | 100    | Not started | In progress |

  Scenario Outline: Update task with invalid parameters (error flow)
    Given "<username>" is logged in
    When The user "<username>" attempts to update the status of the task "<name>", with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and status "<status>" to "<new_state>"  
    Then new task shall be updated
    Then an error message "<error>" shall be raised

    Examples: 
      | username             | name                             | due_date   | estimated_duration | weight    | state       | new_state   |error                     |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 |     1576800        | NULL      | Not started | In progress ||
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-07 |     30             | 75        | In progress | Complete    ||
      | __obi-wan-kenobi__   | Train Luke                       | NULL       |     NULL           | 100       | Not started | In progress ||

  Scenario Outline: Attempt to update a task without being logged in (error flow)
    Given All users are logged out
    When The user attempts to update the task of "<username>" called "<name>", due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then The error message "Log in to update your task status." shall be displayed
    And The user shall be at the login page

    Examples: 
      | username             | name                             | due_date   | estimated_duration | weight | new_state   |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | In progress |
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | Complete    |
