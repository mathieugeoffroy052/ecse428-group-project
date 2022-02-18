Feature: View all tasks
  As a user, I wish to view all my tasks.

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

  Scenario Outline: Successfully list all tasks (normal flow)
    Given "<email>" is logged in
    When the user attempts to view all their tasks
    Then the view function will return the tasks "<task_names>" (which may or may not be sorted)

    Examples:
      | email                    | task_names                                            |
      | obi-wan.kenobi@gar.gov   | Train Anakin, Train Luke                              |
      | anakin.skywalker@gar.gov | See through the lies of the Jedi, Kill the younglings |
