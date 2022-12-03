from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# this file creats the app and runs it
from website import create_app

# Create the app
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)