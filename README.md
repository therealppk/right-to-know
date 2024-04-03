# right-to-know
Right to Know is a simple Mobile Web App that prompts users with real time suggestions while they are encountering any situation with law enforcement.

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
