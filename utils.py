import requests
import time
import pytz

from datetime import datetime, timedelta

codes_returned = []

def get_current_time():
    moscow_tz = pytz.timezone('Europe/Moscow')
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    moscow_time = utc_now.astimezone(moscow_tz)
    return moscow_time.strftime('%Y-%m-%d %H:%M:%S')

def fetch_code(text):
    split = text.split('code: ')
    new_split = split[1].split(' to')[0].strip()
    code = f"{new_split.split('-')[0]}{new_split.split('-')[1]}"
    return code
    
def getsms(tries=0):
    if tries > 600:
        return "Code not received."
    response = requests.get('https://api.sms-activate.org/stubs/handler_api.php?api_key=YOUR API KEY&action=getRentStatus&id=YOUR RENT ID')
    if response.status_code == 200:
        received_time_str = response.json()["values"]["0"]['date']
        received_time = datetime.strptime(received_time_str, '%Y-%m-%d %H:%M:%S')
        moscow_timezone = pytz.timezone('Europe/Moscow')
        received_time = moscow_timezone.localize(received_time)
        expiry_time = received_time + timedelta(seconds=10)
        current_time = datetime.now(moscow_timezone)
        
        if current_time < expiry_time:
            code = fetch_code(response.json()["values"]["0"]["text"])
            if code in codes_returned:
                time.sleep(1)
                return getsms(tries+1)
            codes_returned.append(code)
            return code
        else:
            time.sleep(1)
            return getsms(tries+1)
    else:
        return "API error."
