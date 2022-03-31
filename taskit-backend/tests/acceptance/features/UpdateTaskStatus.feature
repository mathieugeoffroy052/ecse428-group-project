Feature: Update task status
  As a user, I wish to update the status of my task.

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

  Scenario Outline: Successfully update the task status (normal flow)
    Given "<email>" is logged in
    When The user attempts to update the status of the task "<task_name>" to "<new_state>"
    Then the task "<task_name>" shall be updated to "<new_state>"
    And "<email>" shall have a task called "<task_name>" with due date "<due_date>", duration "<estimated_duration>", weight "<weight>", and state "<new_state>"

    Examples:
      | email                    | task_name                        | due_date   | estimated_duration | weight | new_state   |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | In progress |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | Complete    |
      | anakin.skywalker@gar.gov | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | NULL       | NULL               | 100    | In progress |

  Scenario Outline: Attempt to update a task without being logged in (error flow)
    Given All users are logged out
    When The user attempts to update the status of the task "<task_name>" to "<new_state>"
    Then The error message "Authentication credentials were not provided." shall be displayed
    And The user shall be at the login page

    Examples:
      | email                    | task_name                        | due_date   | estimated_duration | weight | old_state   | new_state   |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started | In progress |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress | Complete    |
