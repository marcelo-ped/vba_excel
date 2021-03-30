"""from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array('h', silence)
    r.extend(snd_data)
    r.extend(silence)
    return r

def record():
	
	Record a word or words from the microphone and 
	return the data as an array of signed shorts.

	Normalizes the audio, trims silence from the 
	start and end, and pads with 0.5 seconds of 
	blank sound to make sure VLC et al can play 
	it without getting chopped off.
	
	p = pyaudio.PyAudio()
	wf = wave.open(path, 'rb')
	CHANNELS = wf.getnchannels()
	RATE = wf.getframerate()
	stream = p.open(format=FORMAT, channels=1, rate=RATE,
		input=True, output=True,
		frames_per_buffer=CHUNK_SIZE)

	num_silent = 0
	snd_started = False
	data_all = array('h')
	num_frames = wf.getnframes()
	read_frames = 0
	#first loop to verify when silent stop
	while read_frames < num_frames:
		# little endian, signed short
		sound = wf.readframes(self.CHUNK_SIZE)
		data_chunk = np.array(wave.struct.unpack("%dh"%(len(sound)/2), sound)) #array('h', wf.readframes(self.CHUNK_SIZE))
		data_all.extend(data_chunk)
	sample_width =  p.get_sample_size(p.get_format_from_width(wf.getsampwidth()))
	stream.stop_stream()
	stream.close()
	p.terminate()

	#r = normalize(r)
	#r = trim(r)
	data_all = add_silence(data_all, 1)
	return sample_width, data_all

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

if __name__ == '__main__':
#    print("please speak a word into the microphone")
	mypath = f"{os.path.dirname(os.path.realpath(__file__))}"
	onlyfolder = [folder for folder in listdir(mypath) 
		if not isfile(join(mypath, folder))]
	onlyfiles = []

	for f in onlyfolder:
		#onlyfiles.append(listdir(f))
		files = [file for file in listdir(f)]
		files.sort()
		for a in files:
			if a.endswith("wav"):
				music= f"{f}/{a}"
				record_to_file(f"{music}")
#    print("done - result written to demo.wav")

"""
from pydub import AudioSegment,silence
from os import listdir
from os.path import isfile, join
import os

if __name__ == "__main__":
	mypath = f"{os.path.dirname(os.path.realpath(__file__))}"
	onlyfolder = [folder for folder in listdir(mypath) 
		if not isfile(join(mypath, folder))]
	onlyfiles = []

	for f in onlyfolder:
		#onlyfiles.append(listdir(f))
		files = [file for file in listdir(f)]
		files.sort()
		for a in files:
			if a.endswith("wav"):
				music= f"{f}/{a}"
				print(f"{f}/{a}")
				sound = AudioSegment.from_file(f"{mypath}/{music}", format="wav")
				beginning = sound[:1000]
				ending = sound[-1000:]
				silence_m = silence.detect_silence(beginning, min_silence_len=100, silence_thresh=-16)
				silence_sound = AudioSegment.silent(duration=1000)
				sound_edited = AudioSegment.from_file(f"{music}", format="wav")
				"""if silence_m:
					if int(silence_m[0][0]) > 100 or int(silence_m[0][1]) < 400:
						print(silence_m[0][1])
						sound_edited = silence_sound + sound
				else:"""
				#sound_edited = silence_sound + sound
				silence_m = silence.detect_silence(ending, min_silence_len=100, silence_thresh=-16)
				"""if silence_m:
					if int(silence_m[0][0]) > 100 or int(silence_m[0][1]) < 400:
						print(silence_m[0][1])
						sound_edited =  sound + silence_sound
				else:"""
				sound_edited =silence_sound + sound_edited + silence_sound
				sound_edited.export(f"{mypath}/{music}", format="wav")

