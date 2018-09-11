import nltk
sentence = "I want to go from Delhi to Mumbai"
tagged = nltk.post_tag(sentence)
entities = nltk.chunk.ne_chunk(sentence)
entities
