# webhooks

This app/webhook directory is where flask or fastapi apps should be placed.

## `idempotent_webhook.py`

Here’s how to set up a Flask application to handle MinIO webhooks without requiring the MinIO client or credentials directly within the application. The MinIO server will send webhook notifications to your Flask application, which will process events based on the bucket and object details provided in the webhook payload.

### 1. Configure MinIO Webhooks

First, configure your MinIO server to send event notifications to your Flask application.

#### Adding a Webhook Endpoint

1. **Set up the Webhook Endpoint**:

   ```bash
   mc alias set myminio http://localhost:9000 minio minio123
   mc admin config set myminio notify_webhook:1 endpoint="http://localhost:5000/webhooks/minio" queue_limit="1000" queue_dir="/tmp" --json
   mc admin service restart myminio
   ```

2. **Configure Bucket Notifications**:

   ```bash
   mc event add myminio/mybucket arn:minio:sqs::1:webhook --event put,get,delete
   ```

### 2. Create Flask Application

Create a Flask application to handle the webhook events sent by MinIO. 

#### Flask Setup

1. **Install Flask**:

   ```bash
   pip install Flask Flask-Cors
   ```
 
### Explanation

1. **Webhook Endpoint**: The `/webhooks/minio` endpoint receives webhook events from MinIO. Each event contains details such as the bucket name and the type of event (e.g., object created, deleted, accessed).

2. **Event Handlers**: The `handle_upload_event`, `handle_delete_event`, and `handle_access_event` functions process the events based on the event type and bucket name.

3. **Idempotency**: The event handlers ensure that each event is processed based on the bucket name and event type, maintaining idempotency.

### 3. Testing Your Setup

Start your Flask application:

```bash
python webhooks.py
```

Use tools like `curl` or Postman to test your webhook endpoint by simulating MinIO events. You can also perform operations (upload, delete, access files) on your MinIO buckets to see the webhook in action.

#### Example Test with `curl`:

```bash
curl -X POST http://localhost:5000/webhooks/minio -H "Content-Type: application/json" -d '{
  "Records": [
    {
      "eventName": "s3:ObjectCreated:Put",
      "s3": {
        "bucket": {
          "name": "mybucket"
        },
        "object": {
          "key": "myfile.txt"
        }
      }
    }
  ]
}'
```

This setup ensures that your Flask application can handle various events from multiple MinIO buckets without needing to embed MinIO credentials or client libraries directly within the application, thereby maintaining security and simplicity. For further details on MinIO webhook configuration, refer to the [MinIO documentation](https://min.io/docs/minio/linux/operations/monitoring/bucket-notifications.html).