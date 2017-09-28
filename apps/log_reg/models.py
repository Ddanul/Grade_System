from __future__ import unicode_literals

from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def register_user(self, postData):
        response_to_views = {}
        errors = []
    #1. run our validations
        # is first name longer than 2 characters?
        if len(postData['name']) < 3:
            errors.append('Name must be at least 3 letters!')
        # is last name longer than 2 characters?
        if len(postData['username']) < 3:
            errors.append('Username must be at least 3 letters!')
        # is password longer than 8 characters?
        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters long!')
        # does confirm password match password?
        if not postData['password'] == postData['confirm']:
            errors.append('Password fields must match!')

        user = self.filter(username = postData['username'])

        if user:
            errors.append('Username must be unique!')

        if errors:
            response_to_views['status'] = False
            response_to_views['errors'] = errors

        else:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name = postData['name'], username = postData['username'], password = hashed)

            response_to_views['status'] = True
            response_to_views['user'] = user

        return response_to_views

    def login_user(self, postData):
        user = self.filter(username = postData['username'])
        response_to_views = {}

        if user:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                    response_to_views['status'] = True
                    response_to_views['user'] = user[0]
            else:
                    response_to_views['status'] = False
                    response_to_views['error'] = 'Invalid Username/password combination!'

        else:
            response_to_views['status'] = False
            response_to_views['error'] = 'Invalid username'

        return response_to_views

class User (models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
