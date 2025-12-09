from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "YouTube Transcript API is running!"

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({"error": "Please provide a video_id"}), 400

    try:
        # --- NEW 2025 API SYNTAX ---
        # 1. Instantiate the API Class
        yt = YouTubeTranscriptApi()
        
        # 2. Fetch the transcript (Returns an object, not a list)
        transcript_obj = yt.fetch(video_id)
        
        # 3. Convert it to the raw list of text
        transcript_list = transcript_obj.to_raw_data()
        # ---------------------------
        
        # Combine the text parts
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        return jsonify({
            "video_id": video_id,
            "transcript": full_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)