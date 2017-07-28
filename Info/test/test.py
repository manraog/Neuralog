import pyaudio
import wave
import time
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = ["encender.wav", "apagar.wav"]
 
 
for palabra in WAVE_OUTPUT_FILENAME:
	##### GRABA #################
	audio = pyaudio.PyAudio()
	stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
	print("	PALABRA =>  " + palabra.split('.')[0].upper())
	time.sleep(1)
	print("	** Grabando... **")
	frames = []
	
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print("	** Grabacion terminada **")
  
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
 
	waveFile = wave.open(palabra, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	
	time.sleep(1)
	#### REPRODUCE ##############
	print ("	** Reproduciendo **")

	wf = wave.open(palabra, 'rb')

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
							channels=wf.getnchannels(),
							rate=wf.getframerate(),
							output=True)

	data = wf.readframes(CHUNK)

	while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	p.terminate()
	
	time.sleep(2)
