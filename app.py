rom flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def play():
    return '''
    <h1>Tic Tac Toe</h1>
    <p>
        <a href="/play/">Play</a>
    </p>
    '''