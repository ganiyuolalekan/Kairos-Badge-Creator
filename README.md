# Kairos 2025 Badge Generator

A web application that generates personalized conference badges for Kairos 2025 attendees.

## Features

- ✨ Beautiful landing page with gold-themed animations
- 📝 Simple registration form
- 🖼️ Automatic badge generation with user's photo and name
- 💾 Download personalized badge
- 📱 Fully responsive design

## Setup Instructions

### 1. Initial Setup

```bash
# Make setup script executable
chmod +x setup.sh run.sh

# Run setup
./setup.sh
```

### 2. Add Template Image

**IMPORTANT**: You need to add the original conference badge template image:

1. Create a folder: `templates_img/`
2. Add your template image as: `templates_img/kairos_template.png`
   - This should be the original badge image with "OLALEKAN GANIYU"
   - The application will automatically detect and use this template

### 3. Run the Application

```bash
# Start the application
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python app.py
```

### 4. Access the Application

Open your browser and go to: `http://localhost:5001`

### 5. Test the Application

```bash
# Run tests
python test_app.py
```

## Image Processing Notes

The application will:
1. Place the user's photo in the circular area (automatically detected)
2. Replace "OLALEKAN GANIYU" with the user's name
3. Maintain all other design elements from the original template

**Current Settings** (adjust in `app.py` if needed):
- Circle center: (409, 714)
- Circle radius: 115px
- Name position: (409, 1020)
- Font size: 72px

## File Structure

```
generate_image_template/
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── index.html       # Landing page
│   ├── form.html        # Registration form
│   └── download.html    # Download page
├── templates_img/       # Image templates (create this)
│   └── kairos_template.png  # Add your template here
├── uploads/             # User uploaded images (auto-created)
├── generated/           # Generated badges (auto-created)
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── run.sh              # Run script
├── test_app.py         # Test script
├── test_local.py       # Local test script
└── README.md           # This file
```

## Free Deployment Options

### Option 1: Render.com (Recommended)

1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Note: `gunicorn` is already included in requirements.txt

### Option 2: Railway.app

1. Sign up at [railway.app](https://railway.app)
2. Connect GitHub repo
3. Deploy with one click
4. Railway auto-detects Flask apps

### Option 3: PythonAnywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Set up Flask app in Web tab
4. Configure static files

### Option 4: Replit

1. Create account at [replit.com](https://replit.com)
2. Import from GitHub
3. Run the application
4. Get a free URL

### Option 5: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
3. Run: `vercel`

## Production Considerations

For production deployment:

1. **Environment Variables**: Use `.env` file for configuration
2. **File Storage**: Consider using cloud storage (AWS S3, Cloudinary) for images
3. **Database**: Store user data if needed (PostgreSQL, MongoDB)
4. **Security**: Add rate limiting and input validation
5. **SSL**: Ensure HTTPS is enabled

## Troubleshooting

### Template Image Not Found
- Ensure `templates_img/kairos_template.png` exists
- The app will create a placeholder if template is missing

### Font Issues
- The app tries to use system fonts
- Falls back to default if fonts aren't available
- For production, include custom fonts

### Image Processing Issues
- Ensure uploaded images are in supported formats (PNG, JPG, JPEG)
- Maximum file size: 16MB

## Support

For issues or questions, please check:
1. Console output for error messages
2. Generated files in `generated/` folder
3. Upload files in `uploads/` folder

## License

This project is for the Kairos 2025 Conference - RCCG Praise Assembly, The Issachar Generation.
