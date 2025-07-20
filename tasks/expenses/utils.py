import requests
from django.core.cache import cache
import socket

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Fetch the latest exchange rate from frankfurter.app (no API key required).
    """
    url = "https://api.frankfurter.app/latest"
    params = {
        'from': from_currency,
        'to': to_currency,
    }
    resp = requests.get(url, params=params, timeout=5)
    data = resp.json()
    # Expected JSON: {"amount":1.0,"base":"USD","date":"2025-07-15","rates":{"EUR":0.92}}
    if resp.status_code != 200 or 'rates' not in data or to_currency not in data['rates']:
        raise ValueError(f"Frankfurter API error: {data}")
    return data['rates'][to_currency]

def get_cached_rate(from_currency: str, to_currency: str) -> float:
    key = f"rate_{from_currency}_{to_currency}"
    rate = cache.get(key)
    if rate is None:
        rate = get_exchange_rate(from_currency, to_currency)
        cache.set(key, rate, 60 * 60)  # 1-hour cache
    return rate

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable — just forces a selection
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP