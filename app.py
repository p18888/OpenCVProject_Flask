from flask import Flask, render_template
import virtual_paint
import gym_trainer
app=Flask(__name__)

import finger_counter

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/finger_counts')
def finger_counts():
    return finger_counter.count_finger()

@app.route('/draw_virtual')
def draw_virtual():
    return virtual_paint.paint_virtual()

@app.route('/personal_trainer')
def personal_trainer():
    return gym_trainer.pushup_count()





if __name__ == "__main__":
    app.run(debug=True)