# Non-buffered Ostensibly Instant Dedicated Everything Archive
import jinja2
import json
from flask import Flask
from os import walk
from os.path import splitext


movie_dir = r".\static\movies"
poster_dir = r".\static\movies\posters"

app = Flask(__name__)
env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(r".\templates"),
	autoescape=jinja2.select_autoescape(['html', 'xml'])
)


### PAGES ###
@app.route("/")
def page():
	template = env.get_template('index.html')
	
	itemlist = get_all_movies()
	return template.render(items=itemlist)

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
		name = splitext(file)[0]
		poster = poster_dir + "\\" + name + ".bmp"
		item = Movie(name, poster, file)
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


### OTHER SHIT ###
class Movie:
	name = ''
	poster = ''
	file = ''
	
	def __init__(self, name, poster, file):
		self.name = name
		self.poster = poster
		self.file = file











