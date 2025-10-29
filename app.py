from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Demo songs database
SONGS_DATABASE = [
    {'id': '1', 'title': 'Blinding Lights', 'artist': 'The Weeknd', 'thumbnail': 'https://via.placeholder.com/200?text=Blinding+Lights', 'duration': 200, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'},
    {'id': '2', 'title': 'Shape of You', 'artist': 'Ed Sheeran', 'thumbnail': 'https://via.placeholder.com/200?text=Shape+of+You', 'duration': 234, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'},
    {'id': '3', 'title': 'Levitating', 'artist': 'Dua Lipa', 'thumbnail': 'https://via.placeholder.com/200?text=Levitating', 'duration': 203, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'},
    {'id': '4', 'title': 'One Dance', 'artist': 'Drake ft. Wizkid', 'thumbnail': 'https://via.placeholder.com/200?text=One+Dance', 'duration': 287, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'},
    {'id': '5', 'title': 'Anti-Hero', 'artist': 'Taylor Swift', 'thumbnail': 'https://via.placeholder.com/200?text=Anti-Hero', 'duration': 229, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'},
    {'id': '6', 'title': 'Titanium', 'artist': 'David Guetta ft. Sia', 'thumbnail': 'https://via.placeholder.com/200?text=Titanium', 'duration': 244, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3'},
    {'id': '7', 'title': 'Animals', 'artist': 'Martin Garrix', 'thumbnail': 'https://via.placeholder.com/200?text=Animals', 'duration': 246, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'},
    {'id': '8', 'title': 'Wake Me Up', 'artist': 'Avicii', 'thumbnail': 'https://via.placeholder.com/200?text=Wake+Me+Up', 'duration': 255, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'},
    {'id': '9', 'title': 'Bohemian Rhapsody', 'artist': 'Queen', 'thumbnail': 'https://via.placeholder.com/200?text=Bohemian+Rhapsody', 'duration': 354, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'},
    {'id': '10', 'title': 'Smells Like Teen Spirit', 'artist': 'Nirvana', 'thumbnail': 'https://via.placeholder.com/200?text=Teen+Spirit', 'duration': 301, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'},
    {'id': '11', 'title': 'Watermelon Sugar', 'artist': 'Harry Styles', 'thumbnail': 'https://via.placeholder.com/200?text=Watermelon+Sugar', 'duration': 174, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'},
    {'id': '12', 'title': 'Sunset Lover', 'artist': 'Petit Biscuit', 'thumbnail': 'https://via.placeholder.com/200?text=Sunset+Lover', 'duration': 215, 'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3'},
]

playlists = {}
favorites = []
history = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower().strip()
    if not query:
        return jsonify({'songs': SONGS_DATABASE[:10]})
    results = [song for song in SONGS_DATABASE if query in song['title'].lower() or query in song['artist'].lower()]
    if not results:
        results = SONGS_DATABASE
    return jsonify({'songs': results})

@app.route('/api/songs')
def api_get_all_songs():
    return jsonify({'songs': SONGS_DATABASE, 'total': len(SONGS_DATABASE)})

@app.route('/api/song/<song_id>')
def api_get_song(song_id):
    for song in SONGS_DATABASE:
        if song['id'] == song_id:
            return jsonify({'song': song})
    return jsonify({'error': 'Song not found'}), 404

@app.route('/api/trending')
def api_trending():
    return jsonify({'songs': SONGS_DATABASE[::2][:5]})

@app.route('/api/featured')
def api_featured():
    return jsonify({'songs': SONGS_DATABASE[:6]})

@app.route('/api/playlist/create', methods=['POST'])
def api_create_playlist():
    data = request.get_json()
    name = data.get('name', 'My Playlist')
    playlist_id = len(playlists) + 1
    playlists[str(playlist_id)] = {'id': str(playlist_id), 'name': name, 'songs': []}
    return jsonify({'success': True, 'playlist': playlists[str(playlist_id)]})

@app.route('/api/playlists')
def api_get_playlists():
    return jsonify({'playlists': list(playlists.values())})

@app.route('/api/playlist/<playlist_id>/add', methods=['POST'])
def api_add_to_playlist(playlist_id):
    data = request.get_json()
    song = data.get('song')
    if str(playlist_id) not in playlists:
        return jsonify({'error': 'Playlist not found'}), 404
    playlists[str(playlist_id)]['songs'].append(song)
    return jsonify({'success': True})

@app.route('/api/favorites/add', methods=['POST'])
def api_add_favorite():
    data = request.get_json()
    song = data.get('song')
    if song not in favorites:
        favorites.append(song)
    return jsonify({'success': True, 'total_favorites': len(favorites)})

@app.route('/api/favorites')
def api_get_favorites():
    return jsonify({'songs': favorites, 'total': len(favorites)})

@app.route('/api/history/add', methods=['POST'])
def api_add_to_history():
    data = request.get_json()
    song = data.get('song')
    history.append(song)
    if len(history) > 100:
        history.pop(0)
    return jsonify({'success': True})

@app.route('/api/history')
def api_get_history():
    return jsonify({'history': history[-20:]})

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'online',
        'app': 'Sanchit Music',
        'version': '3.0',
        'made_by': 'SANCHIT KUMAR',
        'songs_available': len(SONGS_DATABASE)
    })

if __name__ == '__main__':
    print('=' * 60)
    print('🎵 SANCHIT MUSIC - FULLY INTEGRATED')
    print('=' * 60)
    print(f'✅ Server Running')
    print(f'🎶 Total Songs: {len(SONGS_DATABASE)}')
    print(f'📡 URL: http://zeus.hidencloud.com:24579')
    print(f'👤 Made by: SANCHIT KUMAR')
    print('=' * 60)
    app.run(host='0.0.0.0', port=24579, debug=False, threaded=True)
