import os

os.environ['TRANSFORMERS_CACHE'] = '../hf_cache'



from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "google/gemma-3-4b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(model_name)
