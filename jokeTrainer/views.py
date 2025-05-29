from django.shortcuts import redirect, render
from .models import Joke, Rating


def listJokes(req):
    jokes = Joke.objects.all()
    return render(req, 'listJokes.html', {'jokes': jokes})


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
    return render(req, 'viewJoke.html', {'joke': joke, 'meanRating': meanRating})
