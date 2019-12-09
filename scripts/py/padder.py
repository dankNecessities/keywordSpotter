import argparse, argcomplete, pydub, numpy
import os.path
from pydub.generators import WhiteNoise
from pydub import AudioSegment

FLAGS = None

def pad_tokens(sig=None):
	""" Pad token with leading and trailing whitespace to fit a given length"""
	if sig:
		sound = AudioSegment.from_file(sig)
	else:
		sound = AudioSegment.from_file(FLAGS.i)

	samples = numpy.array(sound.get_array_of_samples())
	file_export_name = None

	# Do we have enough samples for our given time?
	if sig:
		desired_length = sound.frame_rate * int(1000/1000)
	else:
		desired_length = sound.frame_rate * int(FLAGS.l/1000)
	if len(samples) <= desired_length:
		# Segment of white noise to be appended
		wn = numpy.array(WhiteNoise(sound.frame_rate).to_audio_segment((1000), -60).get_array_of_samples())
		#wn = numpy.zeros(sound.frame_rate)

		# Samples padded to beginning
		left_samples = int(numpy.ceil(abs(len(samples) - desired_length)/2))
		pad_left = wn[0:left_samples]

		# Samples padded to end
		right_samples = int(numpy.floor(abs(len(samples) - desired_length)/2))
		pad_right = wn[0:right_samples]
		
		# Concatenate arrays of samples
		padded_sound = numpy.concatenate([pad_left, samples, pad_right])

		#Convert back to AudioSegment then export
		audio_segment = AudioSegment(
				padded_sound.tobytes(),
				frame_rate=sound.frame_rate,
				sample_width=sound.sample_width,
				channels=1,
				)
		if sig is None:
			file_export_name = "pad_" + os.path.basename(FLAGS.i)
	else:
	# Trim edges for sounds longer than our desired length
		excess = len(samples) - desired_length
		trim_left = int(numpy.ceil(abs(len(samples) - desired_length)/2))
		trim_right = int(numpy.floor(abs(len(samples) - desired_length)/2))
		trimmed_sound = samples[trim_left:-trim_right]

		#Convert back to AudioSegment then export
		audio_segment = AudioSegment(
				trimmed_sound.tobytes(),
				frame_rate=sound.frame_rate,
				sample_width=sound.sample_width,
				channels=1,
				)
		if sig is None:
			file_export_name = "trim_" + os.path.basename(FLAGS.i)

	# Export completed file
	if sig:
		file_handle = audio_segment.export("tmp.wav2", format="wav")
	else:
		file_handle = audio_segment.export(file_export_name, format="wav")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		help="Input file")
	parser.add_argument(
		"-l",
		type=int,
		help="Length desired for token")

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	pad_tokens()
