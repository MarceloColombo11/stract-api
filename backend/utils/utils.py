"""
This module provides functions to fetch and process insights data from an external API.

The module includes functions to:
  - Retrieve available platforms.
  - Retrieve all fields and accounts for a given platform.
  - Fetch all insights for a platform (or multiple platforms).
  - Process (normalize and adjust) individual insights.
  - Aggregate insights per account for summary reports.

All API requests are performed using the configured API token and base URL.
"""

from main import app
import requests
from flask import jsonify

api_token = app.config['API_TOKEN']
base_url = app.config['BASE_URL']
headers = {"Authorization": f"Bearer {api_token}"}


def get_platforms():
    """
    Retrieve the list of platforms from the API.

    Returns:
        dict or tuple: A dictionary containing the platform data if successful,
                       or a tuple with an error message and HTTP status code if failed.
    """
    url = f"{base_url}/platforms"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch platforms"}, response.status_code


def get_all_fields(platform):
    """
    Retrieve all field values for a given platform.

    Args:
        platform (str): The platform identifier.

    Returns:
        list: A list of field values for the platform, or a JSON error response if the request fails.
    """
    url = f"{base_url}/fields?platform={platform}"
    all_fields = []
    page = 1
    while True:
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch fields"}), response.status_code
        data = response.json()
        all_fields.extend(field["value"] for field in data.get("fields", []))
        pagination = data.get("pagination", {})
        if page >= pagination.get("total", 1):
            break  
        page += 1  
    return all_fields


def get_all_accounts_per_platform(platform):
    """
    Retrieve all accounts for a given platform.

    Args:
        platform (str): The platform identifier.

    Returns:
        list: A list of account dictionaries for the platform, or a JSON error response if the request fails.
    """
    url = f"{base_url}/accounts?platform={platform}"
    all_accounts = []
    page = 1
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch accounts"}), response.status_code
        data = response.json()
        all_accounts.extend(data.get("accounts", []))
        pagination = data.get("pagination", {})
        if page >= pagination.get("total", 1):
            break
        page += 1
    return all_accounts


def get_all_platform_insights(platform):
    """
    Retrieve all insights for a given platform or list of platforms.

    If the platform parameter is a string, it is converted into a list of dictionaries.
    If it is a dictionary with a 'platforms' key, that list is used.

    Args:
        platform (str or dict): The platform identifier or a dictionary containing platforms.

    Returns:
        Response: A Flask JSON response containing a list of processed insights.
    """
    if isinstance(platform, str):
        platforms = [{"value": platform}]
    elif isinstance(platform, dict) and "platforms" in platform:
        platforms = platform["platforms"]
    else:
        return jsonify({"error": "Invalid platform input. Must be a string or an object with 'platforms'."}), 400

    insights_data = []

    for plt in platforms:
        platform_value = plt["value"]
        all_field = get_all_fields(platform_value)
        all_accounts = get_all_accounts_per_platform(platform_value)
        all_field_str = ",".join(all_field)

        for account in all_accounts:
            account_id = account["id"]
            account_name = account["name"]
            account_token = account["token"]

            url = (f"{base_url}/insights?platform={platform_value}"
                   f"&account={account_id}&token={account_token}&fields={all_field_str}")
            page = 1

            while True:
                response = requests.get(f"{url}&page={page}", headers=headers)
                if response.status_code != 200:
                    print(f"Warning: Failed to fetch insights for {account_name} on {platform_value}. Skipping...")
                    break
                
                data = response.json()
                insights = data.get("insights", [])
                for insight in insights:
                    # Process the insight to adjust and normalize its fields.
                    insight = process_insight(insight)
                    # Add account and platform information to the insight.
                    insight["platform"] = platform_value
                    insight["account_id"] = account_id
                    insight["account_name"] = account_name
                    insight["account_token"] = account_token
                insights_data.extend(insights)

                pagination = data.get("pagination", {})
                if page >= pagination.get("total", 1):
                    break
                page += 1

    return jsonify(insights_data)


def process_insight(insight):
    """
    Process and normalize an insight dictionary.

    This function applies adjustments and normalization rules:
      - If the platform is 'ga4', adjust cost_per_click using spend (or cost) and clicks.
      - Convert 'adName' to 'ad_name'.
      - Convert 'spend' to 'cost'.
      - Convert 'region' to 'country'.
      - Convert 'effective_status' to 'status'.
      - Convert 'cpc' to 'cost_per_click' (rounded to 3 decimal places) or calculate cost_per_click as cost/clicks if not provided.
      - If 'ctr' is not provided, calculate it as clicks/impressions (rounded to 3 decimal places).

    Args:
        insight (dict): The insight data to process.

    Returns:
        dict: The processed and normalized insight.
    """
    # Adjust cost_per_click for Google Analytics (ga4) if applicable.
    if insight.get("platform") == "ga4":
        clicks = insight.get("clicks", 0)
        spend = insight.get("spend") or insight.get("cost")
        if clicks and spend:
            insight["cost_per_click"] = spend / clicks
        else:
            insight["cost_per_click"] = None
    if "adName" in insight:
        insight["ad_name"] = insight.pop("adName")

    if "spend" in insight:
        insight["cost"] = insight.pop("spend")

    if "region" in insight:
        insight["country"] = insight.pop("region")

    if "effective_status" in insight:
        insight["status"] = insight.pop("effective_status")

    if "cpc" in insight:
        try:
            insight["cost_per_click"] = round(float(insight.pop("cpc")), 3)
        except (ValueError, TypeError):
            insight["cost_per_click"] = None
    else:
        if "cost" in insight and "clicks" in insight and insight["clicks"]:
            try:
                insight["cost_per_click"] = round(insight["cost"] / insight["clicks"], 3)
            except Exception:
                insight["cost_per_click"] = None
        else:
            insight["cost_per_click"] = None
    if "ctr" not in insight:
        if "clicks" in insight and "impressions" in insight and insight["impressions"]:
            try:
                insight["ctr"] = round(insight["clicks"] / insight["impressions"], 3)
            except Exception:
                insight["ctr"] = None
        else:
            insight["ctr"] = None

    return insight


def get_platform_account_summary(platform):
    """
    Aggregates insights for the given platform by collapsing all rows belonging
    to the same account into a single row.
    
    For each account:
      - Numeric fields are summed.
      - Textual fields (except for account_name) are set to an empty string.
      
    Args:
        platform (str or dict): The platform identifier (e.g., "ga4") or a dictionary
                                with a "platforms" key containing a list of platforms.
                                
    Returns:
        Response: A Flask JSON response containing a list of aggregated account summaries.
    """

    if isinstance(platform, str):
        platforms = [{"value": platform}]
    elif isinstance(platform, dict) and "platforms" in platform:
        platforms = platform["platforms"]
    else:
        return jsonify({"error": "Invalid platform input. Must be a string or an object with 'platforms'."}), 400

    aggregated_data = {}


    for plt in platforms:
        platform_value = plt["value"]
        response = get_all_platform_insights(platform_value)
        insights_data = response.get_json()

        for insight in insights_data:

            insight = process_insight(insight)

            account_id = insight["account_id"]
            account_name = insight["account_name"]
            account_token = insight["account_token"]
            account_platform = insight["platform"]

            if account_id not in aggregated_data:
                aggregated_data[account_id] = {
                    "account_id": account_id,
                    "account_name": account_name,
                    "account_token": account_token,
                    "platform": account_platform
                }

            for key, value in insight.items():
                if key in ["account_id", "account_name", "account_token", "platform", "id"]:
                    continue
                if isinstance(value, (int, float)):
                    current_sum = aggregated_data[account_id].get(key, 0) + value
                    if isinstance(current_sum, float) or isinstance(value, float):
                        aggregated_data[account_id][key] = round(current_sum, 3)
                    else:
                        aggregated_data[account_id][key] = current_sum
                else:
                    aggregated_data[account_id][key] = ""

    return jsonify(list(aggregated_data.values()))


def get_geral_summary():
    """
    Aggregates insights from all platforms by collapsing all rows belonging
    to the same platform into a single row.

    For each platform:
      - Numeric fields are summed and, if a float, rounded to 3 decimal places.
      - Textual fields (except for the platform name) are set to an empty string.

    Returns:
        Response: A Flask JSON response containing a list of aggregated summaries per platform.
    """

    platforms_response = get_platforms()
    if isinstance(platforms_response, tuple):
        return platforms_response

    platforms_list = platforms_response.get("platforms", [])
    aggregated_data = {}

    for platform_obj in platforms_list:
        platform_value = platform_obj["value"]
        response = get_all_platform_insights(platform_value)
        insights_data = response.get_json()

        for insight in insights_data:
            insight = process_insight(insight)
            current_platform = insight.get("platform", platform_value)

            if current_platform not in aggregated_data:
                aggregated_data[current_platform] = {
                    "platform": current_platform
                }

            for key, value in insight.items():
                if key in ["account_id", "account_name", "account_token", "platform", "id"]:
                    continue
                if isinstance(value, (int, float)):
                    current_sum = aggregated_data[current_platform].get(key, 0) + value
                    if isinstance(current_sum, float) or isinstance(value, float):
                        aggregated_data[current_platform][key] = round(current_sum, 3)
                    else:
                        aggregated_data[current_platform][key] = current_sum
                else:
                    aggregated_data[current_platform][key] = ""

    return jsonify(list(aggregated_data.values()))