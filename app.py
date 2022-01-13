from flask import Flask, render_template
import virtual_paint
import gym_trainer
import zoom_filter
import backgroud_effect
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

@app.route("/zoom_filter")
def zoom_fltr():
    return zoom_filter.image_zoom()



@app.route("/change_background")
def change_background():
    return backgroud_effect.change_background()



if __name__ == "__main__":
    app.run(debug=True)