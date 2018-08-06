from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if postData['type'] == 'register':
            if len(postData['first_name']) == 0:
                errors['First Name'] = "First Name field is empty"

            if len(postData['last_name']) == 0:
                errors['Last Name'] = "Last Name field is empty"

            if len(postData['email']) == 0:
                errors['Email'] = "Email field is empty"

            if len(postData['password']) < 8:
                errors['password'] = "Password should be greater than 8 characters"

            if len(postData['password']) == 0:
                errors['Password'] = "Password field is empty"

            elif postData['password'] != postData['cf_password']:
                errors['Password'] = "Passwords do not match"

            if not EMAIL_REGEX.match(postData['email']):
                errors['Email'] = "Email is in inproper format"

        if postData['type'] == 'login':
            if len(postData['email']) == 0:
                errors['Email'] = "Email field is empty"
            if len(postData['password']) == 0:
                errors['Password'] = "Password field is empty"
            if not EMAIL_REGEX.match(postData['email']):
                errors['Email'] = "Email is in inproper format"
            if len(errors) == 0:
                if not self.filter(email = postData['email']).exists():
                    errors['Email'] = 'Email is not registered'
                else:
                    this_user = User.objects.get(email = postData['email'])
                    if not bcrypt.checkpw(postData['password'].encode(), this_user.salt.encode()):
                        errors['Password'] = 'Password is invalid'
                
                    

        return errors

    def createUser(self,fName,lName,email,password,birthday):
        hash1 = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        User.objects.create(first_name = fName, last_name = lName, email = email, password = password, birthday=birthday, salt = hash1)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    objects = UserManager()
    