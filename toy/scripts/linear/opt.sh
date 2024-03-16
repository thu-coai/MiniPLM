#! /bin/bash

BASE_PATH=${1-"/home/MiniLLM"}
MASTER_ADDR=localhost
MASTER_PORT=${2-2030}
NNODES=1
NODE_RANK=0
GPUS_PER_NODE=${3-2}

DISTRIBUTED_ARGS="--nproc_per_node $GPUS_PER_NODE \
                  --nnodes $NNODES \
                  --node_rank $NODE_RANK \
                  --master_addr $MASTER_ADDR \
                  --master_port $MASTER_PORT"

# type
TYPE="toy"
# hp
LR=0.1
BATCH_SIZE=512
# runtime
SAVE_PATH="${BASE_PATH}/results/${TYPE}"
# seed
SEED=10
SEED_DATA=20


OPTS=""
# type
OPTS+=" --type ${TYPE}"
# model
OPTS+=" --model-type linear"
OPTS+=" --base-path ${BASE_PATH}"
OPTS+=" --input-dim 128"
OPTS+=" --ckpt-name linear-128"
# data
OPTS+=" --train-num 4096"
OPTS+=" --dev-num 512"
OPTS+=" --test-num 512"
OPTS+=" --data-names toy-linear"
OPTS+=" --data-dir ${BASE_PATH}/processed_data/toy-linear/128/0.5-3.0-1.0-4096-10-20-1"
OPTS+=" --load-toy-data 1"
OPTS+=" --add-noise 0.5-3.0-1.0"
# hp
OPTS+=" --lr ${LR}"
OPTS+=" --batch-size ${BATCH_SIZE}"
OPTS+=" --eval-batch-size 64"
OPTS+=" --grad-batch-size 512"
OPTS+=" --epochs 2000"
OPTS+=" --log-interval 10"
OPTS+=" --outer-lr 0.001"
OPTS+=" --outer-epochs 1000"
OPTS+=" --clip-grad -1"
OPTS+=" --max-length -1"
# runtime
OPTS+=" --save ${SAVE_PATH}"
OPTS+=" --opt-alpha"
OPTS+=" --toy-zero2"
# seed
OPTS+=" --seed ${SEED}"
OPTS+=" --seed-data ${SEED_DATA}"
# deepspeed
OPTS+=" --deepspeed"
OPTS+=" --deepspeed_config ${BASE_PATH}/configs/deepspeed/ds_config.json"


export NCCL_DEBUG=""
# export WANDB_DISABLED=True
export TF_CPP_MIN_LOG_LEVEL=3
export PYTHONPATH=${BASE_PATH}
export OMP_NUM_THREADS=16
# CMD="deepspeed ${DISTRIBUTED_ARGS} ${BASE_PATH}/toy/trm/main.py ${OPTS} $@"
CMD="torchrun ${DISTRIBUTED_ARGS} ${BASE_PATH}/toy/trm/main.py ${OPTS} $@"

echo ${CMD}
echo "PYTHONPATH=${PYTHONPATH}"
mkdir -p ${SAVE_PATH}
${CMD}