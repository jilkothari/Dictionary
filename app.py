import json
from difflib import get_close_matches

import os

import flask

from flask import Flask, render_template, request


# Load in our file data

app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

def get_definition(word):
    """Gets a definition of the inputted word from the dictionary."""
    file_data = open("data.json")
    data = json.load(file_data)
    file_data.close()
    lowercase = word.lower()
    capitalized = word.title()  # Proper nouns like state names
    upper = word.upper()  # Acronyms like USA
    if lowercase in data:
        return data[lowercase]
    elif capitalized in data:
        return data[capitalized]
    elif upper in data:
        return data[upper]
    elif len(get_close_matches(lowercase, data.keys())) > 0:
        confirm = input("Did you mean %s instead? (Y/N): " % get_close_matches(lowercase, data.keys())[0]).lower()
        if confirm == "y":
            return data[get_close_matches(lowercase, data.keys())[0]]
        elif confirm == "n":
            return "The word was not found in the dictionary. Check if you have misspelled it."
        else:
            return "We didn't understand your input."
    else:
        return "The word was not found in the dictionary. Check if you have misspelled it."


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        prediction=''	
        input = request.form['text']
        definition = get_definition(input)
        if isinstance(definition, list):
            for item in definition:
                prediction = prediction + item
        else:
            prediction = (definition)
    return render_template("result.html", input=input, prediction=prediction)