#!/usr/bin/env python
"""
Startup script for HealthPredict AI Backend Server
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    reload = os.getenv("RELOAD", "True").lower() == "true"
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     HealthPredict AI Backend Server                          ║
    ║     Version: 3.0.0                                          ║
    ║     Host: {host}:{port}                                        ║
    ║     Debug Mode: {debug}                                         ║
    ║                                                              ║
    ║     API Documentation: http://{host}:{port}/docs               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )