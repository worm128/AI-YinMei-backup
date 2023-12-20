set PRE_SEQ_LEN=128
set CHECKPOINT=adgen-chatglm2-6b-pt-128-1e-4
set STEP=300
set NUM_GPUS=1

python main.py ^
    --do_predict ^
    --validation_file AdvertiseGen/dev.json ^
    --test_file AdvertiseGen/dev.json ^
    --overwrite_cache ^
    --prompt_column content ^
    --response_column summary ^
    --model_name_or_path ../THUDM/chatglm2-6b ^
    --ptuning_checkpoint ./lora2/%CHECKPOINT%/checkpoint-%STEP% ^
    --output_dir ./lora2/%CHECKPOINT% ^
    --overwrite_output_dir ^
    --max_source_length 128 ^
    --max_target_length 128 ^
    --per_device_eval_batch_size 1 ^
    --predict_with_generate ^
    --pre_seq_len %PRE_SEQ_LEN% ^
    --quantization_bit 8