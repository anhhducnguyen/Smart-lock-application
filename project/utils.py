import random


def badge_callback(request):
    return f"+{random.randint(1, 99)}"  