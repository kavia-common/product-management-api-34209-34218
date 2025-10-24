import os
from app import app

if __name__ == "__main__":
    # Bind to 0.0.0.0 for preview, default port 3001 unless PORT env provided
    port = int(os.getenv("PORT", "3001"))
    app.run(host="0.0.0.0", port=port)
