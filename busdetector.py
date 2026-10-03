import datetime
import os
import cv2

from ultralytics import YOLO

import config

model = YOLO(f"{config.MODEL}.pt")
model.set_classes(["bus"])


def count_buses_on_image(image_path: str) -> dict:
    image = cv2.imread(image_path)
    results = model(image)

    marked_image = results[0].plot()

    image_filename = os.path.basename(image_path)
    marked_image_path = os.path.join(config.UPLOAD_FOLDER, f"marked_{image_filename}")
    buses_count = len(results[0].boxes)
    if buses_count > 0:
        cv2.imwrite(marked_image_path, marked_image)
    else: marked_image_path = image_path

    speed = results[0].speed

    return {
        "processed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "speed": speed,
        "total_time": sum(speed.values()),
        "marked_image_path": marked_image_path,
        "buses_count": buses_count,
    }