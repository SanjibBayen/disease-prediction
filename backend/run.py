#!/usr/bin/env python
"""
Startup script for HealthPredict AI Backend Server

This script initializes and starts the FastAPI backend server with
proper configuration from environment variables and command-line arguments.
"""

import uvicorn
import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# CONFIGURATION
# ============================================================================

# Add parent directory to path for imports if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loaded environment from {env_path}")
else:
    print(f"⚠ No .env file found at {env_path}, using defaults")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Configure logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        # Ensure log directory exists
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )


# ============================================================================
# SERVER CONFIGURATION CLASS
# ============================================================================

class ServerConfig:
    """Server configuration management"""
    
    def __init__(self):
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8000))
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        self.reload = os.getenv("RELOAD", "True").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "info")
        self.workers = int(os.getenv("WORKERS", 1))
        self.log_file = os.getenv("LOG_FILE", "logs/server.log")
        self.ssl_key = os.getenv("SSL_KEY")
        self.ssl_cert = os.getenv("SSL_CERT")
        self.access_log = os.getenv("ACCESS_LOG", "True").lower() == "true"
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            'host': self.host,
            'port': self.port,
            'debug': self.debug,
            'reload': self.reload,
            'log_level': self.log_level,
            'workers': self.workers,
            'access_log': self.access_log
        }
    
    def validate(self) -> tuple:
        """
        Validate configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate port range
        if self.port < 1 or self.port > 65535:
            return False, f"Invalid port number: {self.port}. Must be between 1 and 65535"
        
        # Validate host
        if not self.host:
            return False, "Host cannot be empty"
        
        # Validate SSL if provided
        if self.ssl_key and not os.path.exists(self.ssl_key):
            return False, f"SSL key file not found: {self.ssl_key}"
        
        if self.ssl_cert and not os.path.exists(self.ssl_cert):
            return False, f"SSL certificate file not found: {self.ssl_cert}"
        
        return True, None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_requirements() -> bool:
    """
    Check if all required files and directories exist
    
    Returns:
        True if all requirements are met, False otherwise
    """
    required_dirs = ['logs', 'models', 'data']
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = Path(__file__).parent / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
            # Create directory if it doesn't exist
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {dir_name}")
    
    # Check if app module exists
    app_path = Path(__file__).parent / "app" / "main.py"
    if not app_path.exists():
        print(f"✗ Error: app/main.py not found at {app_path}")
        return False
    
    return True


def print_banner(config: ServerConfig):
    """
    Print beautiful startup banner
    
    Args:
        config: Server configuration
    """
    banner = f"""
    ╔════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                ║
    ║                         HealthPredict AI Backend Server                         ║
    ║                                    v3.0.0                                      ║
    ║                                                                                ║
    ║    ┌─────────────────────────────────────────────────────────────────────┐    ║
    ║    │                         Server Information                           │    ║
    ║    ├─────────────────────────────────────────────────────────────────────┤    ║
    ║    │  Host:          {config.host:<46} │    ║
    ║    │  Port:          {str(config.port):<46} │    ║
    ║    │  Debug Mode:    {str(config.debug):<46} │    ║
    ║    │  Auto Reload:   {str(config.reload):<46} │    ║
    ║    │  Log Level:     {config.log_level.upper():<46} │    ║
    ║    │  Workers:       {str(config.workers):<46} │    ║
    ║    └─────────────────────────────────────────────────────────────────────┘    ║
    ║                                                                                ║
    ║    📚 API Documentation:  http://{config.host}:{config.port}/docs                ║
    ║    📖 ReDoc:              http://{config.host}:{config.port}/redoc               ║
    ║    🔍 OpenAPI JSON:       http://{config.host}:{config.port}/openapi.json       ║
    ║                                                                                ║
    ║    🚀 Server is starting... Press CTRL+C to stop                               ║
    ║                                                                                ║
    ╚════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def parse_arguments():
    """
    Parse command-line arguments
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="HealthPredict AI Backend Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run.py                    # Start with default settings
    python run.py --port 8080        # Start on port 8080
    python run.py --host 127.0.0.1   # Start on localhost only
    python run.py --debug False      # Disable debug mode
    python run.py --workers 4        # Start with 4 workers
        """
    )
    
    parser.add_argument(
        "--host",
        type=str,
        help="Host to bind (default: from .env or 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind (default: from .env or 8000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=None,
        help="Enable debug mode"
    )
    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=None,
        help="Enable auto-reload"
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload"
    )
    parser.add_argument(
        "--workers",
        type=int,
        help="Number of worker processes"
    )
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level"
    )
    parser.add_argument(
        "--ssl-key",
        type=str,
        help="SSL key file path (for HTTPS)"
    )
    parser.add_argument(
        "--ssl-cert",
        type=str,
        help="SSL certificate file path (for HTTPS)"
    )
    
    return parser.parse_args()


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main entry point for the backend server"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = ServerConfig()
    
    # Override with command line arguments
    if args.host:
        config.host = args.host
    if args.port:
        config.port = args.port
    if args.debug:
        config.debug = True
    if args.no_debug:
        config.debug = False
    if args.reload:
        config.reload = True
    if args.no_reload:
        config.reload = False
    if args.workers:
        config.workers = args.workers
    if args.log_level:
        config.log_level = args.log_level
    if args.ssl_key:
        config.ssl_key = args.ssl_key
    if args.ssl_cert:
        config.ssl_cert = args.ssl_cert
    
    # Validate configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        print(f"✗ Configuration Error: {error_msg}")
        sys.exit(1)
    
    # Setup logging
    log_level = "DEBUG" if config.debug else config.log_level.upper()
    setup_logging(log_level=log_level, log_file=config.log_file)
    
    # Check requirements
    if not check_requirements():
        print("✗ Requirements check failed. Please ensure all required files exist.")
        sys.exit(1)
    
    # Print banner
    print_banner(config)
    
    # Prepare uvicorn configuration
    uvicorn_config = {
        "app": "app.main:app",
        "host": config.host,
        "port": config.port,
        "reload": config.reload,
        "log_level": config.log_level,
        "access_log": config.access_log,
    }
    
    # Add SSL configuration if provided
    if config.ssl_key and config.ssl_cert:
        uvicorn_config["ssl_keyfile"] = config.ssl_key
        uvicorn_config["ssl_certfile"] = config.ssl_cert
        print("🔒 HTTPS mode enabled")
    
    # Add workers for production (only if reload is disabled)
    if not config.reload and config.workers > 1:
        uvicorn_config["workers"] = config.workers
        print(f"⚡ Running with {config.workers} workers")
    
    # Run the server
    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Server failed to start: {str(e)}")
        sys.exit(1)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()