export CUDA_VISIBLE_DEVICES=0

model_name=iTransformer

python -u run.py --task_name long_term_forecast --is_training 1 --root_path ./dataset/all_5_coins_2_years/ --data_path all_5_coins_2_years_returns.csv --model_id qtr2_60_10 --model iTransformer --data custom --features MS --seq_len 60 --label_len 0 --pred_len 10 --e_layers 4 --d_layers 4 --enc_in 21 --dec_in 21 --c_out 21 --des 'Exp' --d_model 512 --d_ff 512 --itr 1 --target Return --batch_size 256 --train_epochs 10 --patience 5 --num_workers 0

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_returns.csv \
  --model_id qtr_60_10 \
  --model iTransformer \
  --data custom \
  --features MS \
  --seq_len 60 \
  --label_len 0 \
  --pred_len 10 \
  --e_layers 4 \
  --d_layers 4 \
  --enc_in 21 \
  --dec_in 21 \
  --c_out 21 \
  --des 'Exp' \
  --d_model 512 \
  --d_ff 512 \
  --itr 1 \
  --target Return \
  --batch_size 256 \
  --train_epochs 1 \
  --patience 5 \
  --num_workers 0 \
  --freq 15min

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years_date_aligned.csv \
  --model_id qt_360_60 \
  --model iTransformer \
  --data custom \
  --features M \
  --seq_len 360 \
  --label_len 0 \
  --pred_len 60 \
  --e_layers 4 \
  --d_layers 4 \
  --enc_in 5 \
  --dec_in 5 \
  --c_out 5 \
  --des 'Exp' \
  --d_model 512 \
  --d_ff 512 \
  --itr 1 \
  --target Open \
  --batch_size 512 \
  --train_epochs 1


python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/all_5_coins_2_years/ \
  --data_path all_5_coins_2_years.csv \
  --model_id qt_360_60 \
  --model iTransformer \
  --data custom \
  --features M \
  --seq_len 360 \
  --label_len 60 \
  --pred_len 60 \
  --e_layers 3 \
  --d_layers 1 \
  --factor 3 \
  --enc_in 5 \
  --dec_in 5 \
  --c_out 5 \
  --des 'Exp' \
  --d_model 512\
  --d_ff 512\
  --itr 1 \



