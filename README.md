# COS-333-ReEats

Project Overview Document:
https://docs.google.com/document/d/1DmfWCgKmDYtlEXu_Hpge4d450yej2rcl9hXaL_5_mEE/edit?usp=sharing


Code Documentation: 
All files with prefix 'rest' are restaurant specific and all files with prefix 'user' are user specific. 

.py files 
resthtml.py: main controller for the webapp (this file is called in terminal to launch)

restdatabase.py : the database search query code for restaurants (menuSearchRest) AND users (menuSearchUser)

menuResult.py : creates an obj of type MenuResult

.html files 
user_fp.html : first page of website (seen by users and restaurants)
rest_fp.html : first page for restaurants (seen by restaurants only) 


checkoutPage.html : general checkout page
feedbackPage.html : general feedback page
accountPage.html : general account page  

Styling:

static folder contains background.css, reEatslogo.png for design purposes


