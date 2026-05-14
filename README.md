# Daily Doodle

CITS3403 Agile Web Development Project

## Overview

Daily Doodles is a web application where users receive a daily drawing prompt, create artwork using an in-browser drawing canvas, and submit their drawings for others to view and vote on.

Users can:
- Create an account and log in
- Receive a new daily drawing prompt
- Draw and submit artwork
- Browse drawings from other users
- Vote on their favourite submissions
- View the leaderboard to see the top-rated drawings of the day

---

## Features

### Drawing Canvas

![Canvas](./Images/Canvas.png)

### Filtered Browse Page

![Browse](./Images/Browse.png)

### Voting System

![Votes](./Images/Votes.png)

### All-Time / Prompt Leaderboard

![Leaderboard](./Images/Leaderboard.png)

---

## Technologies Used

### Backend
- Python
- Flask
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Flask-WTF
- SQLAlchemy

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

### Testing
- unittest
- Selenium
- webdriver-manager

### Other
- python-dotenv

---
## Prerequisites

- Python 3.10+
- pip

## Installation

Clone the repository:

```bash
git clone https://github.com/hdavies159753/cits3403_app.git
cd cits3403_app
```
# Running the Application

These startup scripts automatically:
- create the virtual environment
- install requirements
- initialize the database

## Windows

Run:
start.bat

## Mac/Linux

Run:
start.sh

# Running Tests

After installation, run the application, open a terminal in the project folder and run:

## Unit Tests

python -m unittest discover tests

## Selenium Tests

python -m unittest discover tests/selenium

# Structure

app/                Main Flask application
tests/              Unit and Selenium tests
migrations/         Database migrations

# Authors

## CITS3403 Project Team

| Name | Student Number | Username(Name) |
| -------- | -------- | -------- |
| Aidan Harding | 24315152 | BlueBackSpider(Aidan Harding) |
| Alan Ling | 23843412 | AlanLingYS(Alan Ling) |
| Henry Davies | 24483717 | hdavies159753(Henry Davies) |
| Oscar Chan | 24320636 | Oscar-0103(Oscar Chan) |
