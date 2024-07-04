from flask import Blueprint, request, render_template
import requests
from dotenv import load_dotenv, find_dotenv
import os
from pyecharts import options as opts
from pyecharts.charts import Graph

transaction_blueprint = Blueprint('transaction', __name__, template_folder='templates')

load_dotenv(find_dotenv())


# Extracting transaction data from history
def trasaction_histroy(address, data):
    processed_data = []
    for item in data['result']:
    
        hash_val = item['hash']
        from_val = item['from']
        to_val = item['to']
        # print(hash_val, from_val, to_val, address)

        # Skip the search key
        keys_to_skip = ["data_source", "contract_address"]

        # Checks if 'from' and 'to' are the same as the given 'address'
        if from_val == address:

            # If they are the same, check the safety of 'to'
            to_data = requests.get(f"https://api.gopluslabs.io/api/v1/address_security/{to_val}?chain_id=1")
            safety = to_data.json()

            # Check if all values ​​are 0
            all_zero = all(value == "0" for key, value in safety["result"].items() if key not in keys_to_skip)
            if all_zero:
                safety = "Safe"
            else:
                safety = "Risk"

            processed_data.append({'hash': hash_val, 'from': 'You', 'to': to_val, 'safety': safety})
        elif to_val == address:

            # If they are the same, check the safety of 'from'
            from_data = requests.get(f"https://api.gopluslabs.io/api/v1/address_security/{from_val}?chain_id=1")
            safety = from_data.json()

            # Check if all values ​​are 0
            all_zero = all(value == "0" for key, value in safety["result"].items() if key not in keys_to_skip)
            if all_zero:
                safety = "Safe"
            else:
                safety = "Risk"
            
            processed_data.append({'hash': hash_val, 'from': from_val, 'to': 'You', 'safety': safety})
    return processed_data

# Generate transaction flow graph
def transaction_flow(histroy_data):
    # Get the Ethereum address to query
    query_address = 'You'  # Set your query address here
    
    nodes = []
    links = []
    for transaction in histroy_data:
        sender = transaction['from']
        receiver = transaction['to']
        if sender not in nodes:
            nodes.append(sender)
        if receiver not in nodes:
            nodes.append(receiver)
        if sender == query_address:
            links.append({'source': sender, 'target': receiver})
        elif sender != query_address:
            links.append({'source': sender, 'target': receiver})
    # Set the node's name to the Ethereum address
    nodes = [{"name": node} for node in nodes]
    
    # Creat graph
    c = (
        Graph()
        .add(
            "",
            nodes,
            links,
            repulsion=8000,
            linestyle_opts=opts.LineStyleOpts(color="black"),
            label_opts=opts.LabelOpts(is_show=False),
            edge_symbol=["circle", "arrow"],
            edge_symbol_size=[10, 15],
            itemstyle_opts=opts.ItemStyleOpts(color="red"),
        )
    )
    
    # Render the template and pass the chart data to the front end
    return c.dump_options()



@transaction_blueprint.route('/transaction')
def transaction():
    return render_template('transaction/transaction.html')

@transaction_blueprint.route('/transaction/query', methods=['POST'])
def query():
    # get the address from the form
    address = request.form['query'].lower()

    #get the api key from the environment variable
    etherscan_api = os.getenv('etherscan_api')

    # make the request to the api
    response = requests.get(f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey={etherscan_api}")
    data = response.json()
    histroy_data = trasaction_histroy(address, data)
    graph = transaction_flow(histroy_data)



    return render_template('transaction/transaction.html', results=histroy_data, graph=graph)