# Movie Mood Generator

A fun web application that recommends movies based on emojis and keywords! Simply choose an emoji that matches your mood and add some keywords to get personalized movie recommendations.

## Setup

1. First, install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Get a TMDB API Key:
   - Sign up at [TMDB](https://www.themoviedb.org/)
   - Go to your account settings
   - Get your API key
   - Create a `.env` file in the project root and add:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

3. Run the application:
```bash
python app.py
```

## How to Use

1. Open your browser and go to `http://localhost:5000`
2. Enter an emoji that matches your mood (e.g., 😊 for happy, 😢 for sad)
3. Add some keywords that interest you
4. Click "Get Movies" to see your recommendations!

## Supported Emojis

- 😊 - Comedy, Family movies
- 😢 - Drama, Romance
- 😱 - Horror, Thriller
- 🚀 - Science Fiction, Adventure
- 🦸 - Action, Superhero
- 🔍 - Mystery, Crime
- ❤️ - Romance
- 🎭 - Drama
- 🌟 - Fantasy, Adventure
- 🎬 - Documentary
