from flask import Flask


# def create_app():
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# return app

from cmcapps import routes
