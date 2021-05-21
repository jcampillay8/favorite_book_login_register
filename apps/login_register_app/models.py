from django.db import models
import re
import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
DATE_REGEX = re.compile(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        # Validate first name
        if(len(postData['first_name'])) < 2:
            errors['first_name']="First name must be more than 2 characters"
        elif postData['first_name'].isalpha() == False:
            errors['first_name'] = "First name cannot contain numbers"
        
        # Validate last name
        if(len(postData['last_name'])) < 2:
            errors['last_name'] = "Last name must be more than 2 characters"
        elif postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last name cannot contain numbers"

        # Validate Email
        if len(postData['email']) < 1:
            errors['email'] = "email must be more than 2 characters"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "email be a valid email address"
        
         # Validate Password
        if len(postData['password']) < 1:
            errors['password'] = "Password cannot be blank"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Invalid Password, must contain at least one uppercase and one number"
        
         # Validate Confrim Password
        if len(postData['confirm_password']) < 1:
            errors['confirm'] = "Confirm Password cannot be blank"
        elif postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords do not match"
        
        return errors

    def loginValidator(self, userData):
            errors = {}

            try:
                user = User.objects.get(email = userData["loginEmail"])

            except:
                errors["loginEmail"] = f"No email address matching {userData['loginEmail']} or an account associated with this email does not exist"
                # errors["loginEmail2"] = "an account associated with this email does not exist"
                return errors
            
            if not bcrypt.checkpw(userData["password"].encode(), user.password.encode()):
                errors["password"] = "Password does not match email address associated with this account. Please try again."

            return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()