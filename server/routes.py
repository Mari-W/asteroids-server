from authlib.integrations.flask_client import OAuth
from flask import Blueprint, render_template, request, jsonify, session, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from server.database import database
from server.models import Score

blueprint = Blueprint(__name__, 'home', static_folder='static')
limiter = Limiter(key_func=get_remote_address)
oauth = OAuth()


@blueprint.route("/", methods=["GET"])
def home():
    # render sweet little scoreboard
    return render_template("home.html", scores=dict(enumerate(Score.as_json_list(id=True))),
                           user=session.get('user'))


@blueprint.route('/login')
def login():
    # admin login
    if "redirect" in request.args.keys():
        session['login_redirect'] = request.args['redirect']
    # another hardcoded URL are u crazy??
    # nah just lazy
    redirect_uri = "https://stream.inpro.informatik.uni-freiburg.de/callback"
    return oauth.auth.authorize_redirect(redirect_uri)


@blueprint.route('/callback')
def auth():
    # oauth callback from https://auth.inpro.informatik.uni-freiburg.de/
    token = oauth.auth.authorize_access_token()
    user = oauth.auth.parse_id_token(token)

    if not user:
        return "Failed to authenticate user", 500

    session['user'] = user
    return redirect('/')


@blueprint.route("/highscores", methods=["GET", "POST"])
@blueprint.route("/highscores/<name>", methods=["GET"])
@limiter.limit("1000/hour")
def api(name=None):
    # return scores sorted and only best 10 (optionally filtered by name)
    if request.method == "GET":
        return jsonify(dict(enumerate(Score.as_json_list(count=10, name=name))))

    # read request json
    json = request.get_json(silent=True)

    if not json:
        return "invalid json", 500

    # construct score object
    score = Score.from_json(json)

    if not score:
        return "invalid object", 500

    # add to database
    with database as db:
        db += score

    return "", 200


@blueprint.route("/delete/<id>", methods=["POST"])
def delete(id=0):
    # admin endpoint to delete scores
    # if someone uses bad names
    user = session.get('user')
    if user["account_type"] != "admin":
        return "nope.", 404

    with database:
        Score.query.delete_by(id=id)

    return redirect("/")


# stuff
@blueprint.route('/favicon.ico')
def favicon():
    return blueprint.send_static_file('favicon.ico')


@blueprint.route('/css/bootstrap.min.css')
def css():
    return blueprint.send_static_file('bootstrap.min.css')


@blueprint.route('/gif/background.gif')
def background():
    return blueprint.send_static_file('space.gif')
