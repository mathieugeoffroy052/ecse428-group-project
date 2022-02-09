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

  Scenario Outline: Successfully list all tasks (normal flow)
    Given "<username>" is logged in 
    Given user "<username>" has tasks "<task_names>", Then the view function will return this list of tasks (which may or may not be sorted)

    Examples: 
      | username             | task_names                                            |
      | __obi-wan-kenobi__   | Train Anakin, Train Luke                              | 
      | __anakin-skywalker__ | See through the lies of the Jedi, Kill the younglings |

  Scenario Outline: Unsuccessfully list all tasks (normal flow)
    Given "<username>" is logged in
    Given user "<username>" has tasks "<task_names>"
    Then the view function will not return this list of tasks
    Then the system shall report "<error>"

    Examples: 
      | username             | task_names                                            | error                    |
      | __obi-wan-kenobi__   | Train Anakin, See through the lies of the Jedi        | Wrong task listed        |
      | __anakin-skywalker__ | See through the lies of the Jedi                      | Missing task             |
