Feature: Remove task
  As a user, I wish to be able to remove a task from my task list

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
    Given The following tasks exist:
      | email                    | task_name                        | due_date   | estimated_duration | weight | state       |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 | 1576800            | 90     | Not started |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 | 30                 | 75     | In progress |
      | anakin.skywalker@gar.gov | Kill the younglings              | 2022-02-07 | 5                  | 25     | Complete    |
      | obi-wan.kenobi@gar.gov   | Train Luke                       | NULL       | NULL               | 100    | Not started |

  Scenario Outline: A user successfully removes a task from their task list (normal flow)
    Given "<email>" is logged in to their account
    When "<email>" attempts to remove their "<task_name>" due on "<due_date>"
    Then The task of "<email>" called "<task_name>" shall be removed from the task list
    Then there shall be 1 less task in the task list

    Examples:
      | email                    | task_name                        | due_date   |
      | obi-wan.kenobi@gar.gov   | Train Anakin                     | 2022-02-06 |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-07 |

  Scenario Outline: A user tries to remove a task using invalid parameters (error flow)
    Given "<email>" is logged in to their account
    When "<email>" attempts to remove their "<task_name>" task due on "due_date"
    Then the system shall report "<error>"
    Then "<email>" shall have a "<task_name>" task due on "<due_date>"
    Then there shall be 0 fewer tasks in the task list

    Examples:
      | email                    | task_name                        | due_date   | error                                                |
      | obi-wan.kenobi@gar.gov   | Kill everyone                    | 2022-02-07 | You do not have a task by this name                  |
      | anakin.skywalker@gar.gov | Train Anakin                     | 2022-02-07 | You do not have a task by this name                  |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi | 2022-02-22 | You do not have a task by this name due on this date |
      | anakin.skywalker@gar.gov |                                  | 2022-02-07 | Invalid task name                                    |
