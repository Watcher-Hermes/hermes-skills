# Full MMLU evaluation (57 subjects)
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --num_fewshot 5 \  # 5-shot evaluation (standard)
  --batch_size 8 \
  --output_path results/ \
  --log_samples  # Save individual predictions