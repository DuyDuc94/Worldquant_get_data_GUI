import requests
import json
import time
import datetime
import pytz
import logging
import os
import traceback
from requests.exceptions import RequestException

# Tùy chỉnh log theo phong cách tối giản
fmt = logging.Formatter('%(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log = logging.getLogger("WQB_Processor")
log.addHandler(sh)
log.setLevel(logging.INFO)

# Tham số hệ thống
URL_TARGET = 'https://api.worldquantbrain.com/simulations'
FILE_STORE = './alpha.txt'
AUTH_PATH = './cookie.txt'

def get_session_config():
    return {
        "type": "REGULAR",
        "settings": {
            "nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1,
            "universe": "MINVOL1M", "truncation": 0.06, "unitHandling": "VERIFY",
            "pasteurization": "ON", "region": "GLB", "language": "FASTEXPR",
            "decay": 3, "neutralization": "STATISTICAL", "visualization": False, "maxTrade": "OFF"
        }
    }

def grab_credentials():
    if not os.path.exists(AUTH_PATH):
        return None
    with open(AUTH_PATH, 'r') as f:
        return f.read().strip()

def filter_completed(path, done_set):
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        with open(path, 'w') as f:
            f.writelines([ln for ln in lines if ln.strip().replace('"', '').replace(' ', '') not in done_set])
    except Exception as e:
        log.error(f"Sync fail: {e}")

def transmit_payload(http, payload, token):
    for r in range(3):
        try:
            res = http.post(URL_TARGET, json=payload, headers={'Cookie': token}, timeout=20)
            data = res.text
            if "SIMULATION_LIMIT_EXCEEDED" in data:
                time.sleep(40)
                continue
            if "Incorrect authentication" in data:
                return "AUTH_ERR"
            res.raise_for_status()
            return "OK"
        except Exception:
            time.sleep(5 * (r + 1))
    return "FAIL"

def execute_batch():
    token = grab_credentials()
    if not token: return
    
    http = requests.Session()
    conf = get_session_config()
    
    while True:
        try:
            if not os.path.exists(FILE_STORE): break
            with open(FILE_STORE, 'r') as f:
                pool = [x.strip().replace('"', '').replace(' ', '') for x in f if x.strip()]
            
            if not pool:
                log.info("No data found. Retrying in 60s...")
                time.sleep(60)
                continue

            processed = []
            for item in pool:
                conf["regular"] = item
                status = transmit_payload(http, conf, token)
                
                if status == "OK":
                    processed.append(item)
                    log.info(f"Done: {item}")
                    time.sleep(1.5)
                elif status == "AUTH_ERR":
                    log.error("Auth expired.")
                    return
                
            if processed:
                filter_completed(FILE_STORE, set(processed))
            
            time.sleep(20)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    execute_batch()