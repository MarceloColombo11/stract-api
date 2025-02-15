from main import app
from utils.utils import *

api_token = app.config['API_TOKEN']
base_url = app.config['BASE_URL']
headers = {"Authorization": f"Bearer {api_token}"}

@app.route("/geral", methods=["GET"])
def get_geral():
    platforms = get_platforms()
    response = get_all_platform_insights(platforms)
    return response

@app.route("/geral/resumo")
def get_global_summary():
    response = get_geral_summary()
    return response