from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import SummarizationPipeline

model_name = 'lincoln/mbart-mlsum-automatic-summarization'

loaded_tokenizer = AutoTokenizer.from_pretrained(model_name)
loaded_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

nlp = SummarizationPipeline(model=loaded_model, tokenizer=loaded_tokenizer)
result = nlp("""
« La veille de l’ouverture, je vais faire venir un coach pour les salariés qui reprendront le travail. 
Cela va me coûter 300 euros, mais après des mois d’oisiveté obligatoire, la reprise n’est pas simple. 
Certains sont au chômage partiel depuis mars 2020 », raconte Alain Fontaine, propriétaire du restaurant Le Mesturet, 
dans le quartier de la Bourse, à Paris. Cette date d’ouverture, désormais, il la connaît. Emmanuel Macron a, en effet, 
donné le feu vert pour un premier accueil des clients en terrasse, mercredi 19 mai. M. Fontaine imagine même faire venir un orchestre ce jour-là pour fêter l’événement.  
Il lui reste toutefois à construire sa terrasse. Il pensait que les ouvriers passeraient samedi 1er mai pour l’installer, mais, finalement, le rendez-vous a été décalé. 
Pour l’instant, le tas de bois est entreposé dans la salle de restaurant qui n’a plus accueilli de convives depuis le 29 octobre 2020, 
quand le couperet de la fermeture administrative est tombé.M. Fontaine, président de l’Association française des maîtres restaurateurs, 
ne manquera pas de concurrents prêts à profiter de ce premier temps de réouverture des bars et restaurants. Même si le couvre-feu limite le service à 21 heures. 
D’autant que la Mairie de Paris vient d’annoncer le renouvellement des terrasses éphémères installées en 2020 et leur gratuité jusqu’à la fin de l’été.
""")
print(result)