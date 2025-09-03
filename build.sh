#!/bin/bash

# TECS Desktop Build Script
# This script automates the build process for the TECS Desktop application

set -e

echo "🚀 TECS Desktop Build Script"
echo "=============================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    echo "   Please upgrade Node.js and try again."
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo "✅ npm $(npm -v) detected"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Check if cf directory exists
if [ ! -d "cf" ]; then
    echo "❌ CF framework directory not found. Please ensure the 'cf' directory exists."
    echo "   This should contain your Python TECS implementation."
    exit 1
fi

echo "✅ CF framework directory found"

# Check if requirements file exists
if [ ! -f "requirements_minimal.txt" ]; then
    echo "❌ requirements_minimal.txt not found. Please ensure this file exists."
    exit 1
fi

echo "✅ Requirements file found"

# Build the application
echo ""
echo "🔨 Building TECS Desktop application..."

# Detect platform and build accordingly
PLATFORM=$(uname -s)
case "$PLATFORM" in
    Linux*)
        echo "🐧 Building for Linux..."
        npm run build:linux
        ;;
    Darwin*)
        echo "🍎 Building for macOS..."
        npm run build:mac
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "🪟 Building for Windows..."
        npm run build:win
        ;;
    *)
        echo "❓ Unknown platform: $PLATFORM"
        echo "   Building for current platform..."
        npm run build
        ;;
esac

echo ""
echo "🎉 Build completed successfully!"
echo ""
echo "📁 Distribution files are in the 'dist/' directory:"
ls -la dist/

echo ""
echo "🚀 To run the application:"
echo "   - Windows: Run the .exe installer"
echo "   - macOS: Mount the .dmg and drag to Applications"
echo "   - Linux: Make the .AppImage executable and run it"
echo ""
echo "💡 For development, run: npm start"
echo "💡 For testing, run: npm run dev"