from server import Server
from app import app

def main():
    server = Server(app)
    server.run()

if __name__ == '__main__':
    main()