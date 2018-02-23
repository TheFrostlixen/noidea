# Non-buffered Ostensibly Instant Dedicated Everything Archive
import jinja2
import json
from flask import Flask
from os import walk
from os.path import splitext, basename


movie_dir = r".\static\movies"
poster_dir = r".\static\movies\posters"

app = Flask(__name__)
env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(r".\templates"),
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
	# get parameter -> media
	# execute the media passed to the page
	return 0

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
	for (a, b, filenames) in walk(dirname):
		files.extend(filenames)
		break
	return filenames

def get_dirs(dirname):
	dirs  = []
	for (a, dirnames, c) in walk(dirname):
		dirs.extend(dirnames)
		break
	return dirs


### CLASSES ###
class Movie:
	def __init__(self, name, poster, file):
		self.name = name
		self.poster = poster
		self.file = file
		
	def __init__(self, file):
		self.file = file
		self.name = splitext(basename(file))[0]
		self.find_poster(self.name)
		
	def find_poster(self, search):
		self.poster = poster_dir + "\\" + search + ".bmp"





















