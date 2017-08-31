from utils.api_utils.facebook_api import FacebookAPI 

fb = FacebookAPI(token="EAACEdEose0cBAPbk2c92jglJpBvNrXNzJJHakgMBUB4gy3PIkUHMmDzETqMP8LdufRx728zEZCFuvW4jbilSsh6S9Rqfppd8FgCbLknlQsxogl1pOvqaVxIgIXMf4BKF3vqUOVI8Q70FgoT5ZCLTnIzKLdyxZBM80EhHcKll0IvevIWnsCBp73keQL4tjmCyAqKigm68AZDZD")
fb.connect()
people_data = fb.request(ids=['231541427020961', '353020448134882'])

print(people_data)