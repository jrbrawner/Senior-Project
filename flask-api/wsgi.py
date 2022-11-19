"""Application entry point."""
from api import create_app

#dev for development
#production for deployment with docker
app = create_app('dev')

if __name__ == "__main__":
    app.run(host="0.0.0.0")