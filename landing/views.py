from django.shortcuts import render
from openai import OpenAI

# Create your views here.
def root(request):
    return render(request, 'landing.html')

def ai(request):
    if request.method == 'POST':
        user_ask = request.POST['talk']
        base_url = "https://api.aimlapi.com/v1"
        api_key = "347441bca2b3457f99010a24a6263e08"
        system_prompt = "You have extensive knowledge in automotive diagnostics, troubleshooting, and repair. Be descriptive and helpful."
        user_prompt = f'{user_ask}'
        api = OpenAI(api_key=api_key, base_url=base_url)
        completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=256,
        )
        
        response = completion.choices[0].message.content
        context = {
                'user':user_ask,
                'bot':response
        }
        return render(request,'ai_chat.html',context)
    return render(request,'ai_chat.html')
