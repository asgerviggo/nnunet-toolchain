import os

import SimpleITK as sitk

def createFileName(title: str, series: int, dir: str, ext: str):
    file_name = f'{title}_000{series}.{ext}'
    file = os.path.join(dir, file_name)
    return file

def writeFile(file: str, image: sitk.Image, type: sitk.imageio = '', compress = False):
    writer = sitk.ImageFileWriter()
    file = f'{file}{".gz" if compress else ""}'

    print("Writing to:", file)
    writer.SetFileName(file)
    writer.SetUseCompression(compress)
    if type:
        writer.SetImageIO(type)

    writer.Execute(image)
