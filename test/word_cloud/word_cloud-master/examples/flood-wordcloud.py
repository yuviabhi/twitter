#!/usr/bin/env python
"""
Flood Word CLoud Generation

Run as : python flood-wordcloud.py 20170803
===============
 
Generating a flood word cloud from the US constitution using default arguments.
"""
import sys
from os import path
from wordcloud import WordCloud,  STOPWORDS
from PIL import Image
import pandas as pd
import numpy as np


filename = str(sys.argv[1])


input_file = "~/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/flood/kolkata/flood-kolkata-1000km-tweets-with-geo-coords-"+filename+".csv"
df = pd.read_csv(input_file, sep="\t", header=0,usecols=["text"])
df.to_csv(r'flood-wordcloud.txt', header=None, index=None, sep='\n', mode='a')

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'flood-wordcloud.txt')).read()


# read the mask image
mask = np.array(Image.open(path.join(d, "bihar-rainfall-aug17.png")))


# tweaking the text a little bit for better result
text = text.replace("Gujarat", "#Bihar")


# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("https")
stopwords.add("co")
stopwords.add("RT")
stopwords.add("ChaudhryShankar")
stopwords.add("Asaram Bapu")
stopwords.add("Bapu Ji")
stopwords.add("Rahul Gandhi")


# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, margin=10, mask=mask,background_color="white", random_state=42).generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
#wordcloud = WordCloud(max_font_size=40).generate(text)
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
plt.show()

wordcloud.to_file("flood_wordcloud_figure_"+filename+".png")

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()
