# Test Plan

This is a test plan for the Bite Buddy Voice Assistant application.

## Purpose

The purpose is to do a task test: can users complete a certain task?

## Problem Statement

The objective of this activity is to verify if the user can use the application
to achieve a given task. We want to know if the application will help maintain
your kitchen inventory in a way that is more convenient than plain note-taking
(e.g., with pencil and paper, or in another app).

## User Profile

- General computer experience: The user is a digital native, has a fair
  understanding of computing technology, uses a cellphone every day for common
  tasks, and usually has access to a computer for more dedicated tasks (e.g., 1
  hour every other day).
- Age: 25 to 45 years old.
- Education: High School, have attended some College.
- Major: Business and Management, Social Sciences.
- General interests: Technology and Gadgets, Social Media, Fitness and Wellness.

## Test Design

The user will be instructed to complete the following tasks:

| Task   | Description                                                             | Time to Complete | Expected Output                                                                   |
| ------ | ----------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------------------------- |
| Task 1 | Tell Bite Buddy what you currently have in the fridge.                  | 60 seconds       | App should save user-provided items to the inventory                              |
| Task 2 | Ask Bite Buddy to list the products in the fridge.                      | 15 seconds       | App should list the products saved before in the fridge                           |
| Task 3 | Ask Bite Buddy where the ketchup is.                                    | 15 seconds       | App should say fridge or product not found                                        |
| Task 4 | Ask Bite Buddy to recommend a recipe with the products in your kitchen. | 60 seconds       | App should return a meal recipe with the products previously listed in the fridge |
| Task 5 | Tell Bite Buddy to forget the products in your fridge.                  | 30 seconds       | App should confirm it has forgotten the products in the fridge                    |

If the user can't execute the task, the tester shall provide additional
information about how to do it. This shall be done after 3 attempts, to prevent
interfering with the testing process and to prevent frustration from the user.

For each user, the following table will be completed:

| Task   | Expected Time to Complete | Task Completed | Actual Time to Complete |
| ------ | ------------------------- | -------------- | ----------------------- |
| Task 1 | -                         | -              | -                       |
| Task 2 | -                         | -              | -                       |
| Task 3 | -                         | -              | -                       |
| Task 4 | -                         | -              | -                       |
| Task 5 | -                         | -              | -                       |

After completing the tasks, the user will be instructed to complete the
following survey, using the Likert Scale to rate engagement level:

| Statement                                           | Strongly Disagree | Disagree | Somewhat Disagree | Neutral | Somewhat Agree | Agree | Strongly Agree |
| --------------------------------------------------- | ----------------- | -------- | ----------------- | ------- | -------------- | ----- | -------------- |
| The app is easy to use                              |                   |          |                   |         |                |       |                |
| I like the flow of the application                  |                   |          |                   |         |                |       |                |
| The app understands what I say                      |                   |          |                   |         |                |       |                |
| I would recommend this application to a friend      |                   |          |                   |         |                |       |                |
| The app responds quickly                            |                   |          |                   |         |                |       |                |
| The app helps me keep track of my kitchen inventory |                   |          |                   |         |                |       |                |
| The app provides clear instructions                 |                   |          |                   |         |                |       |                |
| The app integrates well with my daily routine       |                   |          |                   |         |                |       |                |
| The app is visually appealing                       |                   |          |                   |         |                |       |                |
| I like the assistant voice                          |                   |          |                   |         |                |       |                |

Finally, these open-ended questions will be asked to the user. The questions and
answers will be documented for further analysis:

1. What did you like most about using the Bite Buddy Voice Assistant?
1. What did you find most challenging or frustrating while using the app?
1. Do you have any suggestions for improving the Bite Buddy Voice Assistant?

## Reports

For every testing session, a report will be presented with the following:

1. Task completion rates, and time taken to complete the task.
1. Completed survey with Likert Scale Grading.
1. Notes from the open-ended questions.
