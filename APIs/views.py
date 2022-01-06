from Crypto import Cipher
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os, hashlib, warnings, requests, json
# Create your views here.

@api_view()
def community_list(request):
    communities = Community.objects.all()
    communities_serializer = communitySerializer(communities, many=True)
    return Response(communities_serializer.data)

@api_view()
def community_details(request, id):
    return Response(id)

@api_view()
def card_transfers(request): 

    def getKey(secret_key):
        hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12   

    def encryptData(key, plainText):

        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, hence the need for the conversion below
        test = plainText.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted        
    
    url_payment = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/charge"

    payload_payment = {
            'PBFPubKey': 'FLWPUBK_TEST-228496fddbbe401c9ca14f1bc43aa146-X',
            "cardno": "5438898014560229",
            "cvv": "890",
            "expirymonth": "09",
            "expiryyear": "22",
            "currency": "NGN",
            "country": "NG",
            'suggested_auth': 'pin',
            'pin': '3310',
            "amount": "10",
            'txRef': 'MC-TESTREF-1234',
            "email": "maestrojolly@gmail.com",
            "phonenumber": "0902620185",
            "firstname": "maestro",
            "lastname": "jolly",
            "IP": "355426087298442",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
    }
        
    
    headers_payment = {        
        "Content-Type": "application/json"
    }  

    sec_key = 'FLWSECK_TEST-46af6f348fb05865e587f046398efb21-X'

    # hash the secret key with the get hashed key function
    hashed_sec_key = getKey(sec_key)

    # encrypt the hashed secret key and payment parameters with the encrypt function
    encrypt_3DES_key = encryptData(hashed_sec_key, json.dumps(payload_payment))

    # payment payload
    payload = {
        "PBFPubKey": "FLWPUBK_TEST-228496fddbbe401c9ca14f1bc43aa146-X",
        "client": encrypt_3DES_key,
        "alg": "3DES-24"
    }

    response_payment = requests.request("POST", url_payment, data=json.dumps(payload), headers=headers_payment)
    
    return Response(response_payment)

    # if response.status_code == 200:
    #     url_transfer = "https://api.flutterwave.com/v3/transfers"

    #     payload_transfer = {
    #         "account_bank": "MPS",
    #         "account_number": "+250784019340",
    #         "amount": 3,
    #         "narration": "Someone sent you money",
    #         "currency": "USD",
    #         "reference": "akhlm-pstmnpyt-rfxx007_PMCKDU_1",
    #         "callback_url": "https://webhook.site/b3e505b0-fe02-430e-a538-22bbbce8ce0d",
    #         "debit_currency": "USD"
    #     }

    #     headers_transfer = {
    #         "Accept": "application/json",
    #         "Authorization": "Bearer FLWSECK_TEST-SANDBOXDEMOKEY-X",
    #         "Content-Type": "application/json"
    #     }

    #     response = requests.request("POST", url_transfer, json=payload_transfer, headers=headers_transfer)


@api_view(['POST', 'GET', 'DELETE'])
def exchange_rates(request):
    AMOUNT = 3
    url = 'https://v6.exchangerate-api.com/v6/bb45034e1deaa832192a7785/pair/USD/RWF/'+ str(AMOUNT)   

    response = requests.get(url)
    data = response.json()
    return Response(data)

@api_view()
def bank_transfers(request):            
    
    url_payment = "https://api.flutterwave.com/v3/charges?type=bank_transfer"

    payload_payment = {
        "amount": 5,
        "currency": "USD",
        "card_number": 5531886652142950,
        "cvv": 564,
        "expiry_month": 9,
        "expiry_year": 32,
        "email": "user@flw.com",
        "tx_ref": "MC-3243e",
        
    }   
    
    headers_payment = {
        "Accept": "application/json",
        "Authorization": "Bearer FLWSECK_TEST-46af6f348fb05865e587f046398efb21-X",
        "Content-Type": "application/json"
    } 


    response_payment = requests.request("POST", url_payment, json=payload_payment, headers=headers_payment)
    
    return Response(response_payment)