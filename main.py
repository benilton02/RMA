from dotenv import load_dotenv, find_dotenv
import uvicorn
from src.main.configs import app

load_dotenv(find_dotenv('.env'))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
