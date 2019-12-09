import argparse, argcomplete
import numpy
from scipy.io import wavfile
from scipy.fftpack import dct
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

FLAGS = None
app = dash.Dash()

def convert_to_mel(sig=None):
	# Load the audio file
	if sig is not None:
		signal, sample_rate = sig, 16000
		# Get the number of frames that cover the entire signal, accounting for the overlap
		frame_length, frame_step = int(0.025 * sample_rate), int(0.01 * sample_rate)
	else:
		sample_rate, signal = wavfile.read(FLAGS.i)
		# Get the number of frames that cover the entire signal, accounting for the overlap
		frame_length, frame_step = int(FLAGS.f * sample_rate), int(FLAGS.d * sample_rate)
	
	signal_length = len(signal)
	print(signal_length)
	num_frames = int(numpy.floor(float(numpy.abs(signal_length - frame_length) / frame_step) + 1))

	# Pad signal to make sure that no frame has null data
	padding = int(((num_frames * frame_step) + frame_length) - signal_length)
	pad_signal = numpy.append(signal, numpy.zeros(padding))

	# Get list of indices to split signal into frames
	indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) # Indices for every frame
	indices += numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T

	# Finally split the signal
	signal_frames = signal[indices.astype(numpy.int32, copy=False)]

	# Apply hamming window to each frame
	signal_frames = signal_frames * numpy.hamming(frame_length)

	# We then get the frequency spectrum using FFT
	NFFT = 512
	magnitude_fft_frames = numpy.absolute(numpy.fft.rfft(signal_frames, NFFT))
	power_fft_frames = ((1.0 / NFFT) * ((magnitude_fft_frames) ** 2))

	# Apply triangular filters on mel scale to the power spectrum to extract frequency bands
	nfilt = 40															# 40 filters
	low_freq_mel = 0
	high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))
	mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2) # Equally spaced points in mel scale
	hz_points = (700 * (10**(mel_points / 2595) - 1)) 					# Convert Mel to Hz
	bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)				# Serialized to binary 

	fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
	for m in range(1, nfilt + 1):
		f_m_minus = int(bin[m - 1]) # Left
		f_m = int(bin[m]) 			# Center
		f_m_plus = int(bin[m + 1]) 	# Right

		for k in range(f_m_minus, f_m):
			fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
		for k in range(f_m, f_m_plus):
			fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
	filter_banks = numpy.dot(power_fft_frames, fbank.T)
	filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks) # Numerical stability
	filter_banks = 20 * numpy.log10(filter_banks) # dB

	# Mean normalization
	filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
	
	if sig is None:
		# Save to file
		if FLAGS.s:
			today = datetime.today()
			numpy.save(FLAGS.n + '_' + today.isoformat() + '.npy', filter_banks)
			print(FLAGS.n + '_' + today.isoformat() + '.npy')

		
		# Data Visualization
		if FLAGS.p:
			app.layout = html.Div(children=[html.H1(children='Filter Banks'), 
				dcc.Graph(
						id='filterbank',
						figure={
							'data': [
								{'z': filter_banks, 'type': 'heatmap', 'name':'fb'}
							],
							'layout': {
								'title': 'Mel filter banks'
							}
						}
					)])
			app.run_server(debug=True)
		
	return filter_banks

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		type=str,
		help="Input file")
	parser.add_argument(
		"-l",
		type=int,
		default=1000,
		help="Length of audio")
	parser.add_argument(
		"-f",
		type=int,
		default=0.025,
		help="Frame size")
	parser.add_argument(
		"-d",
		type=int,
		default=0.01,
		help="Stride Length")
	parser.add_argument(
		"-p",
		help="Plot graph",
		action="store_true")
	parser.add_argument(
		"-s",
		help="Save to file",
		action="store_true")
	parser.add_argument(
		"-n",
		type=str,
		help="Output file")

	argcomplete.autocomplete(parser)
	FLAGS, unparsed = parser.parse_known_args()
	convert_to_mel()
