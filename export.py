import glob
import os
from tqdm import tqdm
from helper import *
from data_format import DataFormat, CsvFormat


def export(csv_path, images_dir, output_geojson_name, output_csv_name):

    """
    Terminal Open, input Csv columns name
    Template Csv column first column


    :param csv_path:
    :param images_dir:
    :param output_geojson_name:
    :param output_csv_name:
    :return:
    """

    lats, lons, times = gps_file_reader(csv_path)
    project_files = glob.glob(os.path.join(images_dir, '*.jpg'))
    save_titles(output_csv_name)
    features_geo: list = []

    SequenceUUID = unique_matchId_generator(letter_count=8, digit_count=4)
    for index, img_path in enumerate(tqdm(project_files)):

        image_name = os.path.basename(img_path)

        photo_uuid = photo_uuid_creater(times[index], image_name)

        if index == int(len(project_files)) - 1:
            lats[index - 1], lons[index - 1], \
            lats[index], lons[index] = float(lats[index - 1]), float(lons[index - 1]), \
                                       float(lats[index]), float(lons[index])

            heading_cal = bearing(startLat=lats[index - 1],
                                  startLon=lons[index - 1],
                                  destLat=lats[index],
                                  destLon=lons[index])

        else:
            lats[index], lons[index], \
            lats[index + 1], lons[index + 1] = float(lats[index]), float(lons[index]),\
                                               float(lats[index + 1]), float(lons[index + 1])

            heading_cal = bearing(startLat=lats[index],
                                  startLon=lons[index],
                                  destLat=lats[index + 1],
                                  destLon=lons[index + 1])

        heading_cal = (heading_cal + 360) % 360
        if index % 10 == 0:
            SequenceUUID = unique_matchId_generator(letter_count=8, digit_count=4)
        """Save Format Setting"""
        DataFormat.Latitude = lats[index]
        DataFormat.Longitude = lons[index]
        DataFormat.CaptureTime = times[index]
        DataFormat.Altitude = 0
        DataFormat.Roll = 0
        DataFormat.Pitch = 0
        DataFormat.Roll = 0
        DataFormat.Heading = heading_cal
        DataFormat.SequenceUUID = SequenceUUID
        DataFormat.Orientation = 1
        DataFormat.PhotoUUID = photo_uuid
        DataFormat.image_name = image_name
        DataFormat.image_path = ''
        CsvFormat.OutputFileName = output_csv_name
        save_format(DataFormat, CsvFormat)

        features_geo.append(geojson_add_feature(lat=float(DataFormat.Latitude),
                                                lon=float(DataFormat.Longitude),
                                                time=DataFormat.CaptureTime,
                                                order=index, color='0414fb',
                                                heading=DataFormat.Heading))

    geoFormat = geojson_type(features_geo)
    geoExportPath = output_geojson_name + ".geojson"
    save_(geoFormat, geoExportPath)

