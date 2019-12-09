import sys, re, subprocess
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QCheckBox, QLineEdit, QFileDialog, QWidget, QMessageBox, QApplication, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from queue import Queue

class StreamerThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    stream_data_path = None

    def __init__(self, callback, parent=None):
        QThread.__init__(self)
        #self.queue = queue
        self.signal.connect(callback)

    # run method gets called when we start the thread
    def run(self):
    	if (self.stream_data_path != None):
    		print("Audio: " + self.stream_data_path)
    	sr = StreamReader()
    	sr.main(self.stream_data_path)
    	self.predictedOutput = sr.recognized_keyword
    	print("DETECTED: " + self.predictedOutput)
    	res = [self.predictedOutput, sr.categories, sr.commands]
    	self.signal.emit(res)

    # get stream data if required
    def get_data(self, stream_data_path=None):
    	self.stream_data_path = stream_data_path


class Recognizer(QWidget):

	categories = None
	commands = None
	command = None
	gif = None

	def __init__(self):
		super().__init__()
		self.initUI()
		self.stream_thread = StreamerThread(self.handle_result)

	def initUI(self):

		self.setStyleSheet("background-color: white")

		#Layout Manager and Items
		self.chooseFile = QCheckBox("Audio File")
		self.chooseFile.setChecked(True)
		self.chooseFile.clicked.connect(self.audioSelected)
		#chooseFile.setAlignment(Qt.AlignCenter)
		filecheckbox = QHBoxLayout()
		filecheckbox.addWidget(self.chooseFile)
		filecheckbox.setAlignment(Qt.AlignCenter)

		self.fileLabel = QLineEdit("")
		openBtn = QPushButton("Open", self)
		openBtn.clicked.connect(self.openFileDialog)
		openBtn.resize(openBtn.sizeHint())
		filebox = QHBoxLayout()
		filebox.addWidget(self.fileLabel)
		filebox.addWidget(openBtn)
		filebox.setAlignment(Qt.AlignCenter)
		filebox.setContentsMargins(90, 0, 90, 0)

		self.chooseMic = QCheckBox("Microphone")
		self.chooseMic.clicked.connect(self.micSelected)
		miccheckbox = QHBoxLayout()
		miccheckbox.addWidget(self.chooseMic)
		miccheckbox.setAlignment(Qt.AlignCenter)

		startBtn = QPushButton("Start", self)
		startBtn.clicked.connect(self.hal)
		startBtn.resize(startBtn.sizeHint())
		hbox = QHBoxLayout()
		hbox.addWidget(startBtn)
		hbox.setAlignment(Qt.AlignCenter)

		self.commandBtn = QPushButton("Execute Command", self)
		self.commandBtn.clicked.connect(self.runCmd)
		self.commandBtn.setEnabled(False)
		self.commandBtn.resize(self.commandBtn.sizeHint())
		hbox4 = QHBoxLayout()
		hbox4.addWidget(self.commandBtn)
		hbox4.setAlignment(Qt.AlignCenter)

		closeBtn = QPushButton("Close", self)
		closeBtn.clicked.connect(QApplication.instance().quit)
		closeBtn.resize(closeBtn.sizeHint())
		hbox5 = QHBoxLayout()
		hbox5.addWidget(closeBtn)
		hbox5.setAlignment(Qt.AlignCenter)

		self.gif = QLabel("Loading GIF here.")
		self.gif.setPixmap(QPixmap("../../gui/stop.png"))
		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.gif)
		hbox2.setAlignment(Qt.AlignCenter)

		self.resultLabel = QLabel("Click Start to begin detection...")
		hbox3 = QHBoxLayout()
		hbox3.setAlignment(Qt.AlignCenter)
		hbox3.addWidget(self.resultLabel)

		vbox = QVBoxLayout()
		vbox.addLayout(filecheckbox)
		vbox.addLayout(filebox)
		vbox.addLayout(miccheckbox)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addLayout(hbox)
		vbox.addLayout(hbox4)
		vbox.addLayout(hbox5)

		self.setLayout(vbox)

		self.resize(600, 500)
		self.center()
		self.setWindowTitle('Word Recognizer')
		self.show()

	def openFileDialog(self):
		self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Audio Files (*.wav)')
		if self.fname[0]:
			with open(self.fname[0], 'rb') as f:
				#self.data = f.read()
				self.fileLabel.setText(re.split('/', self.fname[0])[-1])

	def hal(self):
		print("STARTING DETECTION..")
		
		try:
			if (self.chooseFile.isChecked() == True):
				self.stream_thread.get_data(self.fname[0])
			self.loading_animation = QMovie('../../gui/loading_animation.gif')
			self.gif.setMovie(self.loading_animation)
			self.gif.setGeometry(QRect(50,50,50,50))
			self.loading_animation.start()
			self.stream_thread.start()

		except AttributeError as e:
				reply = QMessageBox.question(self, 'Warning!', "Please select a file.", QMessageBox.Yes)

		'''sr = StreamReader()
		sr.main()
		self.predictedOutput = sr.recognized_keyword
		print("DETECTED: " + self.predictedOutput)
		self.command = sr.command

		loading_animation.stop()'''

		return 0

	def handle_result(self, result):
		self.categories = result[1]
		self.commands = result[2]
		self.gif.setPixmap(QPixmap("../../gui/stop.png"))
		self.resultLabel.setText('Detected Word: ' + result[0])
		self.command = self.commands[self.categories.index(result[0])]
		self.commandBtn.setEnabled(True)

	def micSelected(self):
		print('MICROPHONE BABY!')
		self.chooseFile.setChecked(False)

	def audioSelected(self):
		print("AUDIO FILE SELECTED")
		self.chooseMic.setChecked(False)

	def runCmd(self):
		print('EXECUTING COMMAND')
		cmd = re.split(',', self.command)
		subprocess.call(cmd)
		return 0

	def center(self):
		windowFrame = self.frameGeometry()
		windowCenter = QDesktopWidget().availableGeometry().center()
		windowFrame.moveCenter(windowCenter)
		self.move(windowFrame.topLeft())

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Confirm', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	rec = Recognizer()
	from stream_reader import StreamReader
	sys.exit(app.exec_())
	