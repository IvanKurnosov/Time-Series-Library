python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_indicators.csv  \
  --model_id qt_60_0_10 \
  --model TimeMixer \
  --data custom \
  --features MS \
  --target Open \
  --seq_len 60 \
  --label_len 0 \
  --pred_len 10 \
  --e_layers 4 \
  --d_layers 4 \
  --enc_in 24 \
  --dec_in 24 \
  --c_out 24 \
  --des 'Exp' \
  --itr 1 \
  --d_model 16 \
  --d_ff 32 \
  --batch_size 256 \
  --learning_rate 0.0001 \
  --patience 3 \
  --down_sampling_layers 3 \
  --down_sampling_method avg \
  --down_sampling_window 2 \
  --train_epochs 1 \
  --target Close \
  --num_workers 0


python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_date_aligned.csv  \
  --model_id qt_360_0_60 \
  --model TimeMixer \
  --data custom \
  --features M \
  --target Open \
  --seq_len 360 \
  --label_len 0 \
  --pred_len 60 \
  --e_layers 4 \
  --d_layers 4 \
  --enc_in 5 \
  --dec_in 5 \
  --c_out 5 \
  --des 'Exp' \
  --itr 1 \
  --d_model 16 \
  --d_ff 32 \
  --batch_size 256 \
  --learning_rate 0.0001 \
  --patience 3 \
  --down_sampling_layers 3 \
  --down_sampling_method avg \
  --down_sampling_window 2 \
  --train_epochs 1




python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_date_aligned.csv  \
  --model_id qt_360_0_60 \
  --model TimeMixer \
  --data custom \
  --features M \
  --target Open \
  --seq_len 360 \
  --label_len 0 \
  --pred_len 60 \
  --e_layers 3 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 5 \
  --dec_in 5 \
  --c_out 5 \
  --des 'Exp' \
  --itr 1 \
  --d_model 16 \
  --d_ff 32 \
  --batch_size 64 \
  --learning_rate 0.01 \
  --train_epochs 10 \
  --patience 3 \
  --down_sampling_layers 3 \
  --down_sampling_method avg \
  --down_sampling_window 2 \
  --train_epochs 1