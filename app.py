from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "s3cr3ct k3y"

@app.route("/")
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    number_plays = session.get("number_plays", 0)

    return render_template("base.html", board=board,
                           highscore=highscore,
                           number_plays=number_plays)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    number_plays = session.get("number_plays", 0)

    session['number_plays'] = number_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)