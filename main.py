import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import asyncio
from googletrans import Translator
async def main():
    duration = 5  # секунды записи
    sample_rate = 44100

    print("Говори...")
    recording = sd.rec(
    int(duration * sample_rate), # длительность записи в сэмплах
    samplerate=sample_rate,      # частота дискретизации
    channels=1,                  # 1 — это моно
    dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)
    print("Запись завершена, теперь распознаём...")

    recognizer = sr.Recognizer()
    translator = Translator()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("Ты сказал:", text)
        trnsltd = await translator.translate(text, dest="en")
        print("🌍 Перевод на английский:", trnsltd.text)
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")

asyncio.run(main())