from django.shortcuts import render
import os
import openai
from django.conf import settings

api_key = settings.OPENAI_KEY

def chatbot_view(request):
    context={}
    chatbot_response=None
    if api_key is not None and request.method=='POST':
        openai.api_key = api_key
        user_input = request.POST.get('message')
        prompt = f'{user_input} in india'

        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            temperature = 0.5
        )
        print(response)
        chatbot_response = response["choices"][0]["text"]
        context["response"] = chatbot_response
    return render(request,'chatbot/chat.html',context)

