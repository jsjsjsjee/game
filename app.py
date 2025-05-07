from flask import Flask, render_template, request, session, redirect, url_for
import random
import requests

app = Flask(__name__)
app.secret_key = "secret"

def get_random_word():
    try:
        response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        if response.status_code == 200:
            return response.json()[0]
    except:
        pass
    return random.choice(["python", "flask", "developer", "program", "keyboard", "display", "monitor", "screen", "project", "button"])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tic-tac-toe")
def tic_tac_toe():
    return render_template("tic_tac_toe.html")

@app.route("/hangman", methods=["GET", "POST"])
def hangman():
    if "word" not in session:
        session["word"] = get_random_word()
        session["guessed"] = []
        session["remaining"] = 6

    word = session["word"]
    guessed = session["guessed"]
    display_word = " ".join([c if c in guessed else "_" for c in word])
    result = ""
    game_over = False

    if request.method == "POST":
        letter = request.form["letter"].lower()
        if letter and letter not in guessed and session["remaining"] > 0:
            guessed.append(letter)
            session["guessed"] = guessed
            if letter not in word:
                session["remaining"] -= 1

        display_word = " ".join([c if c in guessed else "_" for c in word])

        if "_" not in display_word.replace(" ", ""):
            result = "You won!"
            game_over = True
        elif session["remaining"] <= 0:
            result = f"You lost! The word was: {word}"
            game_over = True

    return render_template("hangman.html", word=display_word, guessed=guessed,
                           remaining=session["remaining"], result=result,
                           game_over=game_over)

@app.route("/rock-paper-scissors", methods=["GET", "POST"])
def rps():
    result = ""
    if request.method == "POST":
        choices = ["rock", "paper", "scissors"]
        user = request.form["choice"]
        computer = random.choice(choices)
        if user == computer:
            result = "It's a tie!"
        elif (user == "rock" and computer == "scissors") or \
             (user == "scissors" and computer == "paper") or \
             (user == "paper" and computer == "rock"):
            result = "You win!"
        else:
            result = "Computer wins!"
        return render_template("rps.html", result=result, user=user, computer=computer)
    return render_template("rps.html")

@app.route("/memory-card")
def memory_card():
    emojis = [
        "🐶", "🐱", "🦊", "🐼", "🐵", "🐸", "🦄", "🐷",
        "🦁", "🐯", "🐨", "🐰", "🦆", "🐔", "🐧", "🐍",
        "🐞", "🐢", "🦋", "🦕", "🐝", "🦓", "🐬", "🦈",
        "🐡", "🦉", "🐊", "🦜", "🐤", "🦩", "🐫", "🦧"
    ]
    cards = emojis * 2
    random.shuffle(cards)
    return render_template("memory_card.html", cards=cards)

@app.route("/word-scramble", methods=["GET", "POST"])
def word_scramble():
    if "scrambled" not in session:
        word = get_random_word()
        scrambled = list(word)
        random.shuffle(scrambled)
        session["original"] = word
        session["scrambled"] = "".join(scrambled)

    if request.method == "POST":
        guess = request.form["guess"].lower()
        if guess == session["original"]:
            result = "Correct!"
            session.pop("scrambled")
            session.pop("original")
        else:
            result = "Wrong! Try again."
        return render_template("word_scramble.html", scrambled=session.get("scrambled", ""), result=result)

    return render_template("word_scramble.html", scrambled=session["scrambled"])
@app.route("/reset-hangman")
def reset_hangman():
    session.pop("word", None)
    session.pop("guessed", None)
    session.pop("remaining", None)
    return redirect(url_for("hangman"))

if __name__ == "__main__":
    app.run(debug=True)