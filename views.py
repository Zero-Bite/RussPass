from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


import uuid


import time
import csv

import requests
import json
import os

#import openai
#openai.api_key = 'YOUR_API_KEY'

def receive_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    with open('token_init.txt', 'r') as f:
        token_init = f.read().rstrip()
        
        
    payload='scope=GIGACHAT_API_PERS'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'RqUID': str(uuid.uuid4()),
      'Authorization': f'Basic {token_init}'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, verify='ca.cer')
    
    print(response.text)
    new_token = dict(json.loads(response.text))["access_token"]
    print(new_token)
    
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    filename = 'token.txt'
    
    
    full_path = os.path.join(parent_dir, filename)
    with open(full_path, 'w') as f:
        f.writelines(new_token)    


csrf_dict = {}

prompt_vladimir = 'Владимир — один из древнейших городов России, история которого насчитывает более 1000 лет. Расположенный на реке Клязьма в 180 км от Москвы, Владимир был основан в конце 10 века и являлся одним из центров Древней Руси, а ныне — это административный центр Владимирской области. Владимир был одним из центров древнерусского зодчества, и в городе сохранились многочисленные старинные достопримечательности, самые известные из которых – Успенский собор, Дмитриевский собор и Золотые ворота. Отели: Гостиница Владимир, АМАКС Золотое Кольцо, Гостиница Застава, Ильинка-отель, Орион Отель. Интересные факты: В течение нескольких веков Владимир был сначала фактической, а затем номинальной столицей Руси. Во Владимире сохранилось три памятника архитектуры, построенных до монголо-татарского завоевания: Золотые ворота, Успенский и Дмитриевский соборы. Раньше ворот в городе было 8, но до наших дней сохранились лишь одни из них.'
prompt_piter = 'Санкт-Петербург - второй по численности населения город России, который часто называют «Северной столицей». Расположен на северо-западе европейской части страны в восточной акватории Балтийского моря в устье реки Невы. Санкт-Петербург - один из самых потрясающих городов Европы, имеющий огромное историческое и культурное наследие, а также волшебную атмосферу. Это город удивительной архитектуры, романтики и вдохновения, разводных мостов и белых ночей. Отели: Novotel St Petersburg Centre, Domina St.Petersburg, Гранд Отель Европа. Интересные факты: самый северный из крупных мегаполисов мира, его иногда называют «Город белых ночей», Протяженность трамвайных путей в городе составляет более 600 км. Этот факт занесен в Книгу рекордов Гиннесса. Купол Исаакиевского собора, внутри которого может поместиться на 14 000 верующих, покрыт чистым золотом.'
prompt_kamchtka = 'Практически на самом краю России раскинулся камчатский полуостров, омываемый с одной стороны Охотским морем, а с другой водами Тихого океана. Камчатка — это предмет национальной гордости, ведь на её территории сосредоточено всё многообразие северной природы. Густые леса, кристально чистые озера, стремительные реки и, что самое главное, вулканы. Камчатка входит в состав Тихоокеанского вулканического огненного кольца, так как на её территории существует больше 300 вулканов: большинство из них время от времени проявляют активность, а около 30 регулярно извергаются. Мощь этих гигантов поражает воображение и заслуживает того, чтобы быть увиденной. В этой статье мы расскажем не только о вулканах Камчатки, но и о других достопримечательностях полуострова, увидеть которые стоит хотя бы раз в жизни. название отелей Лагуна - 5600 руб, Командор-5700, Sopka - 4500, Тайны Камчатки - 40000, Yu Hotel - 11000. Интересные факты:На Камчатке совсем нет змей. И обитает лишь один вид лягушек, и тот был завезён людьми.Популяция медведей на полуострове составляет около 20.000 особей.По полуострову проходит так называемое Тихоокеанское огненное кольцо, это самый богатый на вулканы и землетрясения участок на Земле'

prompt_syzdal = 'В 1965 году Суздаль посетил миллиардер Ротшильд. Пораженный богатой историей и красотой храмов, он заявил: «Если бы мне одолжили этот город на пару лет, я бы увеличил свое состояние вдвое». Поговаривают, что именно после его слов советские власти принялись делать из Суздаля туристический центр. Сегодня сюда приезжает 1,5 миллиона туристов в год. Знакомство с местными достопримечательностями — это путешествие вглубь веков, которое мало кого оставляет равнодушным. Отели: Отель Сокол, Горячие ключи, Светлый теремИнтересные факты: Суздаль (точнее, Суждаль) впервые был упомянут летописцем в 1024 году. С 2002 года в Суздале ежегодно проводится главный российский фестиваль мультфильмов. В Суздале проживает менее 10 тысяч человек, зато на территории города разместились 53 храма. '

prompt_moscow = 'Москва — столица России, город федерального значения. Это культурно-исторический, экономический и политический центр страны. На его территории размещаются органы государственной власти РФ.Москва — крупнейший по численности населения город России: здесь живут 12,6 млн человек (2021 г.), что составляет 8,6% населения страны. В 2012 г. площадь столицы была увеличена в 2,5 раза (2561,5 км²).'
prompt_sergeev = 'Сергиев Посад — столица православия и один из восьми городов, входящих в туристический маршрут «Золотое кольцо России». Сюда едут, чтобы ощутить дыхание древней истории и познакомиться с уникальными памятниками архитектуры. В списке обязательных к посещению достопримечательностей — Троице-Сергиева лавра, святые источники, тематические музеи, городской парк, старинные усадьбы и многое другое.'
prompt_pere = 'Достопримечательности Переславля-Залесского включают в себя большое количество уникальных и красивых памятников архитектуры разных веков. Здесь вы сможете познакомиться с разными стилями и внимательно рассмотреть детали каждого здания. Кроме того, город наполнен интересными музеями, тематика которых сможет удивить даже самого опытного туриста. А любители тихого и размеренного отдыха смогут провести время, наслаждаясь свежим воздухом и красотой местной природы.'
prompt_rostov = 'Мало кто знает, что «Великим» Ростов стал благодаря предприимчивости местных купцов. Тем самым они хотели придать родному городу значимости и избежать путаницы с однофамильцем на Дону. Но Ростов, действительно, Великий. Это один из древнейших городов России. Первые упоминания о нем относятся к 862 году. Туристы со всего мира едут сюда за многовековой историей, красотой православных святынь и очарованием провинциального, но все равно великого города.'
prompt_yaroslavl = 'Туризм в Ярославле развивается уже много десятилетий — почти каждая историческая достопримечательность тщательно отреставрирована, а большой музейный комплекс не хуже многих московских. Город богат прежде всего белокаменными памятниками допетровских времен, но на этом его наследие не заканчивается — здесь есть и любопытные сооружения советской эпохи, и один из самых удачных примеров современной православной архитектуры.'
prompt_kostroma = 'Когда-то в Костроме стремились хотя бы раз в жизни побывать все российские императоры. В наше время уникальный город на левом берегу Волги не растерял своей привлекательности. Сюда приезжает более миллиона туристов в год, причем не только из России, но и из-за рубежа. Достопримечательности Костромы разнообразны: старинные монастыри, храмы, купеческие особняки, театры, музеи, памятники и т.д. Расположены все самые интересные места практически бок о бок, поэтому их вполне реально обойти за 1,5-2 дня.'
prompt_ivanovo = 'Иваново не зря привлекает несколько сотен тысяч туристов в год. Помимо невест, этот город примечателен усадьбами, храмами, музеями, бывшими фабричными зданиями и памятниками советского конструктивизма. А еще именно здесь в начале прошлого столетия зародилось рабочее движение, которое в итоге привело страну к революции 1917 года.'


def get_completion(prompt):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    role = f"ты - профессиональный туристический робот-планировщик путешествий для туриста.Ты рассказиваешь только о городах Российской Федерации. Сначала ты должен спросить о городе, который пользователь хочет посетить. Далее ты предлагаешь самые популярные туристические места для туристов, которые хотят посетить {prompt}, а также рассказываешь о самых интересных местах в этом городе. Расскажи об этом в 3-4 красочных предложениях. Далее дай ссылку на russpass.ru, и спроси пользователя все ли вам понравилось. Не повторяй слова"
    with open('token.txt', 'r') as f:
        token = f.read().rstrip()
        payload = json.dumps({
          "model": "GigaChat",
          "messages": [{
              "role": "system",
              "content": role,
          }, {
              "role": "user",
              "content": prompt,
          },

          ],

          "temperature": 1,
          "top_p": 0.1,
          "n": 1,
          "stream": False,
          "max_tokens": 450,
          "repetition_penalty": 1,
          "update_interval": 0
        })
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': f'Bearer {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify='ca.cer')
        answer = dict(json.loads(response.text))['choices'][0]['message']['content']

    return answer


def chat_view(request):
    print("starting not testing")
    receive_token()
    
    try:
        # if request.method == 'GET':
            #prompt = "Какие самые интересные достопримечатальности?"
            # try:
                #place = request.GET['prompt_place']

            # except:
                #place = "города Золотого кольца центральной части России"
            # print(place)
            ##response = get_completion(prompt, place)
            # return JsonResponse({'response': response})

        place = "города Золотого кольца центральной части России"
        print(place)
        if request.method == 'POST':
            from_frontend = dict(json.loads(request.POST.get('to_django')))
            prompt = from_frontend['prompt']
            csrf_token = from_frontend['csrftoken']
            print(prompt, csrf_token)
            #with open('data.csv', 'r') as f:
                #csv_reader = csv.DictReader(f)
                #for element in csv_reader:
                    #print(element)
                    
            #for k, v in csv_reader:
                #csrf_dict[k] += v
            #else:
                #csrf_dict[csrf_token] += prompt
            try:
                old_text = csrf_dict[csrf_token]
            except Exception as err:
                print(err.args)
                old_text = ' '
            csrf_dict[csrf_token] = old_text + " " + prompt
            prompt = csrf_dict[csrf_token]
            print(prompt)
            print(csrf_dict)


            #with open('data.csv', 'a') as f_w:
                #writer = csv.DictWriter(f_w, fieldnames=['csrf', 'value'])
                #writer.writerow(csrf_dict)
                
            if str(prompt).lower() == 'москва':
                response = get_completion(prompt_moscow)  # , place)
            # response = "WRONG"
            elif str(prompt).lower() == 'сергиев посад':
                response = get_completion(prompt_sergeev)
            elif str(prompt).lower() == 'переславль':
                response = get_completion(prompt_pere)
            elif str(prompt).lower() == 'ростов':
                response = get_completion(prompt_rostov)
            elif str(prompt).lower() == 'ярославль':
                response = get_completion(prompt_yaroslavl)
            elif str(prompt).lower() == 'кострома':
                response = get_completion(prompt_kostroma)
            elif str(prompt).lower() == 'иваново':
                response = get_completion(prompt_ivanovo)
            elif str(prompt).lower() == 'суздаль':
                response = get_completion(prompt_syzdal)
            elif str(prompt).lower() == 'владимир':
                response = get_completion(prompt_vladimir)
            elif str(prompt).lower() == 'питер' or  str(prompt).lower() == 'санкт-петербург':
                response = get_completion(prompt_piter)
            elif str(prompt).lower() == 'камчатка':
                response = get_completion(prompt_kamchtka)    
            else:
                response = get_completion(prompt)  # , place)
            return JsonResponse({'response': response}) 
        return render(request, 'chat.html')
    except Exception as err:
        print("error")
        print(err.args)
        


def index_view(request):

    try:
        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            text = f"I've got: {prompt}"
            print(text)
            print("index")
            response = text
            return JsonResponse({'response_test_from_backend': response})
    except Exception as err:
        print(err.args)
    return render(request, 'index.html')


#def test_view(request):
    #try:
        #if request.method == 'POST':
            #prompt_test = request.POST.get('prompt_test_input_to_backend')
            #text = f"I've got: {prompt_test}"
            #print(text)
            #response_test = text
            #time.sleep(5)
            #return JsonResponse({'response_test_from_backend': response_test})
    #except Exception as err:
        #print(err.args)
    #return render(request, 'test.html')


def map_view(request):
    try:
        if request.method == 'POST':
            prompt_test = request.POST.get('prompt_test_input_to_backend')
            text = f"I've got: {prompt_test}"
            print(text)
            response_test = text
            return JsonResponse({'response_test_from_backend': response_test})
    except Exception as err:
        print(err.args)
    return render(request, 'map.html')


def game_view(request):
    try:
        if request.method == 'POST':
            prompt_test = request.POST.get('prompt_test_input_to_backend')
            text = f"I've got: {prompt_test}"
            print(text)
            response_test = text
            return JsonResponse({'response_test_from_backend': response_test})
    except Exception as err:
        print(err.args)
    return  render(request, 'game.html')# HttpResponse('<h1> Please see game in presentation ))</h1>')




