from django.shortcuts import render,redirect
from .models import User,ProductCategory,BrandProductCategory,BrandProductList
#########################################################################
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#########################################################################



def send_mail(email, message, subject="Mail From Edison Company"):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mjanokodesh@gmail.com"  
    sender_password = "swkb pzug apvk mioh"  
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, sender_password) 
            server.send_message(msg)
        
        print(f"Email sent successfully to {email}")
    
    except Exception as e:
        print(f"Failed to send email: {e}")



def generate_otp():
    otp = random.randint(100000, 999999)
    return otp



##########################################################################################################################

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages  # For flashing success/error messages

def contact(request):
    if request.method == 'POST':
        # Capture form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')  # This will now hold the country name
        message = request.POST.get('message')

        # Send email logic
        subject = f"Message from {first_name} {last_name}"
        message_body = f"Message from {first_name} {last_name}:\n\n{message}\n\nContact Information:\nPhone: {phone}\nEmail: {email}\nCountry: {country}"

        try:
            send_mail(
                subject,          # Subject
                message_body,     # Message Body
                email,            # From email
                ['mjanokodesh@example.com'],  # Recipient email
                fail_silently=False  # Optional: Set to False to raise exceptions if an error occurs
            )
            # Flash success message
            messages.success(request, 'Message sent successfully!')
        except Exception as e:
            # Flash error message
            messages.error(request, f"Error: {str(e)}")

        # Redirect back to the contact page
        return redirect('contact')  # 'contact' should match your URL name for the contact page

    # Handle GET request (display the contact form)
    return render(request, "main/contact.htm")

#######################################################################################################
def login(request):
    email = request.session.get('email', 'Guest')  
    if email == "Guest":

        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            print(email,password)
            if User.objects.filter(email=email).exists():
                request.session['email'] = email
                request.session['is_authenticated'] = True
                return redirect("index")
            
            else:
                return redirect("register")
            
        return render(request,"main/login.htm")
    else:
        return redirect("index")

def otp(request):
    email = request.session.get('email', 'Guest')
    
    if email == "Guest":
        if request.method == "POST":
            otp = request.POST.get("otp")
            user_data = request.session.get('user_data', {})

            verify_otp = user_data.get('otp')

            if str(verify_otp) == str(otp):
                fullname = user_data.get('fullname')
                email = user_data.get('email')
                mobile = user_data.get('mobile')
                password = user_data.get('password')

                # Check if the user already exists
                user, created = User.objects.get_or_create(
                    email=email,
                )

                if created:
                    # If the user is created, set the password and other fields
                    user.set_password(password)  # Hash the password
                    messages.success(request, "Account created successfully!")
                else:
                    # User already exists
                    messages.warning(request, "User already exists with this email.")

                # Update other fields regardless of whether the user was created or not
                user.fullname = fullname
                user.mobile = mobile
                user.save()  # Save the user object to update the data in the database

                # Optionally, clear session data after successful registration
                request.session['user_data'] = {}  # Clear session after registration

                return redirect("/")  # Redirect to the home page after successful registration

        return render(request, "main/otp.htm")
    else:
        return redirect("index")


def Register(request):
    email = request.session.get('email', 'Guest')  
    if email == "Guest":
        if request.method == "POST":
            fullname = request.POST.get("fullname")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            password = request.POST.get("password")
            confirm = request.POST.get("confirm")
            
            otp = generate_otp()  # Generate OTP
            
            if password == confirm:
                # Save user data in session to be used in OTP verification
                request.session['user_data'] = {
                    'fullname': fullname,
                    'email': email,
                    'mobile': mobile,
                    'password': password,  
                    'otp': otp
                }
                
                message = f"""
                Verification Mail From Edison Company
                Your OTP : {otp}
                Kindly Don't Share with Anyone !!!
                """
                
                # Use Django's send_mail function with the required arguments
                send_mail(
                    'Verification Email from Edison Company',  # Subject
                    message,  # Message body
                    settings.EMAIL_HOST_USER,  # From email (configured in settings.py)
                    [email],  # Recipient list (email passed from form)
                    fail_silently=False  # Set to False to raise an exception on failure
                )

                return redirect("otp")  # Redirect to OTP page
                
        return render(request, "main/register.htm")
    else:
        return redirect("index")
#######################################################################################
def user_logout(request):
     # Logs out the user and manually clears the session
    request.session.flush()  # This manually clears the session
    return redirect('index')  # Redirect to the homepage or a login page

###################################################################################################################
from django.shortcuts import render
from .models import User, ProductCategory, BrandProductCategory


def index(request):
    # Get the email from the session or set as 'Guest'
    email = request.session.get('email', 'Guest')  
    print(f"Email from session: {email}")

    # Fetch product categories and brand product categories
    product_categories = ProductCategory.objects.all()
    brand_product_categories = BrandProductCategory.objects.all()

    # Get the user's fullname if logged in
    fullname = None

    if email != "Guest":
        try:
            # Fetch the user by email
            user = User.objects.get(email=email)

            # Get the fullname if available
            fullname = user.fullname if user.fullname else "User"

            # Print the user's name in the terminal
            print(f"User fullname: {fullname}")

            # Store the fullname in the session if you want to persist it across requests
            request.session['fullname'] = fullname

        except User.DoesNotExist:
            # Handle the case where the user is not found
            fullname = "Unknown"
            print("User not found. Setting fullname to Unknown.")

    # Pass the fullname to the template
    context = {
        'product_categories': product_categories,
        'brand_product_categories': brand_product_categories,
        'fullname': request.session.get('fullname', fullname),  # Use the fullname from session
    }

    return render(request, "main/index.htm", context)




#####################################################################################################################
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import ProductCategory, BrandProductCategory, BrandProductList, User

# Utility function to get user details from session
def get_user_from_session(request):
    email = request.session.get('email', 'Guest')
    if email != "Guest":
        user = User.objects.get(email=email)
        fullname = user.fullname
        return email, fullname
    else:
        return None, None

# Products view with session handling
def products(request):
    email, fullname = get_user_from_session(request)
    
    product_list = ProductCategory.objects.all()
    product_categories = ProductCategory.objects.all()
    brand_product_categories = BrandProductCategory.objects.all()

    return render(request, "main/products.htm", {
        "products": product_list,
        'product_categories': product_categories,
        'brand_product_categories': brand_product_categories,
        'fullname': fullname  # Pass fullname to the template
    })

# Brands view with session handling
def brands(request, id):
    email, fullname = get_user_from_session(request)

    if ProductCategory.objects.filter(id=id).exists():
        product_category = ProductCategory.objects.get(id=id)
        brands_list = BrandProductCategory.objects.filter(product_category=product_category)
        product_categories = ProductCategory.objects.all()
        brand_product_categories = BrandProductCategory.objects.all()

        return render(request, "main/brands.htm", {
            "brands": brands_list,
            'product_categories': product_categories,
            'brand_product_categories': brand_product_categories,
            'fullname': fullname  # Pass fullname to the template
        })
    else:
        return redirect("products")

# Brand Products view with session handling
def brand_products(request, id, bid):
    email, fullname = get_user_from_session(request)

    if ProductCategory.objects.filter(id=id).exists():
        brand_category = BrandProductCategory.objects.get(id=bid)
        brand_product_list = BrandProductList.objects.filter(brand_product_category=brand_category)
        product_categories = ProductCategory.objects.all()
        brand_product_categories = BrandProductCategory.objects.all()

        return render(request, "main/brand_products.htm", {
            "brand_products": brand_product_list,
            'product_categories': product_categories,
            'brand_product_categories': brand_product_categories,
            'fullname': fullname  # Pass fullname to the template
        })
    else:
        return redirect("products")

# Brand Product Details view with session handling
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import ProductCategory, BrandProductCategory, BrandProductList, User

# Utility function to get user details from session
def get_user_from_session(request):
    email = request.session.get('email', 'Guest')
    if email != "Guest":
        try:
            user = User.objects.get(email=email)
            fullname = user.fullname
            return email, fullname
        except User.DoesNotExist:
            # Return None if user does not exist
            return None, None
    else:
        return None, None

# Brand Product Details view with session handling and download check
def brand_product_details(request, id):
    email, fullname = get_user_from_session(request)

    if request.method == "POST":
        if email is None:
            # If user is not logged in, redirect back to the same page
            return redirect(request.path)  # Stay on the same page (product details page)
        
        # Code for sending order details via email (unchanged)
        fullname = request.POST.get("fullname")
        user_email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        pid = request.POST.get("product_id")
        pname = request.POST.get("product_name")

        message = f"""
        Order placement from {fullname}
        Details of the User:
        Name : {fullname}
        Email : {user_email}
        Mobile : {mobile}
        Product ID : {pid}
        Product Name : {pname}
        """

        try:
            send_mail(
                subject="Order Placement",
                message=message,
                from_email="mjanokodesh@gmail.com",
                recipient_list=["mjanokodesh@gmail.com"],
            )
            request.session['email_sent'] = True
        except Exception as e:
            messages.error(request, f"Email could not be sent: {str(e)}")
            request.session['email_sent'] = False

        return redirect(request.path)

    if BrandProductList.objects.filter(id=id).exists():
        product_details = BrandProductList.objects.get(id=id)
        product_categories = ProductCategory.objects.all()
        brand_product_categories = BrandProductCategory.objects.all()

        # If user exists, fetch user data
        if email != "Guest" and fullname is not None:
            try:
                user = User.objects.get(email=email)  # Ensure user exists before accessing
            except User.DoesNotExist:
                user = None
        else:
            user = None

        return render(request, "main/product_details.htm", {
            "product_details": product_details,
            "user": user,
            'product_categories': product_categories,
            'brand_product_categories': brand_product_categories,
            'fullname': fullname  # Pass fullname to the template
        })
    else:
        return redirect("products")

# Handling download button in the template
def handle_download(request, id):
    email, fullname = get_user_from_session(request)

    if email is None:
        # If the user is not logged in, redirect them back to the product details page
        return redirect(f"/brand_product_details/{id}")

    # If the user is logged in, allow download logic here
    # For example, you could trigger a file download or redirect to another page
    # Example: download the product PDF or provide a file to download
    product = BrandProductList.objects.get(id=id)
    # For example, returning a file
    response = HttpResponse(product.product_pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{product.product_name}.pdf"'
    return response



##########################################################################################################################


def solutions(request):
    email = request.session.get('email', 'Guest')  
    if email != "Guest":
        return render(request,"main/solutions.htm")
    else:
        return redirect("/")