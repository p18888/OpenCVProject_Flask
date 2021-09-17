import re
from flask import Flask, request, render_template
import flask
from flask_cors import cross_origin

import virtual_paint

import gym_trainer
app=Flask(__name__)

import finger_counter

@app.route("/")
@cross_origin()
def home():
    return render_template('home.html')


@app.route('/finger_counts')
@cross_origin()
def finger_counts():
    return finger_counter.count_finger()

@app.route('/draw_virtual')
@cross_origin()
def draw_virtual():
    return virtual_paint.paint_virtual()

@app.route('/personal_trainer')
@cross_origin()
def personal_trainer():
    return gym_trainer.pushup_count()





if __name__ == "__main__":
    app.run(debug=True)