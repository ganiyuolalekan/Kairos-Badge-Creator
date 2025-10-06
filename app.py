from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import base64
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
app.config['TEMPLATE_FOLDER'] = 'templates_img'

# Create necessary directories
for folder in [app.config['UPLOAD_FOLDER'], 
               app.config['GENERATED_FOLDER'], 
               app.config['TEMPLATE_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        # Get form data
        first_name = request.form.get('first_name', '').upper()
        last_name = request.form.get('last_name', '').upper()
        
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            unique_id = str(uuid.uuid4())[:8]
            filename = secure_filename(f"{unique_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image
            result_path = process_image(filepath, first_name, last_name, unique_id)
            
            # Convert to base64 for preview
            with open(result_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode()
            
            return jsonify({
                'success': True,
                'image_url': f'/download/{os.path.basename(result_path)}',
                'preview': f'data:image/png;base64,{img_base64}',
                'filename': os.path.basename(result_path)
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_image(user_image_path, first_name, last_name, unique_id):
    """Process the user image and overlay it on the template"""
    
    # Load template image
    template_path = os.path.join(app.config['TEMPLATE_FOLDER'], 'kairos_template.png')
    
    # Check if template exists, if not create a placeholder
    if not os.path.exists(template_path):
        create_placeholder_template(template_path)
    
    # Open images
    template = Image.open(template_path)
    user_image = Image.open(user_image_path)
    
    # Create a copy of template to work on
    result = template.copy()
    
    # Process user image for circular crop
    # Define the circular area position and size (adjust these based on your template)
    circle_center = (562, 925)  # Center of the circle in the template
    circle_radius = 288  # Radius of the circle
    
    # Resize user image to fit the circle
    user_image = user_image.resize((circle_radius * 2, circle_radius * 2), Image.Resampling.LANCZOS)
    
    # Create circular mask
    mask = Image.new('L', (circle_radius * 2, circle_radius * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, circle_radius * 2, circle_radius * 2), fill=255)
    
    # Apply circular mask
    user_image_circular = Image.new('RGBA', (circle_radius * 2, circle_radius * 2), (0, 0, 0, 0))
    user_image_circular.paste(user_image, (0, 0))
    user_image_circular.putalpha(mask)
    
    # Paste the circular user image onto the template
    result.paste(user_image_circular, 
                (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                user_image_circular)
    
    # Add text (name) to the image
    draw = ImageDraw.Draw(result)
    
    # Try to load a nice font, fallback to default if not available
    try:
        # You may need to adjust the font path based on your system
        font_size = 100  # Scaled for 1080x1920 template
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    # Text position (adjust based on your template)
    text = f"{first_name}\n{last_name}"
    text_position = (562, 1300)  # Centered below the circle
    
    # Get text bbox for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = text_position[0] - text_width // 2
    text_y = text_position[1]
    
    # Draw text with golden color
    draw.text((text_x, text_y), text, fill=(212, 175, 55), font=font, align="center")
    
    # Save the result
    output_filename = f"kairos_{unique_id}_{first_name}_{last_name}.png"
    output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
    result.save(output_path, 'PNG', quality=95)
    
    return output_path

def create_placeholder_template(template_path):
    """Create a placeholder template if the actual template is not available"""
    # Create a placeholder image with similar design (1080x1920 to match new template)
    img = Image.new('RGB', (1080, 1920), color='black')
    draw = ImageDraw.Draw(img)
    
    # Add golden borders/design elements
    draw.rectangle([0, 0, 1080, 260], fill=(212, 175, 55, 128))
    draw.rectangle([0, 1660, 1080, 1920], fill=(212, 175, 55, 128))
    
    # Add placeholder circle for image
    circle_center = (562, 697)
    circle_radius = 144
    draw.ellipse([circle_center[0] - circle_radius - 5, circle_center[1] - circle_radius - 5,
                  circle_center[0] + circle_radius + 5, circle_center[1] + circle_radius + 5],
                 fill=None, outline=(212, 175, 55), width=5)
    
    # Add title text
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw title
    draw.text((540, 330), "kairos", fill=(212, 175, 55), font=title_font, anchor="mm")
    draw.text((540, 460), "IGC 2025", fill=(255, 255, 255), font=subtitle_font, anchor="mm")
    
    # Draw bottom text
    draw.text((540, 1780), "I WILL BE THERE", fill=(212, 175, 55), font=subtitle_font, anchor="mm")
    
    img.save(template_path)

@app.route('/download/<filename>')
def download_page(filename):
    return render_template('download.html', filename=filename)

@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        path = os.path.join(app.config['GENERATED_FOLDER'], filename)
        return send_file(path, as_attachment=True, download_name=filename)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
