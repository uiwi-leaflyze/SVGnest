import logging
import os

import ezdxf
import svgpathtools
from flask import Flask, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


logging.basicConfig(
    filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)


@app.route("/api2/hello", methods=["GET"])
def hello():
    return {"message": "Hello, world!"}, 200


@app.route("/api2/log", methods=["POST"])
def log():
    forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip = forwarded_for.split(",")[0] if forwarded_for else request.remote_addr

    data = request.get_json()
    message = data.get("message")
    logging.info(f"{client_ip}: {message}")

    return {"message": "Logged"}, 200


@app.route("/api2/convert", methods=["POST"])
def convert():
    if "fileUpload" not in request.files:
        return {"error": "No file part"}, 400

    file = request.files["fileUpload"]

    if file.filename == "":
        return {"error": "No selected file"}, 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    paths, _ = svgpathtools.svg2paths(input_path)

    all_points = []
    for path in paths:
        points = []
        for t in [x / 100 for x in range(100)]:
            point = path.point(t)
            points.append([point.real, -point.imag])
        all_points.append(points)

    doc = ezdxf.new()
    msp = doc.modelspace()
    for points in all_points:
        for i in range(len(points) - 1):
            msp.add_line(points[i], points[i + 1])
        msp.add_line(points[-1], points[0])

    output_path = os.path.join(OUTPUT_FOLDER, file.filename.replace(".svg", ".dxf"))
    doc.saveas(output_path)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8124)
