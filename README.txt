# IMDB REST API

## - Method: GET
> Eg:
> *http://localhost:8000/api/imdb?name=psycho*
> *http://localhost:8000/api/imdb?imdb_score=9.1*


## - Method: POST
> Url: *http://localhost:8000/api/imdb*
> Body: Json format
	> Eg: {
	    "99popularity": 87.1,
	    "director": "Some Random Director",
	    "genre": "Thriller",
	    "imdb_score": 8.7,
	    "name": "Some Random Movie"
	}


## - Method: DELETE
> Eg: *http://localhost:8000/api/imdb?name_director=random*
