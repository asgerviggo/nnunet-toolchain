import os
import SimpleITK as sitk

from enum import Enum

reader = sitk.ImageFileReader()

Type = Enum('Type', [
    ('t T1 3D TFE gd GTV_GBM', 0),
    ('t T2 3D TSE FLAIR', 1),
    ('t T2 TSE gd', 2),
    ('t T1 3D TFE', 3)
])

def getMetaData(file: str, keys: List[str]):
    keys_map = {
        "series": '0008|103e',
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
    reader.SetFileName(file)
    image = reader.Execute()

    output = ()
    for key in keys:
        output += image.GetMetaData(keys_map[key]),

    return output


def extractSequences(input_dir: str):
    sequences = {}

    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
    
        series, patient, location = getMetaData(file_path, ['series', 'patient', 'location'])
        series = series.strip()
        series_num = Type[series].value

        new_file = [(file_path, float(location))]
        s = sequences.get(series_num, {
            "slices": new_file,
            "patient": patient.rsplit("_", 1)[1].strip()
        })
        s.update({"slices": s["slices"] + new_file})

        sequences.update({series_num: s})

    return sequences
