import os
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "YouTube Transcript API (with Proxy) is running!"

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({"error": "Please provide a video_id"}), 400

    try:
        # 1. Get secrets from Render Environment
        proxy_user = os.environ.get('hvwvozst')
        proxy_pass = os.environ.get('7c7y0oq184rx')

        # 2. Configure Proxy (if credentials exist)
        if proxy_user and proxy_pass:
            proxy_config = WebshareProxyConfig(proxy_user, proxy_pass)
            yt = YouTubeTranscriptApi(proxy_config=proxy_config)
        else:
            # Fallback to no proxy (will likely fail on Render)
            yt = YouTubeTranscriptApi()
        
        # 3. Fetch Transcript
        transcript_obj = yt.fetch(video_id)
        transcript_list = transcript_obj.to_raw_data()
        
        # 4. Combine text
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        return jsonify({
            "video_id": video_id,
            "transcript": full_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)