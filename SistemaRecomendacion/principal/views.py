from django.shortcuts import render
import shelve
from SistemaRecomendacion.principal.models import UserInformation, Film, Rating
from SistemaRecomendacion.principal.forms import UserForm, FilmForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from SistemaRecomendacion.principal.recommendations import transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches
from SistemaRecomendacion.principal.populate import populateDatabase

# Create your views here.

Prefs = {}  # matriz de usuarios y puntuaciones a cada a items
ItemsPrefs = {}  # matriz de items y puntuaciones de cada usuario. Inversa de Prefs
SimItems = []  # matriz de similitudes entre los items


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def loadDict():
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.film.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()


#  CONJUNTO DE VISTAS

def index(request):
    return render_to_response('index.html')


def populateDB(request):
    populateDatabase()
    return render_to_response('populate.html')


def loadRS(request):
    loadDict()
    return render_to_response('loadRS.html')


# APARTADO A
def search(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            return render_to_response('ratedFilms.html', {'usuario': user})
    else:
        form = UserForm()
    return render_to_response('search_user.html', {'form': form}, context_instance=RequestContext(request))


# APARTADO B
def recommendedFilms(request):
    if request.method == 'GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:2]
            items = []
            for re in recommended:
                item = Film.objects.get(pk=re[1])
                items.append(item)
            return render_to_response('recommendationItems.html', {'user': user, 'items': items},
                                      context_instance=RequestContext(request))
    form = UserForm()
    return render_to_response('search_user.html', {'form': form}, context_instance=RequestContext(request))


# APARTADO C
def similarFilms(request):
    film = None
    if request.method == 'GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm), n=3)
            items = []
            for re in recommended:
                item = Film.objects.get(pk=int(re[1]))
                items.append(item)
            return render_to_response('similarFilms.html', {'film': film, 'films': items},
                                      context_instance=RequestContext(request))
    form = FilmForm()
    return render_to_response('search_film.html', {'form': form}, context_instance=RequestContext(request))