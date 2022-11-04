from transformers import AutoTokenizer, AutoModelWithLMHead

model_name = "t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)

article = """
Text summarization (TS) is considered one of the most difficult tasks in natural language processing (NLP) Many papersand research studies address this task in literature but are being carried out in extractive summarization. In this paper, an abstractiveArabic text summarization system is proposed, based on a sequence-to-sequence model..
"""

input_tokens = tokenizer(
    [article],
    return_tensors='pt',
    max_length=1024,
    truncation=True)['input_ids']

encoded_ids = model.generate(
    input_tokens,
    num_beams=4,
    length_penalty=2.0,
    max_length=150,
    min_length=50,
    no_repeat_ngram_size=3
)
summary = tokenizer.decode(encoded_ids.squeeze(), skip_special_tokens=True)
print(summary)