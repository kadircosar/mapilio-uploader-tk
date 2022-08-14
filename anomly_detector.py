from gps_anomaly import Anomaly
import json


def anomaly_detector(path) -> tuple:

    with open(path, 'r') as f:
        data = json.load(f)
    anomaly = Anomaly()
    result = anomaly.anomaly_detector(data)
    return result
