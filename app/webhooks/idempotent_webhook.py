from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webhooks/minio', methods=['POST'])
def minio_webhook():
    data = request.json
    records = data.get('Records', [])
    for record in records:
        bucket_name = record['s3']['bucket']['name']
        event_type = record['eventName']
        if event_type.startswith('s3:ObjectCreated:'):
            handle_upload_event(bucket_name, record)
        elif event_type.startswith('s3:ObjectRemoved:'):
            handle_delete_event(bucket_name, record)
        elif event_type.startswith('s3:ObjectAccessed:'):
            handle_access_event(bucket_name, record)
        else:
            return jsonify({"status": "error", "message": "Event not handled"}), 400
    return jsonify({"status": "success", "message": "Webhook processed"}), 200

def handle_upload_event(bucket_name, record):
    print(f"File uploaded in bucket {bucket_name}:", record)
    # Process upload event here
    return

def handle_delete_event(bucket_name, record):
    print(f"File deleted in bucket {bucket_name}:", record)
    # Process delete event here
    return

def handle_access_event(bucket_name, record):
    print(f"File accessed in bucket {bucket_name}:", record)
    # Process access event here
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)