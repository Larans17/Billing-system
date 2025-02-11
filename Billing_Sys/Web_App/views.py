from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
import json
from django.conf import settings
# Create your views here.
base_url = settings.API_BASE_URL

def billing(request):
    if request.method == "POST":
        cus_mail = request.POST.get('customer_email')
        paid_amount = request.POST.get('paid_amount')
        bill_amount = request.POST.get('bill_amount')
        taxable_amount = request.POST.get('taxable_amount')
        tax_amount = request.POST.get('tax_amount')
        items = request.POST.get('items')
        deno = request.POST.get('denominations')

        data = {
            'customer_email': cus_mail,
            'items': items,  # JSON data should be properly formatted
            'denominations': deno,
            'paid_amount': paid_amount,
            'total_amount': bill_amount,
            'taxable_amount': taxable_amount,
            'tax_amount': tax_amount,
        }

        try:
            create_bill = requests.post(f"{base_url}create-purchase/", json=data)
            response_data = create_bill.json() 

            if create_bill.status_code == 201:
                return JsonResponse({'success': True, 'redirect_url': f'/bill-details/?email={cus_mail}'})
            return JsonResponse({'success': False, 'error': response_data}, status=create_bill.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return render(request, 'billing.html')

def bill_details(request):
    try:
        email = request.GET.get('email')
        response = requests.get(f"{base_url}purchases/{email}/")
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch bill details', 'details': str(e)}, status=500)
    
    return render(request,'bill-details.html',context={'bill_data':data,'email':email})


def get_products(request):
    try:
        response = requests.get(f"{base_url}create-purchase/")
        response.raise_for_status()
        get_product = response.json()
        return JsonResponse(get_product)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch products', 'details': str(e)}, status=500)