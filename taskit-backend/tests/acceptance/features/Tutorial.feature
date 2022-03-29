Feature: View Tutorial
    As a first time user of TaskIt, I want to see a tutorial on how to use the system, so that I can learn how to use the system.

    Background:
        Given There exists a user with email "luke.skywalker@rebellion.com" and password "jediknight457"

    Scenario: Sucessfully view tutorial after first login (normal flow)
        Given The tutorial status <has_seen_tutorial> for the user with email "luke.skywalker@rebellion.com" is "false"
        When The user attempts to log in with email address "luke.skywalker@rebellion.com" and password "jediknight457"
        Then The user shall view the tutorial
        And The tutorial status <has_seen_tutorial> for the user with email "luke.skywalker@rebellion.com" shall be "true"

    Scenario: Attempt to watch tutorial after next login (error flow)
        Given The tutorial status <has_seen_tutorial> for the user with email "luke.skywalker@rebellion.com" is "true"
        When The user attempts to log in with email address "luke.skywalker@rebellion.com" and password "jediknight457"
        Then The user shall not view the tutorial
        And The tutorial status <has_seen_tutorial> for the user with email "luke.skywalker@rebellion.com" shall be "true"