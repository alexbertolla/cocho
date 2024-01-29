from flask import Flask, render_template, Response
from camera.camera import camera, record
import cv2 as cv
from threading import Thread


app = Flask(__name__)


def capture_frames():
    cam1 = camera(camera_name="barriga", fps=30)
    th1 = Thread(target=record, args=(cam1,))
    th1.start()
    th1.join(timeout=3)

    contador_erro = 1

    while th1.is_alive():
        frame_captured = cam1.frame_show
        print(cam1.frame_show)
        ret, buffer = cv.imencode(".jpg", frame_captured)
        frame_captured = buffer.tobytes()
        yield b"--frame_captured\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_captured + b'\r\n'

@app.route("/video")
def video():
    return Response(capture_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")



@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    try:
        print("Iniciando...")
        app.run(debug=True)
    except ValueError as e:
        print("ERROR")
        print(e)

    print("FIM")