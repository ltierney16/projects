# ITERATION PLAN 1

## User Stories Week 1
- As a new user, I would like to have a general info web pages so that I knew more about the Workout planner and why I need it
  - Home page 
  - Navigation bar 
  - About us section
  - Features section
  - Sign Up button 
  - Log In button
  

### Otabek
- Create the main website layout in layout.html, including elements like the header, footer and navigation bar
- Write unit and integration tests in app_tests.py
- Define the database schema in schema.sql, including tables and columns
- Configure workflows in a .yml file for GitHub Actions


### Logan
- Create homepage.html and design the layout for the homepage
- Include general information about the Workout Planner
- Integrate the homepage with the Flask application (app.py)


### Karsten
- Create aboutus.html and design the "About Us" page
- Include information about team members, project goals, and values
- Integrate the "About Us" page with the Flask application (app.py)


### Jacob
- Create features.html and design the "Features" page
- List all features of the Workout Planner with descriptions
- Integrate the "Features" page with the Flask application (app.py)


### Jimmy
- Create login.html and design the login page
- Create signup.html and design the signup page
- Integrate the login and signup pages with the Flask application (app.py)



# ITERATION PLAN 2

## User Stories Week 2
 **Jacob**:
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
    
### Creating Profile
- As a new user, I want to create my own profile on the web application, so that it could create a workouts schedule, 
give me the appropriate exercises with according to my body parameters and experience and save my progress which I would like to keep track of
    - Registering on the website 
    - Log In on the website 
    - Forgot the password
  

# ITERATION PLAN 3

## User Stories Week 3

### Creating Profile
- As a new user, I want to create my own profile on the web application, so that it could create a workouts schedule, 
give me the appropriate exercises with according to my body parameters and experience and save my progress which I would like to keep track of
    - Background Questionnaire 
    - Submitting the schedule through manual inputting
    - Entering body parameters
