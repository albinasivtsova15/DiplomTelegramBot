from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from main import bot  # Импортируем экземпляр бота из main.py
import telebot

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        # Получаем обновление от Telegram
        update = json.loads(request.body.decode('utf-8'))
        print("Получен POST-запрос от Telegram:")
        print(json.dumps(update, indent=2, ensure_ascii=False))

        # Передаем обновление в бота
        bot.process_new_updates([telebot.types.Update.de_json(update)])

        return JsonResponse({"status": "received"})
    else:
        print(f"Получен {request.method} запрос")
        return JsonResponse({"status": "not a POST"})
