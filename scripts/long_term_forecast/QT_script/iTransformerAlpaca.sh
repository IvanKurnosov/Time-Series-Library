

python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path ./dataset/sp500/ \
  --data_path sp500_symbols_5month_2class.csv \
  --model_id sp500_5month_60_1_2class \
  --model iTransformer \
  --data custom \
  --features MS \
  --seq_len 60 \
  --label_len 0 \
  --pred_len 1 \
  --e_layers 4 \
  --d_layers 4 \
  --enc_in 21 \
  --dec_in 21 \
  --c_out 21 \
  --des 'Exp' \
  --d_model 512 \
  --d_ff 512 \
  --itr 1 \
  --target should_buy \
  --batch_size 256 \
  --train_epochs 1 \
  --patience 5 \
  --num_workers 0 \
  --freq 1min
