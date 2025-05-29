from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from flashCards.models import Card, Deck


def ownsDeck(viewFunc):
    def wrapped(req, *args, **kwargs):
        deck = Deck.objects.get(id=kwargs['deckId'])
        if deck.owner != req.user:
            return redirect('showDeck', deckId=deck.id)
        return viewFunc(req, *args, **kwargs)
    return wrapped


def listDecks(req):
    decks = Deck.objects.all()
    return render(req, 'listDecks.html', {'decks': decks})


@login_required
def createDeck(req):
    if req.method == "POST":
        deck = Deck(
            name=req.POST["name"],
            owner=req.user
        )
        deck.save()
        return redirect('showDeck', deckId=deck.id)
    return render(req, 'createDeck.html')


def showDeck(req, deckId):
    deck = Deck.objects.get(id=deckId)
    cards = Card.objects.filter(deck=deck).all()
    return render(req, 'showDeck.html', {'deck': deck, 'cards': cards})


@login_required
@ownsDeck
def createCard(req, deckId):
    deck = Deck.objects.get(id=deckId)
    if req.method == "POST":
        card = Card(
            question=req.POST["question"],
            answer=req.POST["answer"],
            deck=deck
        )
        card.save()
        return redirect('showDeck', deckId=deck.id)
    return render(req, 'createCard.html', {"deck": deck})


def showCard(req, deckId, cardId):
    card = Card.objects.get(id=cardId)
    return render(req, 'showCard.html', {'card': card, 'deck': card.deck})


@login_required
@ownsDeck
def editCard(req, deckId, cardId):
    deck = Deck.objects.get(id=deckId)
    card = Card.objects.get(id=cardId)
    if req.method == "POST":
        card.question = req.POST["question"]
        card.answer = req.POST["answer"]
        card.save()
        return redirect('showDeck', deckId=deck.id)
    return render(req, 'editCard.html', {"deck": deck, "card": card})


@login_required
@ownsDeck
def deleteCard(req, deckId, cardId):
    card = Card.objects.get(id=cardId)
    card.delete()
    return redirect('showDeck', deckId=deckId)
