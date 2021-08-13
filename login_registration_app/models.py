from django.db import models
import re
import bcrypt
from django.http import request


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User_Manager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters.'
            #check if it's a valid email layout
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email address entered.'
            # is the email in the database
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
            # does password match confirmed password
        if post_data['password'] != post_data['password_confirm']:
                errors['match'] = 'Passwords do not match'
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        existing_user = User.objects.filter(email = post_data['email'])[0]
        if not EMAIL_REGEX.match(post_data['email']):
            # message should not normally show whether email or password is wrong, just something is wrong
                errors['email'] = 'Invalid Email address entered.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password required'
        #  notice the changes between this and the actual line of code
        # if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()): 
        elif not bcrypt.checkpw(request.post_data['password'].encode(), existing_user.password.encode()):
            errors['mismatch'] = 'Enter a correct password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()
