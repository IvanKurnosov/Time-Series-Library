export CUDA_VISIBLE_DEVICES=2

model_name=DLinear

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_indicators.csv \
  --model_id qt_60_0_10 \
  --model DLinear \
  --data custom \
  --features MS \
  --target Close \
  --seq_len 60 \
  --label_len 0 \
  --pred_len 10 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 24 \
  --dec_in 24 \
  --c_out 24 \
  --des 'Exp' \
  --itr 1 \
  --batch_size 256 \
  --num_workers 0 \
  --train_epochs 1

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years.csv \
  --model_id qt_360_0_60 \
  --model DLinear \
  --data custom \
  --features M \
  --target Open \
  --seq_len 360 \
  --label_len 0 \
  --pred_len 60 \
  --e_layers 2 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 5 \
  --dec_in 5 \
  --c_out 5 \
  --des 'Exp' \
  --itr 1