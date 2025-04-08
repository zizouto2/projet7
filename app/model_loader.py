import torch
from transformers import AutoTokenizer, pipeline
from app.config import settings

model_name = settings.model_name
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

if "mistral" in model_name.lower():
    from auto_gptq import AutoGPTQForCausalLM
    model = AutoGPTQForCausalLM.from_quantized(model_name, device="cuda:0", use_triton=True)
else:
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
