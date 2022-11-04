# from transformers import pipeline

from bs4 import BeautifulSoup
import requests
import re
import torch



wiki_data = requests.get("https://xmlgrid.net/").text
print(requests.url)
soup = BeautifulSoup(wiki_data, 'lxml')

data = []
for k in soup.select('p'):
  #append and remove citation in text, e.g. [1]
  data.append(re.sub("[\(\[].*?[\)\]]", "", k.getText())) 

data = ''.join([s for s in data if isinstance(s,str)])
spchar_list = ['\n', '/', '\\', '[', ']']
data = data.translate({ord(x): '' for x in spchar_list})
data = data.replace(".", ". ")
print(data)

# data = """
# The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.
#  """

# summarizer = pipeline("summarization", model="facebook/bart-large-cnn") 

# summary = summarizer(data, max_length=150)
# summary = summary[0]['summary_text'].replace(u'\xa0', u' ')
# print(summary)

# smr_t5 = pipeline(task="summarization", model="t5-large", framework="tf")
# smt5 = smr_t5(data, max_length=150)
# print(smt5[0]['summary_text'])