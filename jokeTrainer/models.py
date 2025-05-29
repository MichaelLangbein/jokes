from django.db import models


class Rating(models.Model):
    rating = models.IntegerField(
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    joke = models.ForeignKey('jokeTrainer.Joke', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating) + "_" + str(self.joke)[:10]


class Joke(models.Model):
    setup = models.CharField(max_length=200)
    punchline = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.setup
