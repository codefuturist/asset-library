#!/bin/bash
# Setup script for Universal Asset Library

echo "🚀 Setting up Universal Asset Library..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/*.py

# Create initial catalog
echo "📊 Building initial catalog..."
python scripts/build-catalog.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To build the catalog:"
echo "  python scripts/build-catalog.py"
echo ""
echo "To validate assets:"
echo "  python scripts/validate-assets.py --path assets --recursive"
echo ""
echo "Happy asset managing! 🎉"
