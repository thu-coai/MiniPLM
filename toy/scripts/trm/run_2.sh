BASE_PATH=${1}

# bash /home/aiscuser/sps/toy/scripts/trm/ts/opt_5k_noise.sh /home/aiscuser/sps 2030 8 --epochs 4000 --outer-lr 0.1

bash /home/aiscuser/sps/toy/scripts/trm/ts/eval_5k_noise.sh /home/aiscuser/sps/ 2030 8 \
    --load-alpha ${BASE_PATH}/results/toy/trm/toy-trm-5k-ln-ts-64/bs512-lr0.1-tn16384-dn512-e4000/-0.8_30-opt-0.2-0/10-20-7 \
    --alpha-epochs "0.2,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19" \
    --epochs 4000

bash ../scripts/pad.sh /home/aiscuser/sps/ 2030 8 2