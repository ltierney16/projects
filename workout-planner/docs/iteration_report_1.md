# Iteration Report 1

## Team Responsibilities
- **Otabek**:
  - Responsibilities:
    - Create the main website layout in layout.html, including elements like the header and navigation bar
    - Write unit tests in app_tests.py and configure workflows in a .yml file for GitHub Actions
    - Define the database schema in schema.sql, including tables and columns
  - Completed Tasks:
    - All tasks were completed

- **Logan**:
  - Responsibilities:
    - Create and design the layout for the homepage, including general information about the Workout Planner
    - Integrate homepage.html with app.py
  - Completed Tasks:
    - All tasks were completed

- **Karsten**:
  - Responsibilities:
    - Create and design the "About Us" page, including information about team members, project goals, and values
    - Integrate aboutus.html with app.py
  - Completed Tasks:
    - All tasks were completed

- **Jacob**:
  - Responsibilities:
    - Create and design the "Features" page, listing all features of the Workout Planner with descriptions
    - Integrate features.html with app.py
  - Completed Tasks:
    - All tasks were completed

- **Jimmy**:
  - Responsibilities:
    - Create and design the login and signup pages
    - Integrate login.html and signup.html with app.py
    - Implement SQL to store user data when creating an account in the sign-up process, storing the user's username, password and email
    - Redirect users to log-in page after successful registration
  - Completed Tasks:
    - All tasks were completed


## Summary of completed work
- We have completed the infrastructure and basic layout of Workout planner

## Planned but unfinished work 
- All planned was finished

## Issues and difficulties
- No issues/difficulties

## Design adjustments
- We have to improve the style of Workout planner, matching all pages/sections to be consistent

## Helpful tools or processes
- None

---

# Plan for upcoming iterations

## Planned user stories and tasks

### Iteration 2

- **Jacob**:
  - **User story**:As an existing user, I want to log in on the website so that I could access my profile and the features of the web app
    - **Tasks**:
      - Implement input fields for email and password
      - Validate login credentials against the database
      - Redirect users to the homepage after successful login
      
- **Jimmy**:
  - **User story**: As a user, I want to have "Forgot Password" button on the login page so that I could access my account and change the password in case I forgot it
    - **Tasks**:
      - Create a form where users input their email to receive a temporary passcode
      - Implement a functionality to validate the passcode and allow users to confirm a new password
      - Redirect to the homepage after successful password reset
      
- **Karsten**:
  - **User story**: As a new user, I want to take the background questionnaire where the web app would ask me about the experience, time, and my goals so that the application could give me the appropriate exercises
    - - **Tasks**:
      - Create a questionnaire form to collect details on user experience, time commitment and fitness goal
      - Save responses to the user profile and allow user to submit the schedule 
      
- **Logan**:
  - **User story**: As a new user, I want to submit my schedule through filling out the form so that I had the schedule of my workouts on the website
    - **Tasks**:
      - Design a schedule input form with fields for day, time and task title
      - Implement a functionality to save tasks on the chosen day, and allow the user to continue adding tasks for each day
      - Confirm that tasks of all days are saved and proceed to Entering Body Parameters
      
- **Otabek**:
  - **User story**: As a user, I want to enter my body parameters so that the web app could adjust the weight of equipment for me
    - **Tasks**:
      - Create a form to input body weight, height and body type
      - Implement a save functionality to store these parameters 
      - Redirect to the homepage once the information is saved

- **Jimmy**:
  - **User story**: As an existing user, I want to have a schedule displayed on the home page so that I could easily see when I need to work out
    - **Tasks**:
      - Implement the schedule into the homepage
      - Create a "Workout" button on workout days
      - Display the next workout date if it is not a workout day or simply include "Rest Day"

- **Jacob**:
  - **User story**: As an existing user, I want to have "Workout" button on the home page on the day of the workout so that the web application could give me the exercises with according to my user profile
    - **Tasks**:
      - Add functionality to the "Workout" button by displaying the exercises on that day
      - Show exercise details like time and weight for each exercise
    

### Iteration 3
  - **User story**: As an existing user, I want to have a video tutorial for each of the exercises given so that I knew how to do them
    - **Tasks**:
      - Implement video tutorials next to each of the exercises given

  - **User story**: As an existing user, I want to have an ability to input the time and the weight I used doing the exercise so that the web application could record it
    - **Tasks**:
      - Create an input form for recording time and weight used during each exercise
      - In case of the wrong input, notify the one to change it in the appropriate format 

  - **User story**: As an existing user, I want to have an ability modify the schedule so that the web application create a new one for me using the data provided
    - **Tasks**:
      - Create a "Change Schedule" button on top right corner
      - Add functionality to input new tasks details(time and title) in a day selected
      - Add the "Save" button to update the schedule
      - Ensure the updated schedule is visible

  - **User story**: As an existing user, I want to see the time I spent, and weight I used over time so that I could keep track of my progress 
    - **Tasks**:
      - Create a functionality to display the time spent on past workouts
      - Display the weights used in the exercises over time

  
### Iteration 4
  - **User story**: As an existing user, I want to have an ability to view my profile, so that I could modify my body parameters, and change the login information
    - **Tasks**:
      - Create a setting section on the navigation bar
      - Implement forms for editing body parameters, such as weight or height
      - Develop a form with prepopulated log in information and password 
      - Add logout functionality in settings section 
      
  - **User story**: As any user, I want to have the web application notify me in case I input invalid format for the specific data in the forms, so that I knew how to input the correct one
    - **Tasks**:
      - In case of input the invalid form of data, allow the user to see the input field is red bordered 
      - Let the user be able to see the message from the web app, then input the valid format
      - After completing the form, ensure data is saved

  - **User story**: As any user, I want to have an ability to integrate my Google Calendar with my schedule in the web application, so that the web application could create the schedule of the workouts and integrate it in the Google Calendar 
    - **Tasks**:
      - Develop a functionality for users to link their google calendar with the app

  

