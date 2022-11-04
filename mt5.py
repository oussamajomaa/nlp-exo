import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

article = """
Text summarization (TS) is considered one of the most difficult tasks in natural language processing (NLP) Many papersand research studies address this task in literature but are being carried out in extractive summarization. In this paper, an abstractiveArabic text summarization system is proposed, based on a sequence-to-sequence model..
"""

model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

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