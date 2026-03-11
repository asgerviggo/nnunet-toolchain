#!/usr/bin/env python

import sys
import os

import SimpleITK as sitk
from sequence_extraction import extractSequences
from file_writer import createFileName, writeFile

if len(sys.argv) < 3:
    print("Usage: DicomSeriesReader <input_directory> <output_directory>")
    sys.exit(1)

[_, input_dir, output_dir] = sys.argv

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

sequences = extractSequences(input_dir)

multi_reader = sitk.ImageSeriesReader()
for series, data in sequences.items():

    slices = data["slices"]
    sorted_slices = sorted(slices, key=lambda file: file[1])
    pathnames = list(map(lambda file: file[0], sorted_slices))

    multi_reader.SetFileNames(pathnames)
    image = multi_reader.Execute()


    patient = data["patient"]
    title = "Test"
    case_num = 0 # get from meta data?

    compress = True
    file = createFileName(title, patient, 0, series, output_dir, compress)
    writeFile(file, image, compress)
