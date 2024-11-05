from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Path to the images folder
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the images folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images)

@app.route('/slideshow', methods=['POST'])
def slideshow():
    selected_images = request.form.getlist('selectedImages')
    return render_template('slideshow.html', images=selected_images)

@app.route('/manage-images', methods=['GET', 'POST'])
def manage_images():
    if request.method == 'POST':
        # Upload images
        if 'image' not in request.files:
            flash('No image file selected!')
            return redirect(request.url)
        
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'Image {filename} uploaded successfully!')
        else:
            flash('Invalid file type. Only PNG and JPG files are allowed.')
    
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('manage_images.html', images=images)

@app.route('/delete-images', methods=['POST'])
def delete_images():
    selected_images = request.form.getlist('selectedImages')
    for image in selected_images:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image))
            flash(f'Image {image} deleted successfully!')
        except Exception as e:
            print(f"Error deleting file {image}: {e}")
            flash(f'Error deleting image: {image}')
    return redirect(url_for('manage_images'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg'}

if __name__ == '__main__':
    app.run(debug=True)
