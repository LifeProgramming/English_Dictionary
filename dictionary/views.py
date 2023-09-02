from django.shortcuts import render
import nltk
from nltk.corpus import wordnet
from requests.exceptions import RequestException
from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

def word(request):
    search = request.GET.get('search')
    meanings=[]
    synonyms=[]
    antonyms=[]
    
    try:

        synsets = wordnet.synsets(search)
        for synset in synsets:
            meanings.append(synset.definition())

        for synset in synsets:
            for lemma in synset.lemmas():
                synonyms.append(lemma.name())

        
        for synset in synsets:
            for lemma in synset.lemmas():
                for antonym in lemma.antonyms():
                    antonyms.append(antonym.name())
        
        
        # Check if synonyms and antonyms are not empty
        if not synonyms:
            synonyms = ["No synonyms found"]
        if not antonyms:
            antonyms = ["No antonyms found"]

        context = {
            'meanings': meanings,
            'synonyms': synonyms,
            'antonyms': antonyms,
        }
        
        return render(request, 'word.html', context)
    
    except RequestException as e:
        messages.error(request, "An error occurred while fetching data. Please try again later.")
        return render(request, 'word.html', {})