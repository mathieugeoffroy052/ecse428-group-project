Feature: Create task
  As a user, I wish to create a task.

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
      | luke.skywalker@rebellion.com | jediknight457 |
    Given The following tasks exist:
      | email                    | task_name                        | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress |
      | anakin.skywalker@gar.gov | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | NULL       | NULL               | 100    | Not started |

  Scenario Outline: Successfully edit task filters (normal flow)
    Given "<email>" is logged in
    When The user "<email>" attempts to create the task "<name>", with due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then the task "<name>" shall exist in the system
    Then "<email>" shall have a task called "<name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "Not started"
    Then the number of tasks in the system shall be "5"
    And The message "Task created succesfully." shall be displayed

    Examples:
      | email                        | name            | due_date   | estimated_duration | weight |
      | obi-wan.kenobi@gar.gov       | Die a sad death | 2022-02-08 | 30                 | NULL   |
      | anakin.skywalker@gar.gov     | Be the worst    | 2022-02-09 | 1576800            | 100    |
      | luke.skywalker@rebellion.com | Kiss sister     | 2022-02-10 | 2                  | 10     |

  Scenario Outline: Create a task with invalid parameters (error flow)
    Given "<email>" is logged in
    When the user "<email>" attempts to create the task "<name>", with due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then no new task shall be created
    Then an error message "<error>" shall be raised

    Examples:
      | email                    | name         | due_date   | estimated_duration | weight | error                     |
      | obi-wan.kenobi@gar.gov   | NULL         | 2022-02-08 | 30                 | NULL   | The task must have a name |
      | anakin.skywalker@gar.gov |              | 2022-02-09 | 1576800            | 100    | The task must have a name |

  Scenario Outline: Attempt to create task without being logged in (error flow)
    Given All users are logged out
    When The user attempts to create the task of "<email>" called "<name>", due date "<due_date>", duration "<estimated_duration>", and weight "<weight>"
    Then The error message "Log in to edit your tasks." shall be displayed
    And The user shall be at the login page

    Examples:
      | email                  | name            | due_date   | estimated_duration | weight |
      | obi-wan.kenobi@gar.gov | Die a sad death | 2022-02-08 | 30                 | NULL   |
