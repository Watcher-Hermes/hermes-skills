# eval_all_models.sh

TASKS="mmlu,gsm8k,hellaswag,truthfulqa"

while read model; do
    echo "Evaluating $model"