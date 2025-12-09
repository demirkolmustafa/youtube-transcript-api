
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify\
from youtube_transcript_api import YouTubeTranscriptApi\
\
app = Flask(__name__)\
\
@app.route('/', methods=['GET'])\
def home():\
    return "YouTube Transcript API is running!"\
\
@app.route('/transcript', methods=['GET'])\
def get_transcript():\
    video_id = request.args.get('video_id')\
    \
    if not video_id:\
        return jsonify(\{"error": "Please provide a video_id (e.g., ?video_id=dQw4w9WgXcQ)"\}), 400\
\
    try:\
        # Fetch the transcript\
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)\
        \
        # Combine the text parts into one big string (optional, easier for AI to read)\
        full_text = " ".join([entry['text'] for entry in transcript_list])\
        \
        return jsonify(\{\
            "video_id": video_id,\
            "transcript": full_text, \
            "raw_data": transcript_list\
        \})\
    except Exception as e:\
        return jsonify(\{"error": str(e)\}), 500\
\
if __name__ == '__main__':\
    app.run(host='0.0.0.0', port=10000)}
