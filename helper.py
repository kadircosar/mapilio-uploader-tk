import csv
import random
import string
import hashlib
from math import cos, sin, atan2, radians
import math
import json

def save_titles(output_fie_name: str):
    """
    :param output_fie_name: Output csv file name
    :return: Write titles to csv
    """
    data = [['Latitude', 'Longitude', 'CaptureTime', 'Altitude', 'Roll',
             'Pitch', 'Heading', 'SequenceUUID', 'Orientation',
             'DeviceMake', 'DeviceModel', 'ImageSize', 'FoV',
             'PhotoUUID', 'filename', 'path']]

    name = output_fie_name
    with open(name, 'a', newline='') as f:
        write = csv.writer(f)
        write.writerows(data)


def save_format(DataFormat, CsvFormat):

    """
    lat: str, lon: str, capture_time: str, altitude: int, roll: float, pitch: float, heading: float,
    sequenceUUID: str, orientation: int, DeviceMake: str,DeviceMode: str, ImageSize: str, FoV: int,
    PhotoUUID: str, filename: str, path: str, output_fie_name: str
    """

    data = [[DataFormat.Latitude, DataFormat.Longitude,
             DataFormat.CaptureTime, DataFormat.Altitude,
             DataFormat.Roll, DataFormat.Pitch, DataFormat.Heading,
             DataFormat.SequenceUUID, DataFormat.Orientation, DataFormat.DeviceMake,
             DataFormat.DeviceModel,
             DataFormat.ImageSize, DataFormat.FoV,
             DataFormat.PhotoUUID, DataFormat.image_name, DataFormat.image_path]]

    name = CsvFormat.OutputFileName
    with open(name, 'a', newline='') as f:
        write = csv.writer(f)
        write.writerows(data)


def geojson_type(feature: list) -> dict:
    """
    :param feature: Features of geojson file
    :return: Convert geojson file
    """
    return {
        "type": "FeatureCollection",
        "features": feature
    }


def save_(geoFormat: dict, exportPath: str):
    """
    :param geoFormat: feature collection format
    :param exportPath: Directory of output file
    :return: Saved file
    """
    with open(exportPath, "w") as outfile:
        json.dump(geoFormat, outfile, indent=4, ensure_ascii=False)


def geojson_add_feature(lat: float, lon: float, time: str, order: float, color: str, heading: float) -> dict:
    """
    :param lat: Latitude value of  object location
    :param lon: Longitude value of  object location
    :param time: The capture time
    :param order: Order of images
    :param color: Color of object location marker
    :param heading: Heading value
    :return: Write features
    """

    return {
        "type": "Feature",
        "properties": {
            "time": time,
            "order": order,
            "marker-color": color,
            "heading": heading
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                lon,
                lat
            ]
        }
    }


def gps_file_reader(gps_file_path: str) -> list:
    """
    :param gps_file_path: The csv file that obtain gps values
    :return: Latitude, longitude and time values as type list
    """

    with open(gps_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        features, lats, lons, times = [], [], [], []
        for index, row in enumerate(csv_reader):
            if index % 2 == 0:
                lat, lon, time = row
                features.append(geojson_add_feature(float(lat), float(lon), time, (index/2), '#0414fb', heading=0))
                lats.append(lat)
                lons.append(lon)
                times.append(time)
    return [lats, lons, times]


def unique_matchId_generator(letter_count: int = 8, digit_count: int = 4) -> str:
    """
    :param letter_count: Count of random letter
    :param digit_count: Count of random number
    :return: Unique sequence name
    """
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count))) + '-'
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count))) + '-'
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count))) + '-'
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count))) + '-'
    str1 += ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    sam_list = list(str1)
    final_string = ''.join(sam_list)
    return final_string


def photo_uuid_creater(time: str, image_name: str) -> str:
    """
    :param time: Capture time
    :param image_name: Image name
    :return: Unique image name
    """
    code = f'{image_name}--{time}'
    hash_object = hashlib.md5(code.encode())
    photo_uuid = hash_object.hexdigest()
    return photo_uuid


def bearing(startLat: float, startLon: float, destLat: float, destLon: float) -> float:
    """
    :param startLat:  Image latitude value for heading calculation
    :param startLon:  Image longitude value for heading calculation
    :param destLat: Next image latitude value for heading calculation
    :param destLon: Next image longitude value for heading calculation
    :return: Heading value
    """
    to_deg = 180 / math.pi
    phi1 = radians(startLat)
    phi2 = radians(destLat)
    cosPhi2 = cos(phi2)
    dLmd = radians(destLon - startLon)
    aci = atan2(sin(dLmd) * cosPhi2, cos(phi1) * sin(phi2) - sin(phi1) * cosPhi2 * cos(dLmd))
    return aci * to_deg


