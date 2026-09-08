"""
run.py — Start the BIT Attendance System on LAN
Usage:  python run.py
Access: http://<your-ip>:5000
"""
from app import app
from config import Config

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"+----------------------------------------------------+")
    print(f"|  Bangalore Institute of Technology                 |")
    print(f"|  Monthly Attendance Tracking System                |")
    print(f"+----------------------------------------------------+")
    print(f"|  Local:   http://localhost:{Config.PORT}                   |")
    print(f"|  Network: http://{local_ip}:{Config.PORT}              |")
    print(f"+----------------------------------------------------+")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
