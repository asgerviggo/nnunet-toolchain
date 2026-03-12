./extract_to_nifti.py $INPUT ./raw_niftis

./coregistration.py ./raw_niftis ./niftis_registered

python -m hd-bet -i ./niftis_registered -o $OUTPUT
