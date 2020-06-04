# import Dependencies
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.orm.exc import *
from werkzeug.exceptions import *
import sys
import random
from sqlalchemy import func
# import custom models file
from models import setup_db, Question, Category, db

# Initialize data show 10 per page
QUESTIONS_PER_PAGE = 10

# Paginate the data/page


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    ss = selection.paginate(page, per_page=QUESTIONS_PER_PAGE)
    ss1 = [qq.format() for qq in ss.items]
    return ss1


# categories format in key, value with id and type format.
def format_categories(data):
    categories = {}
    for cat in data:
        categories[cat.id] = cat.type
        # return
    return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # after_request decorator to set Access-Control-Allow
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # GET requests for all available categories.

    @app.route('/categories')
    def categories():
        # get all data from table category order by id.
        ctg_selection = Category.query.order_by(Category.id)
        # If ctg_selection get Null value then raise error "Not Found"
        if ctg_selection.all() is None:
            abort(404)
        # if get-data then jsonify data
        return jsonify({
            'success': True,
            'categories': format_categories(ctg_selection.all()),
            'total_categories': ctg_selection.count()  # no use in frontend
        })

    # GET requests for all paginate Questions and categories.

    @app.route('/questions')
    def questions():
        # query question_data from Question order by id.
        qs_selection = Question.query.order_by(Question.id)
        # query data from Category table order by id.
        ctg_selection = Category.query.order_by(Category.id).all()
        if ctg_selection is None:
            abort(404)
        # Paginate data
        current_questions = paginate_questions(request, qs_selection)
        # Raise error if no any record found.

        # Return data in json format
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': qs_selection.count(),
            'current_category': None,
            'categories': format_categories(ctg_selection)
        })

    # delete questions by given id.

    @app.route('/questions/<int:ques_id>/delete', methods=['DELETE'])
    def delete_questions(ques_id):
        try:
            # see data in Question Table,
            ques = Question.query.filter(Question.id == ques_id).one_or_none()
            # If data is None then raise Error,
            if ques is None:
                abort(404)
            # Delete question-data on given id.
            ques.delete()
            # return and pass data
            return jsonify({
                'success': True,
                'deleted': ques_id
            })
        # Exception Handling
        except Exception:
            abort(422)

    # Add new data in Question Table

    @app.route('/questions/add', methods=['POST'])
    def create_questions():
        # retrive json body data
        body = request.get_json()
        # check required Question data
        if all(key in body for key in
               ('question', 'answer', 'category', 'difficulty')):
            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)
            # Insert into table where value is taking from body
            newQues = Question(question=question, answer=answer,
                               category=category, difficulty=difficulty)
            newQues.insert()
            # select question data and paginate
            selection = Question.query.order_by(Question.id)
            current_ques = paginate_questions(request, selection)
            # return data in json format
            return jsonify({
                'success': True,
                'created': newQues.id,
                'questions': current_ques,  # no use in frontend
                'total_question': selection.count()  # no use in frontend
            })
        # raise error
        else:
            abort(422)

    # search questions endpoint

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            # request json body
            body = request.get_json()
            search = body.get('searchTerm', None)
            # select data from Question matched by {search}
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search)))
            current_questions = paginate_questions(request, selection)
            # if page is empty abort
            if len(current_questions) == 0:
                abort(404)
            # jsonify data
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': selection.count(),
                'current_category': None
            })
        # raise error
        except NotFound:
            abort(404)
        except Exception:
            abort(422)

    # Question endpoint with categories Item

    @app.route('/categories/<int:c_id>/questions')
    def ques_based_category(c_id):
        try:
            # Fetch Question data row filter_by question_id.
            question = Question.query.filter(
                Question.category == c_id).order_by(Question.id)
            # Paginate data
            current_question = paginate_questions(request, question)
            # if current_question is None raise error
            if len(current_question) == 0:
                abort(404)
                # return success in json format
            return jsonify({
                'success': True,
                'current_category': c_id,
                'questions': current_question,
                'total_questions': question.count()
            })
        # raise error
        except Exception:
            abort(422)

    # play quiz game
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # request data from json input
        body = request.json
        # check required key available or not
        if all(key in body for key in ('previous_questions', 'quiz_category')):
            q_category = body['quiz_category']
            previous_ques = body['previous_questions']
            # if json category id == 0
            if q_category['id'] == 0:
                # if previous_ques is empty
                if previous_ques is None:
                    questions = Question.query.all()
                # if previous_ques is not empty
                else:
                    # query data from table Questions where Question.id
                    # not in previous_ques using notin_ method.
                    questions = Question.query.filter(
                        Question.id.notin_(previous_ques)).all()
            # if json category id != 0
            else:
                if previous_ques is None:
                    questions = Question.query.filter(
                        Question.category == q_category['id']).all()
                else:
                    questions = Question.query.filter(Question.id.notin_(
                        previous_ques), Question.category ==
                        q_category['id'])
                    questions_data = questions.all()
                    len_questions = questions.count()
            # randomize questions within range or None
            next_ques = questions_data[random.randrange(
                0, len_questions)].format() if len_questions > 0 else None
            # return in json value
            return jsonify({
                'success': True,
                'question': next_ques
            })
        # raise error
        else:
            abort(422)

    # Not Found error Handler

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # Method not allowed error handler

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    # unprocessable error Handler
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # bad request error handler
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": false,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
