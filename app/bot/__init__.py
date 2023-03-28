from flask import Blueprint

bot_blueprint = Blueprint("bot", __name__, template_folder="templates")

from . import views