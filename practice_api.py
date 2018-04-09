import requests
import json

#this function will be intergrated into my application since I will have a tab where users can search for movie data (movie title, movie overview) using TheMovieDB API
def find_movie(query):
	params = {}
	result = requests.get('https://api.themoviedb.org/3/search/movie?api_key=01f21469bee1f9c1dae9b24273441f0c&language=en-US&query='+query+'&page=1&include_adult=false', params = params)

	json_result = json.loads(result.text)
	print(json_result['results'][0]['title'])
	print(json_result['results'][0]['overview'])



if __name__ == '__main__':
	# a user searches for the movie "Mean Girls" and the function returns the title and overview of movie from TheMovieDB API
	#sample input would include Mean Girls and Rocky
	find_movie("Mean Girls")
	find_movie("Rocky")
