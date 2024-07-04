from flask import Blueprint, render_template, request
import requests
import markdown
import subprocess
import os

smartContract_blueprint = Blueprint('smartContract', __name__, template_folder='templates')

def smartcontract_scan(address):
    # The command returned by slither is 'stderr', not 'stdout'
    command = f"slither {address} --print human-summary"

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    
    # Split the output into lines
    output_lines = result.stderr.split('\n')
    output_lines = output_lines[4 - 1:11]
    
    return output_lines

def preprocess_markdown(text):
    new_text = text.replace('Summary', '## Summary')
    processed_text = new_text.replace('- [ ] ', '- ')
    return processed_text

def smartcontract_report(address):
    # Running command
    command = f"slither {address} --checklist --show-ignored-findings"
    # process = subprocess.Popen(command, stdout=subprocess.PIPE)
    # output, _ = process.communicate()
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    # Preprocessing Markdown text
    processed_output = preprocess_markdown(text=process.stdout)

    # Rendering Markdown text into HTML
    html_output = markdown.markdown(processed_output)

    # Writing HTML to a File
    output_directory = "static/reports"
    output_filename = f"{address}_report.html"
    output_path = os.path.join(output_directory, output_filename)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    html_file_link = f"/{output_path}"   # File path

    # Return file path
    return html_file_link


@smartContract_blueprint.route('/smartcontract')
def smartContract():
    return render_template('smartContract/smartcontract.html')

@smartContract_blueprint.route('/smartcontract/scan', methods=['POST'])
def query():
    # get the address from the form
    address = request.form['scan'].lower()

    data = requests.get(f"https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses={address}")
    address_data = data.json()

    # Extract the required keys
    required_keys = [
        "is_honeypot", "is_blacklisted", "is_open_source", "is_proxy",
        "transfer_pausable", "trading_cooldown"
    ]

    filtered_result = {key: address_data["result"][address][key] for key in required_keys}

    for key,value in filtered_result.items():
        if key == 'is_open_source':
            if value == '1':
                filtered_result[key] = "Safe"
            else:
                filtered_result[key] = "Risk"

    address_result = {key: "Risk" if value == '1' else "Safe" for key, value in filtered_result.items()}

    if all(value == 'Safe' for value in address_result.values()):
        address_result["safety"] = "Safe"
        address_result["data_source"] = "GoPlus Security"
    else:
        address_result["safety"] = "Risk"
        address_result["data_source"] = "GoPlus Security"

    scan_result = smartcontract_scan(address)
    scan_report = smartcontract_report(address)



    return render_template('smartContract/smartcontract.html', smartcontract=address_result, scan_result=scan_result, scan_report=scan_report)

