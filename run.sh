#!/bin/bash

base_dir=/data/duhu/wenet/examples/pl_pl/s1/data/
model_types="tiny small base medium large-v1 large-v2"
short_sets="commonvoice King-ASR-212 M_AILABS"
long_sets="" # mls_polish => data error
language=Polish
exp_dir=exp
is_long=false
stage=1

# mls_polish is long type

if [ $stage -le 0 ]; then
    echo "Stage: $stage: do the recognition"
    for model_type in $model_types; do
        # do the recognition for long wav
        for setname in $long_sets; do
            python recoginise.py \
                        --language $language \
                        --model-type $model_type \
                        --exp-dir $exp_dir \
                        --is-long \
                        --data-dir $base_dir/$setname/test \
                        --setname $setname
        done

        # do the recognition for short wav
        for setname in $short_sets; do
            python recoginise.py \
                        --language $language \
                        --model-type $model_type \
                        --exp-dir $exp_dir \
                        --data-dir $base_dir/$setname/test \
                        --setname $setname
        done
    done

fi

if [ $stage -le 1 ]; then
    echo "Stage: $stage:Compute the wer"
    for model_type in $model_types; do
        # do the recognition for short wav
        for setname in $short_sets; do
            ref_file=$exp_dir/$setname/$model_type/${setname}_${model_type}_ref.text
            hyp_file=$exp_dir/$setname/$model_type/${setname}_${model_type}_hyp.text
            ./sclite_run.sh $ref_file $hyp_file
        done
        for setname in $long_sets; do
            ref_file=$exp_dir/$setname/$model_type/${setname}_${model_type}_ref.text
            hyp_file=$exp_dir/$setname/$model_type/${setname}_${model_type}_hyp.text
            ./sclite_run.sh $ref_file $hyp_file
        done
    done
fi