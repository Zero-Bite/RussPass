import requests
import json

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

role_input = input("введите, какая роль модели, например, должна модель отвечать как академик или как школьник: ")
user_input = input("введите ваш вопрос: ")

with open('token.txt', 'r') as f:
    token = f.read().rstrip()

payload = json.dumps({
  "model": "GigaChat",
  "messages": [ {
          "role": "system",
          "content": role_input,
          },   {
      "role": "user",
      "content": user_input,
      },
           
  ],
  
  "temperature": 1,
  "top_p": 0.1,
  "n": 1,
  "stream": False,
  "max_tokens": 1500,
  "repetition_penalty": 1,
  "update_interval": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {token}'
}

response = requests.request("POST", url, headers=headers, data=payload, verify='ca.cer')


#print(dir(json.loads(response.text)))
#print(type(dict.items(json.loads(response.text))))
#print(dir(response.json))
print(dict(json.loads(response.text))['choices'][0]['message']['content'])
#i = 1
#for key, value in  dict.items((json.loads(response.text))):
    #print(i, key, value)
    #if i == 1:
        #print(value[0]['message']['content'])
    #i += 1
#print(dict.items(json.loads(response.text))['choices'][0]['content'])

