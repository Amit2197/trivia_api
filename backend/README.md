# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
## Backend

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Frontend
From the frontend folder, run the following commands to start the client:

```bash
npm install // only once to install dependencies
npm start 
```
By default, the frontend will run on localhost:3000.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API Reference

## Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

## Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 405 Method Not Allowed
* 422: Not Processable

## API EndPoint Documentation
---
<details>
<summary>GET '/categories'</summary>

- General:
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: curl http://127.0.0.1:5000/categories
    ```json
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true,
        "total_categories": 6
    }
    ```
</details>

<details>
<summary>GET '/questions'</summary>

- General:
    - Returns: list of questions, 
  number of total questions, current category, categories.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: curl http://127.0.0.1:5000/questions or http://127.0.0.1:5000/questions?page=1
    ```json
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }        
    ],
    "success": true,
    "total_questions": 21
    }
    ```
</details>

<details>
<summary>DELETE '/questions/<question_id>/delete'</summary>

- General:
    - Returns: Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
- Sample: curl http://127.0.0.1:5000/questions/29/delete
    ```json
    {
        "deleted": 29,
        "success": true
    }
    ```
</details>

<details>
<summary>POST '/questions/add'</summary>

* General:
    * Creates a new question which will require the question and answer text, category, and difficulty score.
* Sample: curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"Is Bella Ciao Italian or Spanish?", "answer":"Doland trump is ...", "category":"5", "difficulty":"2"}'
    ```json
    {
        "created": 31,
        "questions": [
            {
                "answer": "Bella ciao is an Italian partisan song which originated during the Italian civil war",
                "category": 5,
                "difficulty": 2,
                "id": 31,
                "question": "Is Bella Ciao Italian or Spanish?"
            }
        ],
        "success": true,
        "total_question": 21
    }
    ```
</details>

<details>
<summary>POST '/questions/search'</summary>

* General: Take searchTerm as input and return matching data list.
* Sample: curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"search": "ciao"}'
    ```json
    {
        "current_category": null,
        "questions": [
            {
                "answer": "Bella ciao is an Italian partisan song which originated during the Italian civil war",
                "category": 5,
                "difficulty": 2,
                "id": 31,
                "question": "Is Bella Ciao Italian or Spanish?"
            }
        ],
        "success": true,
        "total_questions": 1
    }
    ```
</details>

<details>
<summary>GET '/categories/<int:category_id>/questions'</summary>

* General: return category based questions
* Sample: curl http://127.0.0.1:5000/categories/5/questions
    ```json
    {
    "current_category": 5,
    "questions": [
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "success": true,
    "total_questions": 1
    }
    ```
</details>

<details>
<summary>POST '/quizzes'</summary>

+ General: return random question on given Categories or From All Categories
+ Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "", "id": 1}}'

    ```json
    // Test 1
    {
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
    }
    // Test 2
    {
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
    }
    ```
</details>