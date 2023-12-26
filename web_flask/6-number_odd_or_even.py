#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """ Hello Hbnb"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """ Hello hbnb """
    return 'HBNB'


@app.route('/c/<text>')
def c_compliment(text):
    """ Displaying a message starting with C """
    msg = text.replace('_', ' ')
    return 'C %s' % msg


@app.route('/python/')
@app.route('/python/<text>')
def python_compliment(text='is_cool'):
    """ Displaying a message starting with Python """
    msg = text.replace('_', ' ')
    return 'Python %s' % msg


@app.route('/number/<int:n>')
def display_integer(n):
    """ Displaying n is a number only if n is an integer """
    return "%d is a number" % n


@app.route('/number_template/<int:n>')
def number_page(n):
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>')
def number_info(n):
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
