# Billing-system
A Django-based billing system with REST API and frontend integration. This system allows you to manage products, generate bills, track denominations, and send email invoices to customers.


**Features**

Product management with stock tracking
Dynamic billing calculation with tax support
Denomination management for cash transactions
Automatic change calculation based on available denominations
Email invoice generation and sending
Customer purchase history tracking
RESTful API support
Responsive frontend interface

**Tech Stack
**
**Backend:**

Django 5.0.1
Django REST Framework 3.14.0
Celery 5.3.6 (for async tasks)
Redis 5.0.1 (as message broker)


**Frontend:**

HTML5
Bootstrap 5.3.2
jQuery 3.6.0



**Prerequisites**

Python 3.12 
Redis server
Email server configuration (SMTP)

**Creating a New Bill**

Navigate to /billing/
Enter customer email
Add products and quantities
Update denomination counts if needed
Enter paid amount
Click "Generate Bill"

**Viewing Customer History**

Navigate to /bill-details/bills/
Enter customer email in the filter
View list of customer's bills
Click on individual bills for details
