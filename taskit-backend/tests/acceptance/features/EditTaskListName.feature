Feature: Edit Task List Name
    As a user of TaskIt, I would like to edit the name of my task lists, so that a new name can be given to my tasklist.

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
        Given The following task lists exist:
            | email                    | task_list_name    |
            | obi-wan.kenobi@gar.gov   | Training          |
            | anakin.skywalker@gar.gov | Save the universe |
        Given The following tasks in the task list exist:
            | email                    | task_list_name         | task_names                                            |
            | obi-wan.kenobi@gar.gov   | Training               | Train Anakin, Train Luke                              |
            | anakin.skywalker@gar.gov | Rebel against the Jedi | Kill the younglings, See through the lies of the Jedi |


    Scenario Outline: Successfully edit task list name (normal flow)
        Given "<email>" is logged in
        When The user "<email>" attempts to edit the task list name "<task_list_name>" to "<new_task_list_name>"
        Then The task list "<new_task_list_name>" shall exist in the system
        Then "<email>" shall have a task list named "<new_task_list_name>"
        And "<new_task_list_name>" shall include "<task_names>"
        And The message "Task list name updated succesfully." shall be displayed

        Examples:
            | email                    | new_task_list_name | task_names                                            |
            | obi-wan.kenobi@gar.gov   | Jedi Training      | Train Anakin, Train Luke                              |
            | anakin.skywalker@gar.gov | Join the dark side | Kill the younglings, See through the lies of the Jedi |

    Scenario Outline: Edit task list name with invalid task list name (error flow)
        Given "<email>" is logged in
        When The user "<email>" attempts to edit the task list name "<task_list_name>" to "<new_task_list_name>"
        Then "<email>" shall have a task list named "<task_list_name>"
        And "<task_list_name>" shall include "<task_names>"
        And The error message "<error>" shall be displayed

        Examples:
            | email                    | task_list_name         | new_task_list_name | task_names                                            | error                        |
            | obi-wan.kenobi@gar.gov   | Training               | NULL               | Train Anakin, Train Luke                              | This field may not be blank. |
            | anakin.skywalker@gar.gov | Rebel against the Jedi |                    | Kill the younglings, See through the lies of the Jedi | This field may not be blank. |

    Scenario Outline: Edit task list name without being logged in (error flow)
        Given All users are logged out
        When The user "<email>" attempts to edit the task list name "<task_list_name>" to "<new_task_list_name>"
        Then The error message "Authentication credentials were not provided." shall be displayed
        Then "<email>" shall have a task list named "<task_list_name>"
        And "<task_list_name>" shall include "<task_names>"
        And The user shall be at the login page


        Examples:
            | email                    | task_list_name         | new_task_list_name | task_names                                            |
            | obi-wan.kenobi@gar.gov   | Training               | Jedi Training      | Train Anakin, Train Luke                              |
            | anakin.skywalker@gar.gov | Rebel against the Jedi | Join the dark side | Kill the younglings, See through the lies of the Jedi |

