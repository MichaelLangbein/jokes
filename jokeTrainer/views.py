from django.shortcuts import redirect, render
from .models import Joke, Rating
from django.db.models import Avg
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


def ownsJoke(viewFunc):
    def wrapperFunc(req, *args, **kwargs):
        jokeId = kwargs['jokeId']
        joke = Joke.objects.get(id=jokeId)
        if joke.owner != req.user:
            return redirect('viewJoke', jokeId=jokeId)
        return viewFunc(req, *args, **kwargs)
    return wrapperFunc


def listJokes(req):
    jokes = Joke.objects.annotate(
        meanRating=Avg('rating__rating')  # 'tablename__fieldname'
    ).order_by('-meanRating')
    return render(req, 'listJokes.html', {'jokes': jokes})


@login_required
def createJoke(req):
    if req.method == "POST":
        joke = Joke(
            setup=req.POST["setup"],
            punchline=req.POST["punchline"],
            owner=req.user
        )
        joke.save()
        return redirect('viewJoke', jokeId=joke.id)
    return render(req, 'createJoke.html')


def viewJoke(req, jokeId):

    joke = Joke.objects.get(id=jokeId)
    ratings = Rating.objects.filter(joke=joke)
    meanRating = sum([r.rating for r in ratings]) / \
        len(ratings) if len(ratings) > 0 else 0

    ownRating = None
    if req.user.is_authenticated:
        ownRating = Rating.objects.filter(
            joke=joke, owner=req.user
        ).first()

    return render(req, 'viewJoke.html', {'joke': joke, 'meanRating': meanRating, 'ownRating': ownRating})


@login_required
@ownsJoke
def rateJoke(req, jokeId):
    if req.method == "POST":
        rating = Rating(
            rating=req.POST["rating"],
            joke=Joke.objects.get(id=jokeId),
            owner=req.user
        )
        rating.save()
        return redirect('viewJoke', jokeId=jokeId)
    else:
        return redirect('viewJoke', jokeId=jokeId)


def jokeRoulette(req):
    randomJoke = Joke.objects.order_by('?').first()

    ratings = Rating.objects.filter(joke=randomJoke)
    meanRating = sum([r.rating for r in ratings]) / \
        len(ratings) if len(ratings) > 0 else 0

    ownRating = None
    if req.user.is_authenticated:
        ownRating = Rating.objects.filter(
            joke=randomJoke, owner=req.user
        ).first()

    return render(req, 'jokeRoulette.html', {'joke': randomJoke, 'meanRating': meanRating, 'ownRating': ownRating})
