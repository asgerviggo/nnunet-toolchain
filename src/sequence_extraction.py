import os
import SimpleITK as sitk

from enum import Enum

Type = Enum('Type', [
    ('t T1 3D TFE gd GTV_GBM', 0),
    ('t T2 3D TSE FLAIR', 1),
    ('t T2 TSE gd', 2),
    ('t T1 3D TFE', 3)
])

def getMetaData(image: sitk.Image, keys: List[str]):
    keys_map = {
        "series": '0008|103e',
        "series_num": '0008|103f',
        "location": '0020|1041',
        "patient": '0010|0010',
        "study": '0008|1030',
        "orientation": '0020|0037',
        "thickness": '0018|0050',
        "series_number": '0020|0011',
        "instance": '0020|0013',
        "position": '0020|0032',
        "spacing": '0028|0030',
    }

    metadata_keys = image.GetMetaDataKeys()

    output = ()
    for key in keys:
        meta_key = keys_map[key]
        if meta_key in metadata_keys:
            output += image.GetMetaData(meta_key),
        else:
            output += '',

    return output


def extractSequences(input_dir: str):
    sequences = {} # structure: {series_num: (filepath, location)[]}

    # series = sitk.ImageSeriesReader.GetGDCMSeriesIDs(input_dir)
    # print(series)


    for file_name in os.listdir(input_dir):
        # TODO catch error if not folder
        # TODO glob all and write to subfolders
        
        file_path = os.path.join(input_dir, file_name)
        image = sitk.ReadImage(file_path)
    
        series, location = getMetaData(image, ['series', 'location'])


        # TODO get sequence from hd-seq
        # Combine metadata and hd-seq for series data
        series = series.strip()
        series_num = Type[series].value

        new_file = [(file_path, float(location))]
        current = sequences.get(series_num, [])
        sequences.update({series_num: current + new_file})

    return sequences
