export CUDA_VISIBLE_DEVICES=0

model_name=PatchTST

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_ma.csv \
  --model_id qt_360_0_60 \
  --model PatchTST \
  --data custom \
  --features M \
  --seq_len 360 \
  --label_len 0 \
  --pred_len 60 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 1 \
  --dec_in 1 \
  --c_out 1 \
  --des 'Exp' \
  --itr 1 \
  --n_heads 4 \
  --train_epochs 1 \
  --batch_size 512 \
  --target MA