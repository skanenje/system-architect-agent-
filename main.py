"""
Tech Stack Learning Analyzer - Web UI

This project now uses a web interface instead of CLI.
Run this file to start the web server.
"""

import os
import sys

print("\n" + "=" * 70)
print("🚀 Tech Stack Learning Analyzer")
print("=" * 70)
print("\n📱 Starting Web UI...\n")

# Check if .env exists
if not os.path.exists('.env'):
    print("❌ Error: .env file not found!")
    print("\nPlease create a .env file with your API key:")
    print("  GEMINI_API_KEY=your_key_here")
    print("\nGet your free API key at:")
    print("  https://makersuite.google.com/app/apikey")
    print("\n" + "=" * 70 + "\n")
    sys.exit(1)

# Import and run the Flask app
from app import app

if __name__ == "__main__":
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
