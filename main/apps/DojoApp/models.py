from django.db import models
import re # regex module

# Custom manager for validation
class UsersManager(models.Manager):
    def basic_validator(self, postData, users):

        # Validation 1: Does name contain numbers?
        def hasNumbers(inputString):  # https://stackoverflow.com/a/19859308
            return any(char.isdigit() for char in inputString)

        errors = {}
        # add keys and values to errors dictionary for each invalid field

        # Validation 1 and 2:
        # Ensures names are at least of minimum length and do not contain numbers
        min_name_len = 1
        if len(postData['first_name']) < min_name_len or hasNumbers(postData['first_name']):
            errors["first_name"] = "first-name should be at least " + str(min_name_len) + " characters"
        if len(postData['last_name']) < min_name_len or hasNumbers(postData['last_name']):
            errors["last_name"] = "last-name should be at least " + str(min_name_len) + " characters"

        #  Validation 3: Does email have proper form?
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # create a regular expression object
        if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
            errors["email"] = "email does not have proper form"

        # Validation 4: Does second password match first?
        if(postData['password'] != postData['password-confirm']):
            errors["password"] = "Password entered does not match confirmation"

        # Validation 5: Ensure email is not already in database
        for user in users:
            if user.email == postData["email"]:
                errors["email_in_db"] = "Already registered!"
            break

       # TODO: Change to do the email validation in one of the following ways:
       #  1. User.objects.get(email=email)
       #    -If there is not a matching email for a .get(), Django throws an error (try and except could come in handy),
       #     otherwise it returns the User object associated with the matching user.e.g.Userobject.
       #  2. User.objects.filter(email = email)
       #     -Filter, on the other hand, returns a list, so if there is no user that matches,
       #      it returns an empty list.If there is a single matching user the list will contain a single User object:
       #      e.g.[Userobject].

        return errors
# ======================================================================================================================
# Table-1:
class Users(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

    def __repr__(self):
        return f"Users: ({self.first_name}, {self.last_name}, {self.email}), {self.password_hash})"
# ======================================================================================================================
# Table-2:
# Each user can have multiple review and each review is by one user (one-many: user->reviews)
class Reviews(models.Model):
    review = models.TextField()
    user = models.ForeignKey(Users, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Reviews: ({self.review})"
# ======================================================================================================================
# Table-3:
# Each book has multiple reviews and each review has one book (one-many:   book->reviews)
# Each book has multiple users and each user has multiple book (many-many: book<->users)
class Books(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Book: ({self.title})"
# ======================================================================================================================
# Table-4:
# Each author has multiple books and book has one author (one-many: author->books)
class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Book: ({self.name})"
