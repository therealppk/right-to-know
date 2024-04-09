# right-to-know
Right to Know is a simple Mobile Web App that prompts users with real time suggestions while they are encountering any situation with law enforcement.

## Inspiration
The nation sees a large number of police misconducts, and some misuse their powers. Also, a major population of citizens are unaware of their rights and the laws that protect them.

"Most misconduct involves routine infractions, but the records reveal tens of thousands of cases of serious misconduct and abuse. They include 22,924 investigations of officers using excessive force, 3,145 allegations of rape, child molestation and other sexual misconduct and 2,307 cases of domestic violence by officers." - US Today.

Some cases of excessive force or misinformed citizens can be avoided by helping citizens know their rights when faced with a tense situation (interaction with law enforcement). We built a mobile web application to help citizens know their rights and mutually de-escalate situations. 

## What it does
The app listens to the conversation between the citizen and the law enforcement officer. Based on the ongoing conversation, the app constantly suggests the person with prompts, telling them the possible ways to handle the situation. The user's location is also used to review laws pertinent to the particular state and county.

## How I built it
We created a simple Python Flask application. The connection between the backend and frontend was handled by using SocketIO. The audio was transcribed and sent to Gemini API with the required supporting prompts, and the suggestions were shown to the user.

## Development Setup
1. Create a Virtual Environment (recommended).
2. Install the required Python packages.
```shell
pip3 install -r requirements.txt
```

## How to Run the Project
### Development
1. Create a copy of `.env.development` as `.env`. Fill in the right values.
2. Change the dummy Google API Key
3. Run the Flask application.
```shell
export $(cat .env | xargs) && FLAVOUR=development flask --app righttoknow run
```
### Production
1. Create a copy of `.env.production` as `.env`. Fill in the right values.
2. Run the Flask application.
```shell
export $(cat .env | xargs) && FLAVOUR=production gunicorn 'righttoknow.__init__:create_app()'
```
