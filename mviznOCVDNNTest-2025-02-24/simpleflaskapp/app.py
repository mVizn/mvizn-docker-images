from flask import Flask, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration: Set directories for uploads and incoming images
UPLOAD_FOLDER = '/dev/shm/dockerinput'
INCOMING_FOLDER = '/dev/shm/dockeroutput'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INCOMING_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if a file is an allowed image."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload an image to the UPLOAD_FOLDER."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload'))
    # Simple HTML upload form with a back link
    return '''
    <!doctype html>
    <html>
      <head>
        <title>Upload New Image</title>
      </head>
      <body>
        <h1>Upload New Image</h1>
        <form method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
        <br>
        <a href="/">Back to Home</a>
      </body>
    </html>
    '''

@app.route('/')
def index():
    """
    Poll the INCOMING_FOLDER for the latest image.
    If found, display the image; otherwise, show a message.
    The page auto-refreshes every 1 second.
    """
    image_file = None
    # List only allowed image files
    files = [f for f in os.listdir(INCOMING_FOLDER) if allowed_file(f)]
    if files:
        # Get the most recently modified file
        image_file = max(files, key=lambda f: os.path.getmtime(os.path.join(INCOMING_FOLDER, f)))
    
    return f'''
    <!doctype html>
    <html>
      <head>
        <title>Latest Image</title>
        <meta http-equiv="refresh" content="1">
      </head>
      <body>
        <h1>Latest Image from Incoming Folder</h1>
        {f'<img src="/incoming/{image_file}" alt="Latest Image" style="max-width:100%;">' if image_file else '<p>No images found.</p>'}
        <br><br>
        <a href="/upload"><button>Upload Image</button></a>
      </body>
    </html>
    '''

@app.route('/incoming/<filename>')
def incoming_file(filename):
    """Serve files from the INCOMING_FOLDER."""
    return send_from_directory(INCOMING_FOLDER, filename)

if __name__ == '__main__':
    # Ensure the app is accessible externally by binding to 0.0.0.0
    app.run(debug=True, host='0.0.0.0')

