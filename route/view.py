from flask import Blueprint,render_template, request

view=Blueprint('view',__name__)

@view.route('/')
def hello_world():
    return 'Hello World!'


