from django.shortcuts import render, redirect
import nltk
from nltk.corpus import wordnet
from requests.exceptions import RequestException
from django.shortcuts import render
from django.contrib import messages
from .models import PersonalDictionary
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return HttpResponse('Sorry! You have already logged in!')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.add_message(request, messages.INFO, "This user does not exist!")
    
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('loginCompleted')
    


    context={'page': page}
    return render(request, 'auth.html', context)


def loginCompleted(request):
    return render(request, 'login_comp.html')


def registerUser(request):
    form=UserCreationForm()
    if request.method=='POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('registerCompleted')
        else:
             messages.add_message(request, messages.INFO, "Sorry! Something went wrong!!!")
           
    return render(request, 'auth.html', context={'form':form})

def registerCompleted(request):
    return render(request, 'register_comp.html')

def logoutUser(request):
    logout(request)
    return redirect('index')
@login_required(login_url='login')
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
        
        if request.method=="POST":
            new_word=PersonalDictionary(word=search)
            new_word.save()
            return redirect(f'/word?search={search}')
        

        context = {
            'meanings': meanings,
            'synonyms': synonyms,
            'antonyms': antonyms,
        }
        
        return render(request, 'word.html', context)
    
    except RequestException as e:
        messages.error(request, "An error occurred while fetching data. Please try again later.")
        return render(request, 'word.html', {})
    
def PerDictView(request):
    
    
    saved_words = PersonalDictionary.objects.all()
    word_data = []
    
    for word in saved_words:
        search = word.word
        word_id=word.id
        meanings = []
        synonyms = []
        antonyms = []

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

        word_data.append({
            'pk':word_id,
            'word': search,
            'meanings': meanings,
            'synonyms': synonyms,
            'antonyms': antonyms,
        })

    context = {'word_data': word_data}
    return render(request, 'perdict.html', context)


def delete(request, pk):
    try:
        word_to_delete = PersonalDictionary.objects.get(id=pk)
        word_to_delete.delete()
        messages.success(request, "Word deleted successfully.")
    except PersonalDictionary.DoesNotExist:
        messages.error(request, "Word not found.")
    
    return redirect('personal-dictionary')
