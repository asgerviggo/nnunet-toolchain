#!/usr/bin/env python

import sys
import os
import glob

import SimpleITK as sitk
from file_writer import writeFile

def coregister_images(fixed_image_path, moving_image_path):
    # Read in the fixed and moving images
    fixed_image = sitk.ReadImage(fixed_image_path, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(moving_image_path, sitk.sitkFloat32)
  
    # Set up the registration method
    registration_method = sitk.ImageRegistrationMethod()

    # 1. Similarity metric: Use Mattes Mutual Information
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    # 2. Interpolator: Use linear interpolation for image intensity values
    registration_method.SetInterpolator(sitk.sitkLinear)

    # 3. Optimizer: Regular Step Gradient Descent optimizer
    registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=2.0, 
                                                             minStep=1e-4, 
                                                             numberOfIterations=1000,
                                                             gradientMagnitudeTolerance=1e-8)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Set up multi-resolution framework: using a three-level pyramid
    # At each level, the images are downsampled and smoothed:
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    # 4. Set the initial transform using a center-of-mass approach to roughly align the images
    initial_transform = sitk.CenteredTransformInitializer(
        fixed_image, 
        moving_image, 
        sitk.Euler3DTransform(), 
        sitk.CenteredTransformInitializerFilter.GEOMETRY
    )
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    # Optionally, if you want to further constrain the registration to be rigid, ensure you are using Euler3DTransform
    # (which only allows rotation and translation)
    rigid_transform = sitk.Euler3DTransform(initial_transform)
    registration_method.SetInitialTransform(rigid_transform, inPlace=False)

    # 5. Execute the registration
    final_transform = registration_method.Execute(fixed_image, moving_image)

    # Output final registration details
    print("Final metric value: {0}".format(registration_method.GetMetricValue()))
    print("Optimizer's stopping condition: {0}".format(registration_method.GetOptimizerStopConditionDescription()))

    # 6. Resample the moving (MR) image onto the fixed image grid using the final transform
    resampled_image = sitk.Resample(moving_image, 
                                fixed_image, 
                                final_transform, 
                                sitk.sitkLinear, 
                                0.0, 
                                moving_image.GetPixelID())

    return resampled_image, final_transform


if len(sys.argv) < 3:
    print("Usage: <input_directory> <output_directory>")
    sys.exit(1)

[_, input_dir, output_dir] = sys.argv

if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
   
# TODO also glob .nii.gz ?
# Expect files in format: {title}-{patient}-{run}_000{0-3}.nii.gz
# 0: T1 C
# 1: T2 FLAIR
# 2: T2
# 3: T1

t1c_paths = glob.glob(os.path.join(input_dir, "*_0000.nii"))
for t1c_path in t1c_paths:
    [base, sequence_ext] = t1c_path.rsplit("_", 1)

    remaining_paths_glob = f'{base}_*.nii' 

    sequences_paths = glob.glob(remaining_paths_glob)
    sequences_paths.remove(t1c_path)

    for sequence_path in sequences_paths:
        resampled_image, final_transform = coregister_images(t1c_path, sequence_path)

        stripped_path = os.path.basename(sequence_path)
        new_path = os.path.join(output_dir, stripped_path)
        writeFile(new_path, resampled_image)
