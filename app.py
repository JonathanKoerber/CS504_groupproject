from api import create_app
from api.config import Config, DevelopmentConfig

app = create_app(DevelopmentConfig)
if __name__ == "__main__":
    app.run(debug=True)
