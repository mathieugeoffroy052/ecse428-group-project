Feature: Tutorial
    As a first time user of TaskIt, I want to see a tutorial on how to use the system, so that I can learn how to use the system.

    Background:
        Given The following users exist:
            | email                        | password      |
            | luke.skywalker@rebellion.com | jediknight457 |
        Given The following status:
            | email                        | has_seen_tutorial |
            | luke.skywalker@rebellion.com | false             |
        Given The following users are logged out:
            | email                        | password      |
            | luke.skywalker@rebellion.com | jediknight457 |

    Scenario Outline: Sucessfully view tutorial before first login (normal flow)
        When The user "<email>" attempts to play the tutorial
        Then The user shall view the tutorial
        And The message "Tutorial viewed succesfully." shall be displayed
        And the user status "<has_seen_tutorial" shall be "true" upon logging in

        Examples:
            | email                        | has_seen_tutorial |
            | luke.skywalker@rebellion.com | true              |

    Scenario Outline: Sucessfully skip tutorial (alternative flow)
        When The user "<email>" attempts to skip the tutorial
        Then The message "Tutorial skipped succesfully." shall be displayed
        And the user status "<has_seen_tutorial" shall be "true" upon logging in

        Examples:
            | email                        | has_seen_tutorial |
            | luke.skywalker@rebellion.com | true              |

