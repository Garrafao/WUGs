#!/bin/bash

dir=../../..
out_dir=${dir}/combined_data
new_data=${dir}/dwug_de_en_sv_reannotation_studies-from-annotation-workspace
old_data=${dir}/dwug

rm -rf ${out_dir}


# D1

python3 combine_datasets.py ${out_dir}/D2_de ${old_data}/dwug_de ${new_data}/dwug_de_uses --require-full-word-overlap
python3 combine_datasets.py ${out_dir}/D2_en ${old_data}/dwug_en ${new_data}/dwug_en_uses --require-full-word-overlap
python3 combine_datasets.py ${out_dir}/D2_sv ${old_data}/dwug_sv ${new_data}/dwug_sv_uses ${new_data}/dwug_sv_uses2 --require-full-word-overlap


# D2

python3 combine_datasets.py $out_dir/D2_de ${old_data}/dwug_de ${new_data}/dwug_de_unc --no-require-full-word-overlap
python3 combine_datasets.py $out_dir/D2_sv ${old_data}/dwug_sv ${new_data}/dwug_sv_unc --no-require-full-word-overlap


# D3

python3 combine_datasets.py $out_dir/datasets_combined/D3_de ${old_data}/dwug_de ${new_data}/dwug_de_uses ${new_data}/dwug_de_unc --no-require-full-word-overlap
python3 combine_datasets.py $out_dir/datasets_combined/D3_sv ${old_data}/dwug_sv ${new_data}/dwug_sv_uses ${new_data}/dwug_sv_uses2 ${new_data}/dwug_sv_unc --no-require-full-word-overlap


# D4

python3 combine_datasets.py $out_dir/datasets_combined/D4_de ${new_data}/dwug_de_resampled
python3 combine_datasets.py $out_dir/datasets_combined/D4_sv ${new_data}/dwug_sv_resampled ${new_data}/dwug_sv_resampled2 
python3 combine_datasets.py $out_dir/datasets_combined/D4_de ${new_data}/dwug_en_resampled


# D5

python3 combine_datasets.py $out_dir/datasets_combined/D5_de ${new_data}/dwug_de_uses
python3 combine_datasets.py $out_dir/datasets_combined/D5_sv ${new_data}/dwug_sv_uses ${new_data}/dwug_sv_uses2 
python3 combine_datasets.py $out_dir/datasets_combined/D5_de ${new_data}/dwug_en_uses




