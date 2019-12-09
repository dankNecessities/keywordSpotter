import argparse, argcomplete
import numpy as np
from keras.models import model_from_json
from keras import backend as K

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

def test():
	model = load_cnn(FLAGS.l, FLAGS.w)
	data = np.load(FLAGS.i)
	banks = data.reshape(1, 98, 40, 1)
	z = model.predict(banks)

	p = z[0].tolist().index(max(z[0]))
	recognized_keyword = categories[p]
	print(recognized_keyword)

	K.clear_session()

def load_cnn(name, weights):
	with open(name, 'r') as json_file:
		loaded_model_json = json_file.read()
	loaded_model = model_from_json(loaded_model_json)
	# Load weights into new model
	loaded_model.load_weights(weights)
	print("Loaded model from disk")
	return loaded_model

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		help="Input np data file")
	parser.add_argument(
		"-l",
		type=str,
		default="../model/final_cnn_model.json",
		help="Network Path")
	parser.add_argument(
		"-w",
		type=str,
		default="../model/weights_final_cnn.h5",
		help="Network Weights Path")

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	test()
