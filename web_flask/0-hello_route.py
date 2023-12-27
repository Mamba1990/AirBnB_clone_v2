#!/usr/bin/python3
"""Starting a Flask web application"""


# Importing Flask class from flask module
from flask import Flask

# Creation an instance called app of the class by passong the __name__ variable
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Displaying "Hello HBNB!"

    Returns:
        str: The index page's text
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
