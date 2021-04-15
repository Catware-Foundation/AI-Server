
try: # Мммм, весь код в трай-эксцепт, звучит хайпово

    def PlusWrite(text, target):
        file = open(str(target), 'a', encoding='utf-8')
        file.write(str(text))
        file.close()

    def ReadFF(file): # Read From File
        try:
            Ff = open(file, 'r', encoding='UTF-8')
            Contents = Ff.read()
            Ff.close()
            return Contents
        except:
            return None

    def Similar(first, second): # Similar strings
        if not len(first) == len(second):
            return False
        if len(first) - sum(l1==l2 for l1, l2 in zip(first, second)) > 3:
            return False
        return True

    def writeTo(text, target):
        file = open(str(target), 'w', encoding='utf-8')
        file.write(str(text))
        file.close()
    status = "normal"
    import time
    start = time.time() # pip install flask markovify googletrans pymorphy2 DAWG pyaspeller
    import os
    from flask import Flask, request, Response
    import markovify
    from googletrans import Translator
    translator = Translator()
    from random import randint, choice
    from pyaspeller import Word
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()

    accesstoken = "Ваш токен для доступа к некоторым функциям CatwareAI"

    database_files = os.listdir("databases")
    database_files2 = os.listdir("bread")
    user_database_files = os.listdir("user_databases")

    sucktions = ""
    for x in database_files2:
        sucktions += ReadFF("bread/" + x) # Папки с текстом для Markovify
    text_model = markovify.Text(sucktions).compile()

    answers = {"фывфыв": ["у тебя говно мотив"]} # Начальная база.

    for load in database_files: # Папки с базами для VK Iha Bot
        try:
            cont = ReadFF("databases/" + load)
            for line in cont.split("\n"):
                try:
                    answers[str(line.split("\\")[0]).lower()].append(line.split("\\")[1])
                except:
                    answers[str(line.split("\\")[0]).lower()] = [line.split("\\")[1]]
        except:
            pass

    for load in user_database_files: # Пользовательские базы данных (на самом деле просто вторая папка)
        try:
            cont = ReadFF("user_databases/" + load)
            for line in cont.split("\n"):
                try:
                    answers[str(line.split("\\")[0]).lower()].append(line.split("\\")[1])
                except:
                    answers[str(line.split("\\")[0]).lower()] = [line.split("\\")[1]]
        except:
            pass



    def correct(txt):
        text = ""
        for ae in txt.split(" "):
            check = Word(ae)
            try:
                if check.correct:
                    text += ae + " "
                else:
                    text += check.variants[0] + " "
            except:
                text += ae + " "
        if text.endswith(" "):
            text = text[:-1]
        return text

    def getans(txt):
        notgetted = True
        ret = "none"
        while notgetted:
            global answers
            keyz = list(answers.keys())
            try:
                txt = txt.lower()
                ret = choice(answers[txt])
                notgetted = False
            except Exception as e:
                txt = txt[:-1]
        if ret == "none":
            return "error"
        else:
            return ret

except Exception as e:
    status = "Failed to load: " + str(e)

app = Flask(__name__)

@app.route("/add") # /add?access_token=токен&text=триггер\ответ
def corrs():
    if str(request.args.get("access_token")) == accesstoken:
        try:
            PlusWrite(str(request.args.get("text")) + "\n", "user_databases/vkbase")
            text = str(request.args.get("text"))
            try:
                answers[str(text.split("\\")[0]).lower()].append(text.split("\\")[1])
            except:
                answers[str(text.split("\\")[0]).lower()] = [text.split("\\")[1]]
            return "окей"
        except:
            return "нахуй пошёл" # ХААХХАХАХАХА ИЗВИНИТЕ НЕ СДЕРЖАЛСЯ, ЛЮБЛЮ ТАК ДЕЛАТЬ
    else:
        return "Доступ запрещён"

@app.route("/execute") # КООООНСОСЬ ВЫ ВСЕ ЛОХИ КОНСОСЬ ВЫ ВСЕ ЛОХИ КОООНСООООСЬ /execute?access_token=токен&exec=код()
def corrs_(): 
    if str(request.args.get("access_token")) == accesstoken:
        try:
            exec(request.args.get("exec"))
            return 'ok'
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            message('Error: \n' + "\n".join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    else:
        return 404

@app.route("/correctword") # url?text=Йа умир два годы назат (яндекс спеллер, исправляет ваш неграмотный русский)
def corr():
    try:
        text = str(request.args.get("text"))
        return correct(text)
    except:
        return "Error"

@app.route('/gen') # /gen?text=Привет! и он дёргает базы
def generate():
    try:
        text = str(request.args.get("text")).lower()
        try:
            msg = getans(text)
        except Exception as e:
            msg = str(e)
    except:
        msg = "Я не ебу что тебе ответить, потому что я ещё глупенький и плохо взаимодействую с базами((((("
    return msg

@app.route('/xitext') # /xitext?text=Мы - русские люди и он тебе возвратит "мы русский людь"
def xitext():
    nt = []
    try:
        text = str(request.args.get("text"))
        try:
            text = text.split(" ")
            for x in text:
                try:
                    k = morph.parse(x)[0][2]
                    nt.append(k)
                except:
                    nt.append(x)
            msg = " ".join(nt)
        except Exception as e:
            msg = str(e)
    except:
        msg = "Я не ебу что тебе ответить, потому что я ещё глупенький и плохо взаимодействую с базами((((("
    return msg

@app.route("/bread") # /bread - дёргает Markovify
def breadgen():
    return text_model.make_sentence()

@app.route("/breadrestart") # Переподгрузка какой то хуйни (вроде как бредоген марковифе)
def breadrestart():
    if str(request.args.get("access_token")) == accesstoken:
        try:
            global text_model
            sucktions = ""
            for x in database_files2:
                sucktions += ReadFF("bread/" + x)
            text_model = markovify.Text(sucktions).compile()
            return "ok"
        except Exception as e:
            return "fail: " + str(e)
    else: return Response("Access denied", status=401, mimetype='application/json')

@app.route('/')
def index():
    return """
    <h1><pre>
Catware AI 0.1 is online!

Приветствуем вас на базовом сервере Catware AI!
Вы можете узнать о нас, если перейдёте на домашнюю страницу Catware: https://catware.space/
За получением документации о Catware AI можно обратиться к разработчикам Catware.</pre></h1>"""

@app.route("/serverstatus")
def stat():
    return "Статус сервера - занято " + str(len(answers)) + " байт. В сети " + str(time.time() - start) + " секунд. CatABMS Server 0.1", 418

@app.route("/voicebread")
def voicebread():
    if "text" in request.args.keys() and str(request.args.get("access_token")) == accesstoken:
        PlusWrite(request.args.get("text") + " ", "bread/voice.txt")
        return Response("Success", status=200, mimetype='application/json')
    else:
        return Response("Access denied", status=401, mimetype='application/json')
