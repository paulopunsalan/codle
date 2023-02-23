from flask import Flask, render_template, request
import random

app = Flask(__name__)

words = open('static/wordlist.txt').read().split('\n')

# values get modified based on their level
# 0: empty
# 1: incorrect
# 2: misplaced
# 3: correct
gridValues = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# words
wordsPlayed = []
wordToGuess = random.choice(words).lower()
ended = False

@app.route('/')
def main():
    if ended:
        return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed, word = wordToGuess.upper())
    else:
        return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed)

@app.route('/guess', methods=['POST'])
def guess():
    global ended

    if ended:
        return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed, word = wordToGuess.upper())

    word = request.form['guess'].lower()

    if len(word) < 5 or word not in words:
        return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed)

    wordsPlayed.append(word)

    # duplicate letter checking
    # store all unique letter amts in a dictionary
    letter_amts = {}

    for l in wordToGuess:
        if letter_amts.get(l) == None:
            letter_amts[l] = wordToGuess.count(l)
    
    for i in range(0, len(word)):
        l = word[i]
        row = len(wordsPlayed) - 1

        if l in wordToGuess and letter_amts[l] > 0:
            if l == wordToGuess[i]:
                gridValues[row][i] = 3 # in same index
            elif letter_amts[l] > 0:
                gridValues[row][i] = 2 # not in same index (both word to guess and word guessed)
            else:
                gridValues[row][i] = 1 # wrong
            # decrease amount
            letter_amts[l] -= 1
        else:
            gridValues[row][i] = 1 # wrong
    
    if word == wordToGuess or len(wordsPlayed) == 6:
        ended = True
        return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed, word = wordToGuess.upper())

    return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed)

@app.route('/restart', methods=["POST"])
def restart():
    global ended
    global gridValues
    global wordsPlayed
    global wordToGuess

    gridValues = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    wordsPlayed = []
    wordToGuess = random.choice(words).lower()
    ended = False

    return render_template('index.html', grid = gridValues, wordsPlayed = wordsPlayed)

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/wordlist')
def wordlist():
    return render_template('wordlist.html', wordlist=open('static/wordlist.txt').read().replace('\n', ', '))