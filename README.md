# Spotify2Tidal

This project is a Flask application that integrates with Spotify and Tidal APIs to transfer all playlists from Spotify to Tidal.

## Features

- Spotify authentication and data retrieval
- Tidal authentication
- Import (by way of creating) Spotify playlists to Tidal

## Requirements

- Python 3.x
- Flask
- Spotipy
- TidalAPI

## Setup

### Command Line

1. Clone the repository:

   ```
   git clone https://github.com/MattGrdinic/spotify2tidal
   cd my-flask-app
   ```

2. Create a virtual environment:

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

### VS Code (Recommended)

1. Shift-Command(alt)-P

2. Python: Create Environment

3. Make sure requirements.txt is checked, otherwise manually run: `pip install -r requirements.txt`


4. Rename `config.py.tpl` to `config.py` in the `src` directory and add your sensitive configuration values:

   ```python
   SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
   SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
   SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'

   TIDAL_USERNAME = 'your_tidal_username'
   TIDAL_PASSWORD = 'your_tidal_password'
   ```

Spotify values come from: https://developer.spotify.com/

5. Make sure to add `src/config.py` to your `.gitignore` file to prevent it from being tracked by Git.

## Running the Application

### VS Code

1. Start project in debug or normal mode.
2. In terminal click the Tidal login link.
3. When done click the local app link in the terminal.

## License

This project is licensed under the MIT License.