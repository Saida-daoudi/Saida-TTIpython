from flask import Blueprint, request, jsonify
from cv_filters.filters import apply_filter
import cv2
import numpy as np
import base64

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/process", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filter_name = request.form.get("filter", "origin")

    # decode image
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    # apply filter
    filtered_img, python_code = apply_filter(img, filter_name)

    # encode to base64
    _, buffer = cv2.imencode(".png", filtered_img)
    img_str = base64.b64encode(buffer).decode("utf-8")

    return jsonify({
        "imageUrl": f"data:image/png;base64,{img_str}",
        "pythonCode": python_code
    })
