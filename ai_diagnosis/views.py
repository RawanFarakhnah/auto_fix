import requests
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def ai_diagnosis_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_ask = data.get('message')

        api_url = "https://api.aimlapi.com/v1/chat/completions"
        api_key = "347441bca2b3457f99010a24a6263e08"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {"role": "system", "content": "You have extensive knowledge in automotive diagnostics, troubleshooting, and repair. Be descriptive and helpful."},
                {"role": "user", "content": user_ask}
            ],
            "temperature": 0.7,
            "max_tokens": 256
        }

        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()
        reply = result['choices'][0]['message']['content']
        return JsonResponse({
            'user': user_ask,
            'reply': reply
        })
