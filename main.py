# Non-buffered Ostensibly Instant Dedicated Everything Archive
import base64
import cv2
import jinja2
import json
from flask import Flask, request
from os import walk, system
from os.path import splitext, basename, isfile, abspath


movie_dir = r"./static/movies/"
poster_dir = r"./static/movies/posters/"

app = Flask(__name__)
env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(r"./templates"),
	autoescape=jinja2.select_autoescape(['html', 'xml'])
)


### PAGES ###
@app.route("/")
def index():
	template = env.get_template('index.html')
	
	itemlist = get_all_movies()
	return template.render(items=itemlist)

@app.route("/play/")
def play():
	template = env.get_template('play.html')
	media_name = request.args.get('media', default='error', type=str)
	#system('start "' + media_name + '"')
	return template.render(media_name=media_name)

@app.route("/shows/")
def json_test():
	shows = ['House MD', 'Bojack Horseman']
	return env.get_template('index.html').render(
		shows=map(json.dumps, shows)
	)


### FUNCTIONS ###
def get_all_movies():
	files = get_files( movie_dir )
	movie_list = []
	for file in files:
		item = Movie(file)
		movie_list.append(item)
	return movie_list

def get_files(dirname):
	files = []
	for (base_dir, b, filenames) in walk( dirname ):
		files.extend(filenames)
		break
	return [base_dir + c for c in files]

def get_dirs(dirname):
	dirs  = []
	for (base_dir, dirnames, c) in walk( dirname ):
		dirs.extend(dirnames)
		break
	return [base_dir + c for c in dirs]


### CLASSES ###
class Movie:
	def __init__(self, name, poster, file):
		self.name = name
		self.poster = poster
		self.file = file
		
	def __init__(self, file):
		self.file = file
		self.name = splitext(basename(file))[0]
		self.find_poster(file, self.name)
		
	def generate_poster(self, filename, poster_name):
		threshold = 10
		thumb_width = 240
		thumb_height = 320
		
		vcap = cv2.VideoCapture(filename)
		res, im_ar = vcap.read()
		while im_ar.mean() < 10 and res:
			  res, im_ar = vcap.read()
		im_ar = cv2.resize(im_ar, (240, 320), 0, 0, cv2.INTER_LINEAR)
		cv2.imwrite(poster_name, im_ar)
		print('created poster ' + poster_name)

	def find_poster(self, filename, name):
		poster_name = poster_dir + name + ".png"
		if not isfile(poster_name):
			self.generate_poster(filename, poster_name)
		
		self.poster = poster_name









