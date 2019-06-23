# ======================================================================================================================
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users, Reviews
from datetime import datetime
import bcrypt
# ======================================================================================================================
def debug(request):
    context = {
        "name": "Noelle",
        "favorite_color": "turquoise",
        "pets": ["Bruce", "Fitz", "Georgie"]
    }
    return render(request, "DojoApp/debug.html", context)
    #return HttpResponse('Hello')
# ======================================================================================================================
# ======================================================================================================================
def get_user_info(user_id):
    return {'user': Users.objects.get(id=user_id)}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def get_all_users_info():
    return {'users': Users.objects.all()}
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
def root(request):

    # Initialize session
    if 'user_logged_in' not in request.session:
        request.session['user_logged_in'] = {}
        request.session['logged_in'] = False # TODO: Change this to an element of the logged_in dictinoary
    else:
        request.session['logged_in'] = True # TODO: Remove hack


    return redirect("/users/reg_login")

    # # TODO: Correct this logic
    # #  -Desired: if user is already logged in then route to review/comment-page, else, route to register/login-page
    # if request.session['logged_in'] == None or request.session['logged_in'] == False:
    #     return redirect("/users/reg_login")
    # else:
    #     # if logged-in then go to wall
    #     return redirect("/wall")
# ======================================================================================================================
def reg_login(request):
    return render(request, "DojoApp/reg_login.html")
# ======================================================================================================================
# MAIN PAGE
def books(request):

    # # DEBUG
    # user_id = request.session['user_logged_in']['id']
    # user = Users.objects.get(id=user_id)       # Grab specific user
    # print(user)
    # #review = Reviews.objects.create(review='test review', user=user)
    # review = Reviews.objects.create(review='test review')
    # print(Reviews.objects.all())


    # time = datetime.now()
    # time = time.strftime("%Y/%m/%d %I:%M %p")
    return render(request, "DojoApp/books.html", {'reviews': Reviews.objects.all()})
# ======================================================================================================================
def post_review(request):

    # Step 0: Grab the value of the field from request.POST['review']
    review = request.POST['review']

    # Step 1: Create a new review row in the Table
    user_id = request.session['user_logged_in']['id']

    # TODO: Tie each review to a specific user (e.g., uncomment out below)
    user = Users.objects.get(id=user_id)
    review = Reviews.objects.create(review=review, user=user) # TODO: Change to review
    #review = Reviews.objects.create(review=review)

    # Step 2: Pass table into HTML
    reviews = Reviews.objects.all() # TODO: Change to review
    context = {'reviews': reviews}

    return render(request, "DojoApp/books.html", context)
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
def validate(request):

    # Return true if no errors
    valid = False

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Users.objects.basic_validator(request.POST, Users.objects.all())

    # check if the errors dictionary has anything in it
    if len(errors) > 0:

        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        # Errors found
        return valid

    else:
        # No erros => Valid
        valid = True
        return valid
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def register(request):

    valid = validate(request)
    if valid:

        # Grab values from form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password_orig = request.POST['password']

        # Hash Password
        password_hash = bcrypt.hashpw(password_orig.encode(), bcrypt.gensalt())

        # Create row in database
        user = Users.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash)

        messages.success(request, "Successfully registered")
        print("Successfully registered")
        return redirect("/users/reg_login")
    else: # not-valid
        # redirect the user back to the form to fix the errors
        return redirect("/users/reg_login")
# ======================================================================================================================
def userLogin(request):

    # Grab email from form
    email = request.POST['email-login']

    # Grab row from database IF email is in database
    # TODO: Check to see if email is in database
    user = Users.objects.get(email=email)


    # Grab entered password and test against stored hash
    password_login = request.POST['password-login']
    if bcrypt.checkpw(password_login.encode(), user.password_hash.encode()):

        # Set global logged-in variable to True
        request.session['logged_in'] = True

        print("password match")

        # Set Session with logged-in users info
        request.session['user_logged_in'] = {
            'id': user.id,
            'first_name': user.first_name,
            'logged_in': True
        }

        # Get one of the guys in this dictionary like so:
        #request.session['user_logged_in']['id']

        # return render(request, "DojoApp/logged_in.html", {'user': user})
        return redirect("/books")
    else:
        print("failed password")
        return HttpResponse("You Loose!")
# ======================================================================================================================
def logout(request):
    request.session.pop('user_logged_in')
    request.session['logged_in'] = True
    return redirect("/")
# ======================================================================================================================
