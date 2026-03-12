#!/usr/bin/env python

import sys
import os

import SimpleITK as sitk
from sequence_extraction import extractSequences, getMetaData
from file_writer import createFileName, writeFile

if len(sys.argv) < 3:
    print("Usage: DicomSeriesReader <input_directory> <output_directory>")
    sys.exit(1)

[_, input_dir, output_dir] = sys.argv

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

sequences = extractSequences(input_dir)

multi_reader = sitk.ImageSeriesReader()
for series, slices in sequences.items():

    sorted_slices = sorted(slices, key=lambda file: file[1])
    pathnames = list(map(lambda file: file[0], sorted_slices))

    multi_reader.SetFileNames(pathnames)
    image = multi_reader.Execute()

    #flip image
    # flip_filter = sitk.FlipImageFilter()
    # flip_filter.SetFlipAxes([False, True, False])
    # flip_filter.SetFlipAboutOrigin(True)
    # flipped = flip_filter.Execute(image)

    # Get all these from metadata?
    # patient, = getMetaData(image, ['patient'])
    # patient = patient.rsplit("_", 1)[1].strip()
    patient = "0001"
    title = "Test"
    case_num = 0

    compress = False
    file = createFileName(title, patient, case_num, series, output_dir)
    writeFile(file, image, compress)


