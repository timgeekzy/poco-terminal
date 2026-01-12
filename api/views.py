from django.shortcuts import render
from django.http import JsonResponse
import requests

def home(request):
    """Renders the main terminal interface."""
    return render(request, 'index.html')

def get_token_info(request):
    """
    Fetches token info from Jupiter (Solana) or GeckoTerminal (Multi-chain).
    This acts as a proxy so your frontend doesn't get blocked.
    """
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'No address provided'}, status=400)

    # Example: Check Jupiter API for Solana tokens
    # You can expand this to check Ethereum APIs if needed
    url = f"https://api.jup.ag/price/v2?ids={address}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Parse Jupiter response
        if 'data' in data and address in data['data']:
            token_data = data['data'][address]
            return JsonResponse({
                'found': True,
                'price': token_data.get('price'),
                'type': 'Solana (Jupiter)'
            })
        else:
            return JsonResponse({'found': False, 'message': 'Token not found on Solana'})
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)