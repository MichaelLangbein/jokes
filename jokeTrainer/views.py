from django.shortcuts import redirect, render
from .models import Joke, Rating
from django.db.models import Avg


def listJokes(req):
    jokes = Joke.objects.annotate(
        meanRating=Avg('rating__rating')  # 'tablename__fieldname'
    ).order_by('-meanRating')
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
    ownRating = Rating.objects.filter(
        joke=joke, owner=req.user
    ).first()
    return render(req, 'viewJoke.html', {'joke': joke, 'meanRating': meanRating, 'ownRating': ownRating})


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
