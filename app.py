from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Emoji to genre/mood mapping with TMDB genre IDs
EMOJI_MAPPING = {
    "😊": {"genres": [35, 10751], "mood": "happy"},  # Comedy, Family
    "😢": {"genres": [18, 10749], "mood": "sad"},    # Drama, Romance
    "😱": {"genres": [27, 53], "mood": "scared"},    # Horror, Thriller
    "🚀": {"genres": [878, 12], "mood": "adventurous"},  # Sci-Fi, Adventure
    "🦸": {"genres": [28, 14], "mood": "heroic"},    # Action, Fantasy
    "🔍": {"genres": [9648, 80], "mood": "mysterious"},  # Mystery, Crime
    "❤️": {"genres": [10749], "mood": "romantic"},   # Romance
    "🎭": {"genres": [18], "mood": "dramatic"},      # Drama
    "🌟": {"genres": [14, 12], "mood": "magical"},   # Fantasy, Adventure
    "🎬": {"genres": [99], "mood": "informative"}    # Documentary
}

def search_movies(query):
    api_key = os.getenv('TMDB_API_KEY')
    base_url = "https://api.themoviedb.org/3"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    try:
        # Search for movies using the query
        search_url = f"{base_url}/search/movie"
        params = {
            'query': query,
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }
        
        print(f"Searching movies with query: {query}")
        response = requests.get(search_url, headers=headers, params=params)
        print(f"Search response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            print(f"Search error: {response.text}")
            return []
    except Exception as e:
        print(f"Error in search_movies: {e}")
        return []

def get_movie_recommendations(emoji, keywords):
    api_key = os.getenv('TMDB_API_KEY')
    base_url = "https://api.themoviedb.org/3"
    
    print(f"Processing request - Emoji: {emoji}, Keywords: {keywords}")
    
    # Get genre IDs for the emoji
    emoji_data = EMOJI_MAPPING.get(emoji, {"genres": [], "mood": "neutral"})
    genre_ids = emoji_data["genres"]
    
    # Search for movies using keywords
    search_results = []
    if keywords:
        search_results = search_movies(keywords)
        print(f"Found {len(search_results)} movies from keyword search")
    
    # If no keyword results, search by genre
    if not search_results and genre_ids:
        genres_str = ",".join(map(str, genre_ids))
        headers = {
            "Authorization": f"Bearer {api_key}",
            "accept": "application/json"
        }
        
        try:
            discover_url = f"{base_url}/discover/movie"
            params = {
                'with_genres': genres_str,
                'language': 'en-US',
                'sort_by': 'popularity.desc',
                'include_adult': False,
                'page': 1
            }
            
            print(f"Discovering movies with genres: {genres_str}")
            response = requests.get(discover_url, headers=headers, params=params)
            print(f"Discover response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('results', [])
                print(f"Found {len(search_results)} movies from genre search")
            else:
                print(f"Discover error: {response.text}")
        except Exception as e:
            print(f"Error in genre search: {e}")
    
    # Filter results by genre if we have both keywords and genres
    if keywords and genre_ids and search_results:
        search_results = [
            movie for movie in search_results 
            if any(genre_id in movie.get('genre_ids', []) for genre_id in genre_ids)
        ]
        print(f"After genre filtering: {len(search_results)} movies")
    
    # Get top 5 movies
    movies = search_results[:5]
    
    # Enhance movie data with additional details
    enhanced_movies = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    for movie in movies:
        try:
            movie_response = requests.get(
                f"{base_url}/movie/{movie['id']}",
                headers=headers
            )
            
            if movie_response.status_code == 200:
                movie_details = movie_response.json()
                enhanced_movies.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'vote_average': movie['vote_average'],
                    'release_date': movie.get('release_date', ''),
                    'genres': [genre['name'] for genre in movie_details.get('genres', [])],
                    'runtime': movie_details.get('runtime', 0)
                })
            else:
                print(f"Error fetching movie details: {movie_response.text}")
        except Exception as e:
            print(f"Error processing movie {movie.get('title')}: {e}")
    
    print(f"Returning {len(enhanced_movies)} enhanced movies")
    return enhanced_movies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    emoji = data.get('emoji', '')
    keywords = data.get('keywords', '')
    
    movies = get_movie_recommendations(emoji, keywords)
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
