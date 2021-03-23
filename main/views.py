from django.shortcuts import render
from django.http import HttpResponse
from .models import Bot
from doris import Interpretator
from doris import Doris
from django.views.decorators.csrf import csrf_exempt
import secrets
import base64
import datetime

doris = Doris()
doris.load()

def gen_key(request):
    bot = Bot()
    api_key = base64.b64encode(secrets.token_urlsafe(16).encode("utf-8")).decode("utf-8")
    bot.creater = request.GET["creater"]
    bot.api_key = api_key
    bot.save()
    data = '{"status": "ok", "api_key": "'  + str(api_key) + '"}'
    return HttpResponse(str(data))

@csrf_exempt
def get_answer(request):
    bots = Bot.objects.all()
    keys = []
    for bot in bots:
        keys.append(bot.api_key)
    api_key = request.POST['api_key']
    question = request.POST['question']
    if api_key in keys:
        answer = doris.predict(question)
    data = '{"status": "ok", "question": "' +  str(question) + '", "answer": "' +  str(answer) + '"}'
    return HttpResponse(str(data))


@csrf_exempt
def interpretator(request):
    api_key = request.POST['api_key']
    question = request.POST['question']
    answer = request.POST['answer']
    if "images" in request.POST:
        images = request.POST.getlist('images')
        for i in range(len(images)):
            image = base64.b64decode(images[i].encode("utf-8"))
            with open(f'logs/images/image_{i}.jpg', 'wb+') as f:
                f.write(image)
    inter = Interpretator()
    inter.questions = request.POST.getlist('questions')
    inter.answers = request.POST.getlist('answers')
    inter.people_name = request.POST.get('people_name', None)
    inter.people_hobby = request.POST.get('people_hobby', None)
    bots = Bot.objects.all()
    keys = []
    for bot in bots:
        keys.append(bot.api_key)
    if api_key in keys:
        answer = inter.run(question, answer)
    data = '{"status": "ok", "question": "' +  str(question) + '", "answer": "' +  str(answer) + '"}'
    return HttpResponse(str(data))
