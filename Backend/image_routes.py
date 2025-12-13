from flask import Blueprint, request, jsonify
from cv_filters.filters import apply_filter
import cv2
import numpy as np
import base64

image_bp = Blueprint("image_bp", __name__)

@image_bp.route("/process", methods=["POST"])
def process_image():
    file = request.files.get("image")
    filter_name = request.form.get("filter")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    if not filter_name:
        return jsonify({"error": "No filter provided"}), 400

    # Lire image
    try:
        npimg = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    except Exception as e:
        print("DECODE ERROR:", e)
        return jsonify({"error": "decode failed"}), 500

    # Appliquer filtre
    filtered = apply_filter(img, filter_name)
    if filtered is None:
        return jsonify({"error": "Filter returned None"}), 500

    # Encode en base64
    try:
        _, buffer = cv2.imencode(".png", filtered)
        img_str = base64.b64encode(buffer).decode("utf-8")
    except Exception as e:
        print("ENCODE ERROR:", e)
        return jsonify({"error": "encode failed"}), 500

    return jsonify({
        "imageUrl": f"data:image/png;base64,{img_str}",
        "pythonCode": f"# Python code for {filter_name}\ndef apply_{filter_name}(img):\n    # ... code ici ...\n    return img"
    })
