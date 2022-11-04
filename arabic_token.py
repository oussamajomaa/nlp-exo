from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("hatmimoha/arabic-ner")

model = AutoModelForTokenClassification.from_pretrained("hatmimoha/arabic-ner")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

article = """
مرحبا أنا أسامة. ولدت في القاهرة وأعيش حاليا في بو جنوب فرنسا, أهلي وأصدقائي ما زالو في سوريا وتعاملون بالليرة والدولار. ذهبت إلى حمص واللاذقية. طرطوس جميلة وجبلة. حوش عرب تقع في القلمون
"""

named_entities = nlp(article)
locations = []

print(named_entities)
[{'entity': 'B-LOCATION', 'score': 0.99823284, 'index': 6, 'word': 'بو', 'start': 26, 'end': 28}, {'entity': 'B-LOCATION', 'score': 0.99821246, 'index': 8, 'word': 'فرنسا', 'start': 32, 'end': 37}]