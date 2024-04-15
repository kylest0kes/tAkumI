from flask import Flask, render_template, request
import pygame
import threading

app = Flask(__name__)

#run the game
def run_pygame():
    # game goes here
    print('in run_pygame func')

@app.route('/')
def index():
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)