import config
from app import app
import routes

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)
