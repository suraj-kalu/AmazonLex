import json
import logging
import urllib3


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # TODO implement
    logger.debug(event)

    if event['currentIntent']['name'] == 'CurrencyData':
        base_code = event["currentIntent"]["slots"]["base_code"]
        final_code = event['currentIntent']['slots']['final_code']
        amount = event['currentIntent']['slots']['amount']
        
        http = urllib3.PoolManager()
        response = http.request('GET', 'http://api.currencylayer.com/live?access_key=API_KEY')
        if response.status == 200:
            heroes = json.loads(response.data.decode('utf-8'))
            quotes = heroes["quotes"]
            new_format = dict()
            for code, currency in quotes.items():
                new_format[code[3:]] = currency
            if (float(amount) > 0.0) and (final_code.upper() in new_format.keys()) and (base_code.upper() in new_format.keys()):
                usd_amount = float(amount)/new_format[base_code.upper()]
                # final_amount = usd_amount * new_format[curr_code.upper()]
                return{
                        "sessionAttributes": event["sessionAttributes"],
                        "dialogAction": {
                            # "type": "Close",
                            "type":"ElicitSlot",
                            "intentName" : "EmailConfirmation",
                            # "fulfillmentState": "Fulfilled",
                            "slotToElicit" : "confirm",
                            "message": {
                                "contentType": "PlainText",
                                "content": f"{str(amount)} {base_code.upper()} equals to {str(round(usd_amount * new_format[final_code.upper()],3))} {final_code.upper()}. " + 
                                "Do you want to send this information to your email id?"
                            }
                        }
                    }
            else:
                return{
                        "sessionAttributes": event["sessionAttributes"],
                        "dialogAction": {
                            "type": "Close",
                            "fulfillmentState": "Fulfilled",
                            "message": {
                                "contentType": "PlainText",
                                "content": "Invalid inputs provided"
                            }
                        }
                    }
        else:
            return{
                    "sessionAttributes": event["sessionAttributes"],
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": "Access denied"
                            }
                        }
                    }
    
    elif event['currentIntent']['name'] == 'EmailConfirmation':
        confirm = event['currentIntent']['slots']['confirm']
        if confirm.upper() == "YES":
            return{
                "sessionAttributes" : event["sessionAttributes"],
                "dialogAction" : {
                    "type":"ElicitSlot",
                    "intentName":"SendEmail",
                    "slotToElicit" : "email",
                    "message":{
                        "contentType":"PlainText",
                        "content" : "Please enter your email address"
                    }
                }
            }
        else:
            
            return{
                        "sessionAttributes": event["sessionAttributes"],
                        "dialogAction": {
                            "type": "Close",
                            "fulfillmentState": "Fulfilled",
                            "message": {
                                "contentType": "PlainText",
                                "content": "Thank you for using our service!"
                            }
                        }
                    }
    
    elif event['currentIntent']['name'] == 'SendEmail':
        email = event['currentIntent']['slots']['email']
        return{
                        "sessionAttributes": event["sessionAttributes"],
                        "dialogAction": {
                            "type": "Close",
                            "fulfillmentState": "Fulfilled",
                            "message": {
                                "contentType": "PlainText",
                                "content": f"Email has been send to {email}"
                            }
                        }
                    }

    else:
        return{
                "sessionAttributes": event["sessionAttributes"],
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": str(final_amount)
                            }
                        }
                    }
           

