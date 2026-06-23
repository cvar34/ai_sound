import time 
import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import asyncio
from googletrans import Translator

duration = 5  # секунды записи
sample_rate = 44100

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

async def main():
    while True:
        lvl = input("Выберите сложность (Easy, Medium, Hard)").lower()
        word = random.choice(words_by_level[lvl])
        print("Ваше слово", word)
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)

        print("Говори...")
        recording = sd.rec(
        int(duration * sample_rate), # длительность записи в сэмплах
        samplerate=sample_rate,      # частота дискретизации
        channels=1,                  # 1 — это моно
        dtype="int16")               # формат аудиоданных
        sd.wait()  # ждём завершения записи

        wav.write("output.wav", sample_rate, recording)
        print("Запись завершена")

        recognizer = sr.Recognizer()
        translator = Translator()

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print("Ты сказал:", text)
            trnsltd = await translator.translate(word, dest="en")
            print("🌍 Перевод загадонного слова на английский:", trnsltd.text)
            if text == trnsltd.text: 
                print("Правильно")
            else:
                print("Неправильно")
        except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
            print("Не удалось распознать речь.")
        except sr.RequestError as e:             # - если нет интернета или API недоступен
            print(f"Ошибка сервиса: {e}")

        c = input("Играем еще?")
        if c == "Нет":
            break

asyncio.run(main())
