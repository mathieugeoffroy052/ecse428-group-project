Feature: Create task
  As a user, I wish to create a task.

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

  Scenario Outline: Successfully edit task filters (normal flow)
    Given "<username>" is logged in
    When The user "<username>" attempts to create the task "<name>", with due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then the task "<name>" shall exist in the system
    Then "<username>" shall have a task called "<name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "Not started"
    Then the number of tasks in the system shall be "5"
    And The message "Task created succesfully." shall be displayed

    Examples: 
      | username             | name            | due_date   | estimated_duration | weight    | 
      | __obi-wan-kenobi__   | Die a sad death | 2022-02-08 |     30             | NULL      |
      | __anakin-skywalker__ | Be the worst    | 2022-02-09 |     1576800        | 100       | 
      | __luke-skywalker__   | Kiss sister     | 2022-02-10 |     2              | 10        | 

  Scenario Outline: Create a task with invalid parameters (error flow)
    Given "<username>" is logged in
    When the user "<username>" attempts to create the task "<name>", with due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"    
    Then no new task shall be created
    Then an error message "<error>" shall be raised

    Examples: 
      | username             | name            | due_date   | estimated_duration | weight    | error                     |
      | __obi-wan-kenobi__   | NULL            | 2022-02-08 |     30             | NULL      | The task must have a name |
      | __anakin-skywalker__ |                 | 2022-02-09 |     1576800        | 100       | The task must have a name |
      | __obi-wan-kenobi__   | Train Anakin    | 2022-02-06 |     1576800        | 90        | This task already exists  |

  Scenario Outline: Attempt to create task without being logged in (error flow)
    Given All users are logged out
    When The user attempts to create the task of "<username>" called "<name>", due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then The error message "Log in to edit your tasks." shall be displayed
    And The user shall be at the login page

    Examples: 
      | username             | name            | due_date   | estimated_duration | weight    |
      | __obi-wan-kenobi__   | Die a sad death | 2022-02-08 |     30             | NULL      |
