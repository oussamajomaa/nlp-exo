import re
from transformers import pipeline

# summarizer1 = pipeline("summarization", model = "facebook/bart-large-cnn")
summarizer2 = pipeline("summarization", model = "google/pegasus-xsum")
# summarizer3 = pipeline("summarization", model = "csebuetnlp/mT5_multilingual_XLSum")


text = """
The tower is 324 meters (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, 
measuring 125 meters (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 meters. 
Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 meters (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France
after the Millau Viaduct.
"""

# summary1 = summarizer1(text)[0]['summary_text'].replace(u'\xa0', u' ')
# summary1 = re.sub("\s\s+"," ",summary1)

summary2 = summarizer2(text)[0]['summary_text'].replace(u'\xa0', u' ')
summary2 = re.sub("\s\s+"," ",summary2)

# summary3 = summarizer3(text)[0]['summary_text'].replace(u'\xa0', u' ')
# summary3 = re.sub("\s\s+"," ",summary3)


# print(summary1)
print('*****************************************************************')
print(summary2)
print('*****************************************************************')
# print(summary3)
print('*****************************************************************')
