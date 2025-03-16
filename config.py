import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    APP_NAME = "fieldsecure"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "cfde43524c5d23f331f032e2ad4a47dc"
