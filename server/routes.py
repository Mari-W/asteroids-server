from flask import Blueprint, render_template, request, jsonify

from server.database import database
from server.models import Score

blueprint = Blueprint(__name__, 'home', static_folder='static')


@blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html", scores=dict(enumerate(Score.as_json_list())))


@blueprint.route("/highscores", methods=["GET", "POST"])
@blueprint.route("/highscores/<name>", methods=["GET"])
def api(name=None):
    if request.method == "GET":
        return jsonify(dict(enumerate(Score.as_json_list(count=10, name=name))))
    else:
        json = request.get_json(silent=True)

        if not json:
            return "invalid json", 500

        with database as db:
            db += Score.from_json(json)

        return "", 200


@blueprint.route('/favicon.ico')
def favicon():
    return blueprint.send_static_file('favicon.ico')


@blueprint.route('/css/bootstrap.min.css')
def css():
    return blueprint.send_static_file('bootstrap.min.css')


@blueprint.route('/gif/background.gif')
def background():
    return blueprint.send_static_file('space.gif')
