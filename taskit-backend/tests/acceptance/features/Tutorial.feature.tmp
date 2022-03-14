Feature: Tutorial
    As a first time user of TaskIt, I want to see a tutorial on how to use the system, so that I can learn how to use the system.

    Background:
        Given The following users exist:
            | email                        | password      |
            | luke.skywalker@rebellion.com | jediknight457 |

    Scenario Outline: Sucessfully view tutorial before first login (normal flow)
        Given The user "<email>" is logged out
        And The user status "<has_seen_tutorial>" for user "<email>" is "false"
        When The user "<email>" attempts to play the tutorial
        Then The user "<email>" shall view the tutorial
        And The message "Tutorial viewed succesfully." shall be displayed
        And The user status "<has_seen_tutorial" for user "<email>" shall be "true" upon logging in

        Examples:
            | email                        | has_seen_tutorial |
            | luke.skywalker@rebellion.com | true              |

    Scenario Outline: Attempt to watch tutorial after being logged in (error flow)
        Given The user "<email>" is logged in
        And The user status "<has_seen_tutorial>" for user "<email>" is "true"
        When The user "<email>" attempts to view the tutorial
        Then The error message "You have already viewed the tutorial." shall be displayed

        Examples:
            | email                        | has_seen_tutorial |
            | luke.skywalker@rebellion.com | true              |

