from pydub import AudioSegment	
import argparse, argcomplete, re

FLAGS = None

def normalize(sig=None):
	"""Change the audio level of a specified file"""
	if sig:
		sound = AudioSegment(sig, sample_width=2, frame_rate=16000, channels=1)
	else:
		sound = AudioSegment.from_file(FLAGS.i)
	max_dB = sound.max_dBFS
	#Normalize sound
	normalized_sound = sound.apply_gain(float(-sound.max_dBFS))
	# Remove DC Offset
	normalized_sound.remove_dc_offset()
	# Export to wav file
	if sig:
		f = normalized_sound.export('tmp.wav2', format="wav")
		return f
	else:
		f = normalized_sound.export(re.split('\\.', re.split('/', str(FLAGS.i))[-1])[0] + ".wav2", format="wav")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		help="Input file.")
	parser.add_argument(
		"-d",
		type=str,
		default=1,
		help="The audio level in dB")

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	normalize()
