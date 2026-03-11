import os

import SimpleITK as sitk

def createFileName(title: str, patient: str, case: int, series: int, dir: str, compression = False):

    file_name = f'{title}-{patient}-10{case}_000{series}.nii{".gz" if compression else ""}'
    file = os.path.join(dir, file_name)
    return file

def writeFile(file: str, image: sitk.Image, compress = False):
    writer = sitk.ImageFileWriter()

    print("Writing to:", file)
    writer.SetFileName(file)
    writer.SetUseCompression(compress)
    writer.SetImageIO('NiftiImageIO')

    writer.Execute(image)
