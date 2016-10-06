# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 20:36:25 2016

@author: shivani
"""
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, name, pwd, userid, active=True):
        self.name = name
        self.id = userid
        self.active = active
        self.pwd = pwd

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True