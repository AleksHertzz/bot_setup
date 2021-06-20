import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
word = ''
res = ''
vec = ''
user_result = None
tex_t = []
vec_ = []
with open("vectors.tsv") as f:
    for line in f:
        vec_ += line.strip().splitlines()
with open("metadata.tsv") as f:
    for line in f:
        tex_t += line.strip().splitlines()


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Как дела?")
    item2 = types.KeyboardButton("Найти слово")
    item3 = types.KeyboardButton("Найти соседей")
    item4 = types.KeyboardButton("Показать векторы")

    markup.add(item1, item2, item3,item4)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name} ".format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup = markup)

@bot.message_handler(content_types =['text'])
def lala(message):
    # keyboard
    if message.chat.type == 'private':
        if message.text == 'Как дела?':
            bot.send_message(message.chat.id, 'Всё хорошо,я еще в доработке')
        elif message.text == 'Найти слово':
            msg = bot.send_message(message.chat.id, 'Введите слово:')
            bot.register_next_step_handler(msg, process_1)
        elif message.text == 'Найти соседей':
            msq = bot.send_message(message.chat.id, 'Введите слово')
            bot.register_next_step_handler(msq, process_2)
        elif message.text == 'Показать векторы':
            mwq = bot.send_message(message.chat.id, 'Введите слово')
            bot.register_next_step_handler(mwq, process_3)
        else:
            bot.send_message(message.chat.id, 'Чего???')

def process_1(message, user_result = None):
        word = message.text
        if word in tex_t:
            msg = bot.send_message(message.chat.id, 'Такое слово есть')
        else:
            msg = bot.send_message(message.chat.id, 'Слово отсутствует')


def process_2(mess, user_result = None):
    res = mess.text
    neighbor = ''
    num = 3
    print(num)
    if res in tex_t:
        index = int(tex_t.index(res))
        for i in range(1,num):
            neighbors = tex_t[index - i] + ' ' + tex_t[index + i] + ' '
            neighbor += neighbors
        msq = bot.send_message(mess.chat.id, neighbor)
    else:
        msq = bot.send_message(mess.chat.id, 'Слово отсутствует')



def process_3(vector,user_result = None):
    vec = vector.text
    index = int(tex_t.index(vec))
    vectors = vec_[index]
    mwq = bot.send_message(vector.chat.id, vectors)

bot.polling(none_stop=True)

