#!/bin/bash
# Setup script for Universal Asset Library

echo "🚀 Setting up Universal Asset Library..."

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✓ uv found: $(uv --version)"

# Check Python version
echo "🐍 Checking Python version..."
if ! uv python list | grep -q "3.12"; then
    echo "📥 Installing Python 3.12..."
    uv python install 3.12
fi

# Create virtual environment with Python 3.12
echo "📦 Creating virtual environment with Python 3.12..."
uv venv --python 3.12

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies using uv
echo "📚 Installing dependencies..."
uv pip install -e ".[dev]"

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
echo "  source .venv/bin/activate"
echo ""
echo "To build the catalog:"
echo "  python scripts/build-catalog.py"
echo ""
echo "To validate assets:"
echo "  python scripts/validate-assets.py --path assets --recursive"
echo ""
echo "Happy asset managing! 🎉"
