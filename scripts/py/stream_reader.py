'''
This program records audio from the microphone when speech has been detected, and sends it in 20ms frames
to the keyword spotter. The spotter then tries to identify which words are present in the recording/
'''
from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for
from scipy.io import wavfile
from datetime import datetime
from os import path, system
from mel_converter import convert_to_mel
from normalizer import normalize
from padder import pad_tokens
from keras.models import model_from_json
from keras import backend as K
import subprocess
import numpy as np
import re, os, shutil
import wave

class StreamReader():
	
	categories = [
					'None',
					'akatambi',
					'app',
					'bluetooth',
					'damu',
					'fayilo',
					'folder',
					'galawo',
					'gulawo',
					'koma awo',
					'lekera awo',
					'menu',
					'task_manager',
					'vaako',
					'webake',
					'wezeeko',
					'wifi',
					'wumula',
					'zanya',
					'zikira',
				]
	commands = [
					'',
					'',
					'',
					'',
					'',
					'',
					'',
					'nautilus',
					'nautilus',
					'pkill,-KILL -u $USER',
					'',
					'',
					'gnome-system-monitor,',
					'shutdown,-rf,now',
					'shutdown,-f,now',
					'',
					'',
					'',
					'',
					'shutdown,-f,now'
				]

	'''
	categories = ['None', 'damu', 'galawo', 'menu', 'task_manager', 'wuumula']
	commands = ['', 'Unset', 'pkill,-KILL -u $USER', 'nautilus,', 'gnome-system-monitor,', 'shutdown,-f']'''
	
	recognized_keyword = None
	command = None

	def __init__(self):
		self.asource = ADSFactory.ads(record=True, max_time=4)
		self.validator = AudioEnergyValidator(sample_width=2, energy_threshold=50)
		self.tokenizer = StreamTokenizer(validator=self.validator, min_length=20, max_length=1000, max_continuous_silence=30)
		self.player = player_for(self.asource)

		self.model = self.load_cnn('../model/final_cnn_model.json', '../model/weights_final_cnn.h5')
		self.model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

	#CALLBACK FOR NEXT PROCESSING
	def echo(self, data, start, end):
		if (self.audio_file is not None):
			recording = self.asource.read()
		else:
			recording =  b''.join(data)
			print("Acoustic Activity at: {0}--{1}".format(start, end))

		print(recording)
		#data = np.array(data)
		#serialized = np.frombuffer(data)
		
		#print(len(hex_data))
		#print(len(recording))
		normalize(recording)
		pad_tokens('tmp.wav2')
		sample_rate, normalized_signal = wavfile.read('tmp.wav2')
		print(sample_rate)
		print(len(normalized_signal))
		banks = convert_to_mel(normalized_signal)
		banks = np.array(banks)
		Banks = banks.reshape(1, 98, 40, 1)
		#np.save('test.npy', Banks)

		z = self.model.predict(Banks)
		p = z[0].tolist().index(max(z[0]))
		self.recognized_keyword = self.categories[p]
		print(self.recognized_keyword)

		'''
		frame_length, step_size = 16000, 64000
		no_of_shifts = int(64000 / step_size) - int(frame_length / step_size)
		print(no_of_shifts)
		#keyword = None
		prob = 0
		for i in range(0, no_of_shifts):
			l = int(i*320)
			banks = convert_to_mel(normalized_signal[l:l+frame_length])
			banks = np.array(banks)
			np.save('test.npy', banks)
			#banks = np.load('sd.npy')
			Banks = banks.reshape(1, 98, 40, 1)
			z = self.model.predict(Banks)
			print(z)
			p = z[0].tolist().index(max(z[0]))
			prob += p
			self.recognized_keyword = self.categories[p]
			#self.recognized_keyword = self.categories[np.argmax(z[0], -1)]
			#com = self.commands[p]
			print(self.recognized_keyword)
		final = int(np.ceil(prob/no_of_shifts))
		print(prob/no_of_shifts)
		print(final)
		self.recognized_keyword = self.categories[final]'''

		K.clear_session()
		os.remove('tmp.wav2')
		os.remove('tmp.wav')

		#self.command = re.split(',', com)
		#print(max(z[0]))
		#print(self.recognized_keyword)
		#subprocess.call([self.command[0], self.command[1]])
		#print(normalized_signal.get_array_of_samples())

		#print(normalized_signal.get_array_of_samples())
		#frame = np.array()

		#with open(datetime.today().isoformat() + 'XX.txt', 'w') as f:
		#	f.write(recording)
		#player.play(recording)

	def load_cnn(self, name, weights):
		with open(name, 'r') as json_file:
			loaded_model_json = json_file.read()
		loaded_model = model_from_json(loaded_model_json)
		# Load weights into new model
		loaded_model.load_weights(weights)
		print("loaded model from disk")
		return loaded_model

	def main(self, audio_file=None):
		self.audio_file = audio_file
		if (self.audio_file is None):
			print("RECORDING STARTED")
			self.asource.open()
			self.tokenizer.tokenize(self.asource, callback=self.echo)
		else:
			print("AUDIO PROCESSING STARTED")
			#DELETE TOKENS FOLDER
			shutil.rmtree('../../tokens', ignore_errors=True)
			shutil.rmtree('../../data', ignore_errors=True)
			#CREATE tokens/tmp FOLDER
			os.makedirs('../../tokens/temp')
			#CREATE tmp/test AND tmp/train
			os.makedirs('../../tokens/temp/test')
			os.makedirs('../../tokens/temp/train')
			#COPY AUDIO FILE TO tokens/tmp/test as test.wave
			shutil.copyfile(self.audio_file, '../../tokens/temp/test/tf.wav')
			shutil.copyfile(self.audio_file, '../../tokens/temp/train/tf2.wav')
			#CALL SUBPROCESS TO RUN ./dump.sh
			with cd('../../'):
				subprocess.call(['./dump.sh',''])
				#OPEN FILE IN /data/test/*.npy
				files = [file for file in os.listdir('./data/temp/test/')]
				#PREDICT DATA
				data = np.load('./data/temp/test/' + files[0])
				banks = data.reshape(1, 98, 40, 1)
				z = self.model.predict(banks)
				p = z[0].tolist().index(max(z[0]))
				self.recognized_keyword = self.categories[p]
				print(self.recognized_keyword)
				K.clear_session()			

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

if __name__ == '__main__':
	sr = StreamReader()
	sr.main()
