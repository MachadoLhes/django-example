<div align="center">
    <img src="https://raw.githubusercontent.com/Jobsity/ReactChallenge/main/src/assets/jobsity_logo_small.png"/>
</div>

# Python/Django Challenge

## Description
This project was created as a test for a software developer position at Jobsity.

## How to run the project
### Running the container:
* Simply run `docker compose up` from the project's root directory.
### Running manually:
* Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Start the api service: `cd api_service; python manage.py runserver`
* Start the stock service: `cd stock_service ; python manage.py runserver 8001`

## Services
### API service
__Important:__ This service requires authentication for it's usage. Authentication is made via token authentication, which you can retrieve from the `/api/token` endpoint detailed below.
* This service will integrate with the Stock Service to retrieve stock information from an external api, in this case, `stooq.com`.
* The following endpoints are available:

  `GET /stock?q={stock_code}`

  > Will retrieve, if found, `name`, `symbol`, `open`, `high`, `low` and `close` for the provided `stock_code`.

  `GET /history`

  > Will retrieve the history of queries made to the api service by the authenticated user.

  `GET /stats`

  > Accecible only by __super users__. Will return the top 5 most requested stocks.

  `POST /api/token`

  Expects the following `JSON` body:

  ```json
    {
      "username":{username},
      "email":{email},
      "password":{password},
      "is_admin":false,
    }
  ```

  > Accecible only by __super users__. Will create a new user, which can be a __super user__ by using the optional parameter `is_admin: true` in body.

  `POST /api/token`

  Expects the following `JSON` body:

  ```json
    {
      "username":{username},
      "password":{password},
    }
  ```

  > Will return both an `access` and `refresh` token, which will be valid for __30 minutes__ and __10 days__, respectively.

  `POST /api/token/refresh`

  Expects the following `JSON` body:

  ```json
    {
      "refresh":{refresh_token},
    }
  ```

  > Will return an `access` token, which will be valid for __30 minutes__.

### Stock service
* This is an internal service, essential for the `API service` to work.
* This should only be used by the `API service`, but `stocks` can be queried via the following endpoint:

  `GET /stock?stock_code={stock_code}`

  > Will retrieve, if found, `name`, `symbol`, `open`, `high`, `low`, `close` and `date` for the provided `stock_code`.