import telebot
import whisper

TOKEN = '6568818186:AAEFmlLXI1SADQVAsDykg3feZryESPfcCjA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
  bot.reply_to(message, "Welcome, my name is Marcus and I am here to transcribe your audio recordings (& files) to text. \n\nSend /record to begin.")


@bot.message_handler(commands=['record'])
def record_voice(message):
  markup = telebot.types.ForceReply(selective=False)
  bot.send_message(message.chat.id, "Record your voice now and I will transcribe it. \n\nPlease speak clearly into your microphone in order to get an accurate transcription", reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
  file_id = message.voice.file_id
  voice_info = bot.get_file(file_id)
  voice_file = bot.download_file(voice_info.file_path)

  with open("voice.ogg", "wb") as f:
    f.write(voice_file)

  model = whisper.load_model("medium")
  result = model.transcribe("voice.ogg")

  bot.reply_to(message, f"Transcription: {result['text']}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
  bot.reply_to(message, "Send /record to start recording your voice.")

bot.polling()

