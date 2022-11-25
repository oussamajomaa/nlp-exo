import spacy
import spacy_transformers
nlp = spacy.blank("ar") # empty English pipeline
# create the config with the name of your model
# values omitted will get default values
config = {
    "model": {
        "@architectures": "spacy-transformers.TransformerModel.v3",
        "name": "aubmindlab/bert-large-arabertv02"
    }
}
nlp.add_pipe("transformer", config=config)
nlp.initialize() # XXX don't forget this step!
doc = nlp("فريك الذرة لذيذة")
print(doc._.trf_data) # all the Transformer output is stored here 
print('heool')