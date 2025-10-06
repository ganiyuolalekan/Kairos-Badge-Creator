#!/bin/bash

echo "=== Kairos Badge Generator Startup ==="
echo "PORT: ${PORT:-8080}"
echo "FLASK_ENV: ${FLASK_ENV:-production}"
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo ""

# Check for required files
echo "Checking required files..."
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py not found!"
    exit 1
fi

if [ ! -f "templates_img/kairos_template.png" ]; then
    echo "WARNING: kairos_template.png not found! Will use placeholder."
fi

if [ ! -d "templates" ]; then
    echo "ERROR: templates directory not found!"
    exit 1
fi

# List key files for debugging
echo "Key files present:"
ls -la app.py 2>/dev/null || echo "  app.py: MISSING"
ls -la templates/ 2>/dev/null || echo "  templates/: MISSING"
ls -la templates_img/ 2>/dev/null || echo "  templates_img/: MISSING"
ls -la requirements.txt 2>/dev/null || echo "  requirements.txt: MISSING"

echo ""
echo "Starting Gunicorn server..."
echo "Command: gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app"
echo ""

# Start the application
exec gunicorn \
    --bind "0.0.0.0:${PORT:-8080}" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
