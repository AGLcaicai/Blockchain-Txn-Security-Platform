from flask import Blueprint, request, render_template
import requests
import re



address_blueprint = Blueprint('address', __name__, template_folder='templates')



@address_blueprint.route('/address')
def address():
    return render_template('address/address.html')

@address_blueprint.route('/address/check', methods=['POST'])
def query():
    # get the address from the form
    address = request.form['check'].lower()

    # Regular expression for Ethereum address
    ethereum_address_pattern = r'^0x[a-fA-F0-9]{40}$'
    # Regular expression for website links
    website_link_pattern = r'^(https?|http):\/\/(www\.)?[^\s/$.?#].[^\s]*$'

    address_result = []
    website_result = []

    if re.match(ethereum_address_pattern, address):

        data = requests.get(f"https://api.gopluslabs.io/api/v1/address_security/{address}?chain_id=1")
        address_data = data.json()

        # Extract the required keys
        required_keys = [
            "cybercrime", "money_laundering", "financial_crime", "darkweb_transactions",
            "phishing_activities", "fake_kyc", "stealing_attack", "blackmail_activities",
            "malicious_mining_activities"
        ]

        # Create a dictionary to hold the required key-value pairs
        filtered_result = {key: address_data["result"][key] for key in required_keys}

        # Create a dictionary to hold the required key-value pairs
        address_result = {key: "Risk" if value == '1' else "Safe" for key, value in filtered_result.items()}

        # Check if all are 'Safe'
        if all(value == 'Safe' for value in address_result.values()):
            address_result["safety"] = "Safe"
            address_result["data_source"] = "GoPlus Security"
        else:
            address_result["safety"] = "Risk"
            address_result["data_source"] = address_data["result"]["data_source"]

    elif re.match(website_link_pattern, address):

        data = requests.get(f"https://api.gopluslabs.io/api/v1/phishing_site?url={address}")
        address_data = data.json()

        filtered_result = address_data["result"]["phishing_site"]

        phishing_site_status = "Risk" if filtered_result == 1 else "Safe"
        website_result = {"phishing_site": phishing_site_status}
        website_result["data_source"] = "GoPlus Security"

        
    return render_template('address/address.html', address=address_result, website=website_result)
