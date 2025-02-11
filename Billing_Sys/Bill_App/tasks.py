import threading
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_email(**self.kwargs)
        except Exception as e:
            print("Threading function exception:", e)


def send_email(**kwargs):
    try:
        to_address = kwargs.get("to_email")
        total_cost = kwargs.get("total_amount", 0)  
        balance = kwargs.get("paid_amount", 0) - total_cost
        total_cost = '{:.2f}'.format(total_cost)
        balance = '{:.2f}'.format(balance)
        paid_amount = '{:.2f}'.format(kwargs.get("paid_amount", 0))
        subject = "Your Purchase Invoice"
        html_content = f"""
        <p>Thank you for your purchase.</p>
        <p><strong>Total Invoice: </strong> ₹{total_cost}</p>
        <p><strong>Paid Amount: </strong> ₹{paid_amount}</p>
        <p><strong>Balance: </strong> ₹{balance}</p>
        """
        
        from_address = settings.EMAIL_HOST_USER
        text_content = strip_tags(html_content)  # Strip HTML for plain text version
        
        email_msg = EmailMultiAlternatives(subject, text_content, from_address, [to_address])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()
        
    except Exception as e:
        print("Send email function exception:", e)

# # tasks.py
# from celery import shared_task
# from django.core.mail import send_mail

# @shared_task
# def send_email_to_customer(to_email, subject, message):
#     send_mail(
#         subject,
#         message,
#         "laranssd17@gmail.com",  # Change this to your sender email
#         [to_email],
#         fail_silently=False,
#     )
#     return f"Email sent to {to_email}"
