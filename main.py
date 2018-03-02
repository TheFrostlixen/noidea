# Non-buffered Ostensibly Instant Dedicated Everything Archive
import cv2
import jinja2
import subprocess
from flask import Flask, request
from os import walk, system
from os.path import splitext, basename, isfile
from pathlib import Path


shows_dir  = r"./static/shows/"
movie_dir  = r"./static/movies/"
poster_dir = r"./static/posters/"

app = Flask(__name__)
env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(r"./templates"),
	autoescape=jinja2.select_autoescape(['html', 'xml'])
)


### PAGES ###
@app.route("/")
def index():
	movies, shows = build_index(movie_dir)
	
	template = env.get_template('index.html')
	return template.render(movies=movies, shows=shows)

@app.route("/show/")
def show():
	id = request.args.get('id', default='error', type=str)
	
	show_list = build_show_index(shows_dir, id)
	
	template = env.get_template('show.html')
	return template.render(show_name=id, show_list=show_list)

@app.route("/play", methods=['POST'])
def play():
	form_information = request.get_json(silent=True)
	media_name = form_information[0]['media_name']
	path = Path(media_name)
	subprocess.call(str(path.resolve()), shell=True)
	
	template = env.get_template('play.html')
	return template.render(media_name=media_name)


### FUNCTIONS ###
def build_index(target_dir):
	files = get_files( target_dir )
	movies = []
	for file in files:
		item = Movie(file)
		movies.append(item)
	
	shows = []
	dirs = get_dirs( shows_dir )
	for dir in dirs:
		item = Show(dir)
		shows.append(item)
	
	return movies, shows

def build_show_index(target_dir, show_id):
	files = get_files( target_dir+show_id+'/' )
	episodes = []
	for file in files:
		item = Episode(file, show_id)
		episodes.append(item)
	
	return episodes

def get_files(dirname):
	files = []
	for (base_dir, b, filenames) in walk( dirname ):
		files.extend(filenames)
		break
	return [base_dir + b for b in files]

def get_dirs(dirname):
	dirs  = []
	for (base_dir, dirnames, c) in walk( dirname ):
		dirs.extend(dirnames)
		break
	return [base_dir + a for a in dirs]


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
		thumb_width = 120
		thumb_height = 160
		
		vcap = cv2.VideoCapture(filename)
		res, im_ar = vcap.read()
		while im_ar.mean() < threshold and res:
			  res, im_ar = vcap.read()
		im_ar = cv2.resize(im_ar, (thumb_width, thumb_height), 0, 0, cv2.INTER_LINEAR)
		cv2.imwrite(poster_name, im_ar)
		
	def find_poster(self, filename, name):
		poster_name = poster_dir + name + ".png"
		if not isfile(poster_name):
			self.generate_poster(filename, poster_name)
		
		self.poster = poster_name

class Show:
	def __init__(self, name, poster, dir):
		self.name = name
		self.poster = poster
		self.dir = dir
		
	def __init__(self, dir):
		self.dir = dir
		self.name = basename(dir)
		self.find_poster(dir, self.name)
		
	def generate_poster(self, filename, poster_name):
		threshold = 10
		thumb_width = 120
		thumb_height = 160
		
		vcap = cv2.VideoCapture(filename)
		res, im_ar = vcap.read()
		while im_ar.mean() < threshold and res:
			  res, im_ar = vcap.read()
		im_ar = cv2.resize(im_ar, (thumb_width, thumb_height), 0, 0, cv2.INTER_LINEAR)
		cv2.imwrite(poster_name, im_ar)
		
	def find_poster(self, dirname, name):
		poster_name = poster_dir + name + ".png"
		
		if not isfile(poster_name):
			for (base_dir, b, filenames) in walk( dirname ):
				break
			base_file = base_dir + '/' + filenames[0]
			self.generate_poster(base_file, poster_name)
		
		self.poster = poster_name

class Episode:
	def __init__(self, name, poster, file):
		self.name = name
		self.poster = poster
		self.file = file
		
	def __init__(self, file, show_id):
		self.file = file
		self.name = splitext(basename(file))[0]
		self.find_poster(file, show_id)
		
	def find_poster(self, filename, show_id):
		poster_name = poster_dir + show_id + ".png"
		
		self.poster = poster_name









