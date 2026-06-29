# Iteration Report 2

## Team Responsibilities
- **Otabek**:
  - User Stories to Complete:
    - As a user, I want to enter my body parameters so that the web app could adjust the weight of equipment for me
    
  - Completed Tasks:
    - All tasks were completed with a way to store the data. 

- **Logan**:
  - User Stories to Complete:
    - As a new user, I want to submit my schedule through filling out the form so that I had the schedule of my workouts on the website
  - Completed Tasks:
    - All tasks were completed, requires minor tweaks for inputting time frames and no duplicate entries. 

- **Karsten**:
  - User Stories to Complete:
    - As a new user, I want to take the background questionnaire where the web app would ask me about the experience, time, and my goals so that the application could give me the appropriate exercises
 
  - Completed Tasks:
    - All task Complete with added columns to store the data in SQL

- **Jacob**:
  - User Stories to Complete:
    - As an existing user, I want to have "Workout" button on the home page on the day of the workout so that the web application could give me the exercises with according to my user profile
    - As an existing user, I want to log in on the website so that I could access my profile and the features of the web app
  - Completed Tasks:
    - All tasks were completed. workout button does not display a person's workout yet since there is no way to format a workout yet. 

- **Jimmy**:
  - User Stories to Complete:
    - As a user, I want to have "Forgot Password" button on the login page so that I could access my account and change the password in case I forgot it
    - As an Admin I want to hash user passwords for better security to protect my user's privacy and information.
    - As an existing user, I want to have a schedule displayed on the home page so that I could easily see when I need to work out.
  - Completed Tasks:
    - All tasks were completed except for the Forgot Password button. there was alot of confusion throughout the group if 
      we can do this or not which after talking to a TA and the Professor we decided to delay that task to next iteration.
      with the addition to learning how to hash passwords in class we also decided to add that as a task for this iteration. 


## Summary of completed work
- We have completed the majority of task related to making a user's profile for the app. this will help us make 
  the other app functions to be customized by the user's data from the questionnaire. 

## Planned but unfinished work 
- Change Password Button
- workout button (no data for making a workout yet)

## Issues and difficulties
- besides the difficulties that came with the Change password button and being unsure what to do there were no problems. 
- other problem we have is not having foundations to go on to what task we want to complete in further iterations. so we need 
  to take some time to develop layouts for the user part of the app so we can build the functionalities further. 

## Design adjustments
- We need to make sure the formatting of all pages look similar to each other to make it look more professional. 

## Helpful tools or processes
- for the future we need to make sure we let our teammates know when they are merging files into the main so all other group members
  can prepare and adept to the new changes appropriately 

---

# Plan for upcoming iterations

## Planned user stories and tasks

### Iteration 3

- **Jacob**:
  - **User story**: As a user, I want to see and edit my overall schedule when needed
  - **Tasks**:
      - develop the layout for the schedule page for the user
      - make it so days they are working out are highlighted 
      - Create a "Change Schedule" button on top right corner
      - Add functionality to input new tasks details(time and title) in a day selected
      - Add the "Save" button to update the schedule
      - Ensure the updated schedule is visible
      
- **Jimmy**:
  - **User story**: As a user, I want to have "Forgot Password" button on the login page so that I could access my account and change the password in case I forgot it
    - **Tasks**:
      - Create a form where users input their email to receive a temporary passcode
      - Implement a functionality to validate the passcode and allow users to confirm a new password
      - Redirect to the homepage after successful password reset
      
- **Karsten**:
  - **User story**:  As a User, I want to be able to track my progress as I work out. 
    - **Tasks**:
      - develop layout for progress page
      - have the user be able to pull data from pass workouts by data and exercise
      - have user be able to compare current body weight to past body weight 
      
- **Logan**:
  - **User story**: As a new user, I want the website to account for my availability when creating my workout schedule for the month. 
  - **Tasks**:
      - Design a schedule input form with fields for day, time and task title
      - Implement a functionality to save tasks on the chosen day, and allow the user to continue adding tasks for each day
      - Confirm that tasks of all days are saved and proceed to Entering Body Parameters
      - have the application determine what days the user should work out based on availability 
      
- **Otabek**:
  - **User story**: As a user, I want to see my workout for the day when I login. 
    - **Tasks**:
      - Edit layout of user home page to have their workout displayed with workout button 
      - highlight days of the current week when they are gonna workout. 

- **Jimmy**:
  - **User story**: As an existing user, I want to be able to set profile settings and customize my profile 
  - **Tasks**:
      - make profile settings for the user
      - make it so the user can change info like their password, username, email, or past responses to the questionare 
      - have a verification for changing new profile info with username, password, and email. 
      

    

### Iteration 4
  - **User story**: As an existing user, I want to have a video tutorial for each of the exercises given so that I knew how to do them
    - **Tasks**:
      - Implement video tutorials next to each of the exercises given

  - **User story**: As an existing user, I want to have an ability to input the time and the weight I used doing the exercise so that the web application could record it
    - **Tasks**:
      - Create an input form for recording time and weight used during each exercise
      - In case of the wrong input, notify the one to change it in the appropriate format 


  - **User story**: As an existing user, I want to see the time I spent, and weight I used over time so that I could keep track of my progress 
    - **Tasks**:
      - Create a functionality to display the time spent on past workouts
      - Display the weights used in the exercises over time

  
### Iteration 5
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

  

