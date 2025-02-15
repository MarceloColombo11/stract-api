from main import app
from utils.utils import *

api_token = app.config['API_TOKEN']
base_url = app.config['BASE_URL']
headers = {"Authorization": f"Bearer {api_token}"}


@app.route("/<platform>", methods=["GET"])
def get_platform_insights(platform):

    response = get_all_platform_insights(platform)    
    return response


@app.route("/<platform>/resumo", methods=["GET"])
def get_platform_summary(platform):
    response = get_platform_account_summary(platform)
    
    return response


