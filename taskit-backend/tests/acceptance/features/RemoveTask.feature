Feature: Remove task
  As a user, I wish to be able to remove a task from my task list

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

  Scenario: A user successfully removes a task from their task list (normal flow)
    Given "<username>" is logged in to their account
    When "<username>" attempts to remove their "<task_name>" due on "<due_date>"
    Then "<username>"'s "<task_name>" task due on "<due_date>" shall be removed from the task list
    Then there shall be 1 less task in the task list

    Examples: 
      | username             | task_name                        | due_date   |
      | __obi-wan-kenobi__   | Train Anakin                     | 2022-02-06 |
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-07 |

  Scenario: A user tries to remove a task using invalid parameters (error flow)
    Given "<username>" is logged in to their account
    When "<username>" attempts to remove their "<task_name>" task due on "due_date"
    Then the system shall report "<error>"
    Then "<username>" shall have a "<task_name>" task due on "<due_date>" 
    Then there shall be 0 less tasks int the task list

    Examples: 
      | username             | task_name                        | due_date   |  error                                               |
      | __obi-wan-kenobi__   | Kill everyone                    | 2022-02-07 | You do not have a task by this name                  |
      | __anakin-skywalker__ | Train Anakin                     | 2022-02-07 | You do not have a task by this name                  |
      | __anakin-skywalker__ | See through the lies of the Jedi | 2022-02-22 | You do not have a task by this name due on this date |
      | __anakin-skywalker__ |                                  | 2022-02-07 | Invalid task name                                    |
      | __anakin-skywalker__ | NULL                             | 2022-02-07 | Invalid task name                                    |