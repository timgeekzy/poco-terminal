from django.shortcuts import render
from django.http import JsonResponse
import requests

def home(request):
    """Renders the main terminal interface."""
    return render(request, 'index.html')

# In api/views.py

def get_token_info(request):
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'No address provided'}, status=400)

    # NEW: Switch to DexScreener API (Finds EVERYTHING: Solana, Base, ETH, Pump.fun)
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # DexScreener returns a list of 'pairs'. We want the most liquid one.
        if 'pairs' in data and data['pairs']:
            best_pair = data['pairs'][0] # The first one is usually the main one
            
            return JsonResponse({
                'found': True,
                'symbol': best_pair.get('baseToken', {}).get('symbol', 'UNKNOWN'),
                'price': best_pair.get('priceUsd', '0'),
                'liquidity': best_pair.get('liquidity', {}).get('usd', 0),
                'chain': best_pair.get('chainId', 'unknown').title()
            })
        else:
            # If DexScreener can't find it, it truly doesn't exist
            return JsonResponse({'found': False, 'message': 'Token not found (New or invalid)'})
            
    except Exception as e:
        return JsonResponse({'found': False, 'error': str(e)}, status=500)