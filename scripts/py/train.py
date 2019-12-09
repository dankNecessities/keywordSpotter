import argparse, argcomplete
import os, re
import numpy
from keras.models import model_from_json
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical

FLAGS = None
path = os.path.abspath('.')

""" Train the model on successive inputs stored in the same folder"""

def train():
	model = load_cnn(FLAGS.n, FLAGS.w)
	
	words_list = os.listdir(FLAGS.i)
	words_list.sort()
	# Control
	#words_list.append("Empty")
	x_input, y_input = [], []
	x_input_test, y_input_test = [], []
	for label in words_list:
		data_dir = os.path.join(FLAGS.i, label)
		try:
			train_feed_in = os.listdir(data_dir + '/train')
			test_feed_in = os.listdir(data_dir + '/test')
			for np_file in train_feed_in:
				x_input.append(numpy.load(data_dir + '/train/' + np_file))
				y_input.append(numpy.array([words_list.index(label)+1]))
			for np_file in test_feed_in:
				x_input_test.append(numpy.load(data_dir + '/test/' + np_file))
				y_input_test.append(numpy.array([words_list.index(label)+1]))
		except FileNotFoundError as e:
		 	pass
	
	x_input = numpy.array(x_input)
	y_input = numpy.array(y_input)
	x_input_test = numpy.array(x_input_test)
	y_input_test = numpy.array(y_input_test)

	# Reshape data to fit model
	X_input = x_input.reshape(len(x_input), 98, 40, 1)
	X_input_test = x_input_test.reshape(len(x_input_test), 98, 40, 1)
	print(X_input_test.shape)

	# Change labels to binary
	Y_input = to_categorical(y_input)
	Y_input_test = to_categorical(y_input_test)
	print(Y_input.shape)

	model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
	early_stopping_monitor = EarlyStopping(patience=10)
	#model.fit(X_input, Y_input, epochs=30, callbacks=[early_stopping_monitor])
	model.fit(X_input, Y_input, validation_data=(X_input_test, Y_input_test), epochs=60, callbacks=[early_stopping_monitor])
	save_cnn(model)

def load_cnn(name, weights):
	with open(name, 'r') as json_file:
		loaded_model_json = json_file.read()
	loaded_model = model_from_json(loaded_model_json)
	# Load weights into new model
	loaded_model.load_weights(FLAGS.w)
	print("loaded_model from disk")
	return loaded_model

def save_cnn(model):
	model_json = model.to_json()
	with open(FLAGS.n, 'w') as json_file:
		json_file.write(model_json)
	# Serialize weights to h5
	model.save_weights(FLAGS.w)
	print("Saved model to disk")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		help="Path to input files")
	parser.add_argument(
		"-n",
		type=str,
		help="Path to neural network")
	parser.add_argument(
		"-w",
		type=str,
		help="Path to weights")
	parser.add_argument(
		"-p",
		action='store_true',
		help="Predict new data")

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	train()
