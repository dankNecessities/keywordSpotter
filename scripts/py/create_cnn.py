import argparse, argcomplete, os
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, BatchNormalization
from keras.optimizers import SGD

FLAGS = None
sgd = SGD(lr=0.001, momentum=0.0, decay=0.0, nesterov=False)

# Create network by adding layer by layer - model used here is a convolutional neural network
def create_cnn(outputs):
	model = Sequential()
	model.add(Conv2D(FLAGS.f, kernel_size=tuple(FLAGS.k), strides=FLAGS.s, activation='relu', input_shape=tuple(FLAGS.i)))
	model.add(MaxPooling2D(pool_size=(1, 3)))
	model.add(Conv2D(78, kernel_size=(5, 4), strides=1, activation='relu', padding="same"))
	model.add(MaxPooling2D(pool_size=(1, 1)))
	model.add(Flatten())
	model.add(BatchNormalization())
	model.add(Dense(32, activation='relu'))
	model.add(Dense(128, activation='relu'))
	model.add(Dense(outputs, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
	print(model.summary())
	save_cnn(model)
	'''
	model = Sequential()
	model.add(Conv2D(FLAGS.f, kernel_size=FLAGS.k, strides=FLAGS.s, activation='relu', input_shape=FLAGS.i))
	#model.add(MaxPooling2D(pool_size=(1, 3)))
	model.add(Conv2D(64, kernel_size=(5, 4), strides=1, activation='relu', padding="same"))
	#model.add(MaxPooling2D(pool_size=(1, 1)))
	model.add(MaxPooling2D(pool_size=(3, 3)))
	model.add(Flatten())
	model.add(BatchNormalization())
	#model.add(Dense(32, activation='relu'))
	model.add(Dense(128, activation='relu'))
	model.add(BatchNormalization())
	model.add(Dense(outputs, activation='softmax'))
	model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
	print(model.summary())
	save_cnn(model)
	'''

# Save the network weights to h5 files
def save_cnn(model):
	model_json = model.to_json()
	with open("../model/" + FLAGS.n + "_model.json", 'w') as json_file:
		json_file.write(model_json)
	# Serialize weights to h5
	model.save_weights("../model/weights_" + FLAGS.n + ".h5")
	print("Saved model to disk")

def count_outputs():
	count = len([i for i in os.listdir('../../data').__iter__()]) + 1
	return count

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-n",
		type=str,
		default="",
		help="Model name")
	parser.add_argument(
		"-f",
		type=int,
		default=126,
		help="Feature depth")
	parser.add_argument(
		"-k",
		nargs="+",
		type=int,
		default=(16, 8),
		help="Shape of kernel")
	parser.add_argument(
		"-s",
		type=int,
		default=8,
		help="Number of strides")
	parser.add_argument(
		"-i",
		nargs="+",
		type=int,
		default=(98, 40, 1),
		help="Shape of input")
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-n",
		type=str,
		help="Model name")
	parser.add_argument(
		"-f",
		type=int,
		default=32,
		help="Feature depth")
	parser.add_argument(
		"-k",
		type=tuple,
		default=(4, 4),
		help="Shape of kernel")
	parser.add_argument(
		"-s",
		type=int,
		default=1,
		help="Number of strides")
	parser.add_argument(
		"-i",
		type=tuple,
		default=(98, 40, 1),
		help="Shape of input")'''

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	create_cnn(count_outputs())
