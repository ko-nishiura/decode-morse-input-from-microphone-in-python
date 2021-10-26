import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import scipy.io.wavfile
import pyaudio
import wave
import threading

wav_file_name = "cw.wav"

MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def morse_analysis():
    rate, data = scipy.io.wavfile.read(wav_file_name)
    N = data.shape[0]
    envelope = np.abs(signal.hilbert(data))
    list1 = []
    for i in range(0, len(envelope), 300):
        if abs(envelope[i]) > 650:
            list1.append(i)
    count = 0
    num = 0
    liat2 = []
    into = ""
    if len(list1) > 0:
        for i in range(1, len(list1)):
            if (list1[i] - list1[i - 1]) < 2000:
                pass
            else:
                if (list1[i - 1] - list1[num]) > 5999:
                    liat2.append(i - 1)
                    into += "-"
                    # print("-", end="")
                elif (list1[i - 1] - list1[num]) > 2000:
                    liat2.append(i - 1)
                    into += "."
                    # print("・", end="")
                count += 1
                num = i
        if (list1[len(list1) - 1] - list1[num]) > 5999:
            liat2.append(i - 1)
            into += "-"
            # print("-")
        elif (list1[len(list1) - 1] - list1[num]) > 2000:
            liat2.append(i - 1)
            into += "."
            # print("・")

        n = 0
        for i in range(0, len(liat2)):
            if (list1[liat2[i] + 1] - list1[liat2[i]]) > 5999:
                for k, v in MORSE_CODE_DICT.items():
                    if v == into[n:i + 1]:
                        print(k, end="")
                n = i + 1
            if i == len(liat2) - 1:
                for k, v in MORSE_CODE_DICT.items():
                    if v == into[n:i + 1]:
                        print(k, end="")
                n = i + 1

    else:
        pass
        # print("No morse")


def recording():
    RECORD_SECONDS = 5  # 録音する時間の長さ（秒）
    WAVE_OUTPUT_FILENAME = wav_file_name  # 音声を保存するファイル名
    iDeviceIndex = 1  # 録音デバイスのインデックス番号

    # 基本情報の設定
    FORMAT = pyaudio.paInt16  # 音声のフォーマット
    CHANNELS = 1  # モノラル
    RATE = 44100  # サンプルレート
    CHUNK = 2 ** 11  # データ点数
    audio = pyaudio.PyAudio()  # pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=iDeviceIndex,  # 録音デバイスのインデックス番号
                        frames_per_buffer=CHUNK)

    # recording
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # finished recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


recording()
th = threading.Thread(target=morse_analysis)
th.start()

while True:
    recording()
    th.join()
    th = threading.Thread(target=morse_analysis)
    th.start()
