from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Card(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    deck = models.ForeignKey('flashCards.Deck', on_delete=models.CASCADE)

    def __str__(self):
        return self.question
