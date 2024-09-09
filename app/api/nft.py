import ipfshttpclient
import json
from flask import jsonify, request
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from flask_jwt_extended import jwt_required
from . import api
def mint_token(metadata_url):

    file = open('nftMinter.json')
    data = json.load(file)
    abi = data["abi"]

    from manage import app

    rinkeby_chain_id = 4
    private_key = app.config['PRIVATE_KEY']
    provider_url = app.config['PROVIDER_URL']
    wallet_address = app.config['WALLET_ADDRESS']

    w3 = Web3(Web3.HTTPProvider(provider_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    nonce = w3.eth.getTransactionCount(wallet_address)
    contract_address = app.config['NFT_CONTRACT_ADDRESS']
    Nft_Minter = w3.eth.contract(address=contract_address, abi=abi)

    create_nft = Nft_Minter.functions.mintNFT(metadata_url).buildTransaction(
        {
            "chainId": rinkeby_chain_id,
            "from": wallet_address,
            "nonce": nonce
        })


    sign_create_nft = w3.eth.account.sign_transaction(
        create_nft,
        private_key=private_key)


    trx_hash = w3.eth.send_raw_transaction(sign_create_nft.rawTransaction)
    trx_recipt = w3.eth.wait_for_transaction_receipt(trx_hash)
    token_id = Nft_Minter.functions.getItemId().call()

    opensea_url = f"https://testnets.opensea.io/assets/rinkeby/{contract_address}/{token_id - 1}"
    return opensea_url

@api.route("/nft/mint", methods=["POST"])
@jwt_required()
def nft_minter():
    if request.method == "POST":
        title = request.form.get('title')
        uid = request.form.get('uid')
        description = request.form.get('description')
        nft_file = request.files['file']

        from manage import app
        client = ipfshttpclient.connect(app.config['IPFS_CONNECT_URL'])
        file_info = client.add(nft_file)
        nft_file_url = app.config['IPFS_FILE_URL'] + file_info['Hash']

        NFT_info = {
            "name": title,
            "description": description,
            "image": nft_file_url,
            "attributes": [{}],
            'uid': uid
        }

        with open('nft_json.json', 'w') as nft_json:
            json.dump(NFT_info, nft_json, indent=7)

        print(nft_json)
        nft_json_info = client.add('nft_json.json')
        metadata_url = app.config['IPFS_FILE_URL'] + nft_json_info['Hash']
        print(metadata_url, nft_json_info['Hash'])
        os.remove('nft_json.json')

        opensea_url = mint_token(metadata_url)
        return jsonify(metadata_url = opensea_url, status=0)



