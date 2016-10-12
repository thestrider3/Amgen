# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 09:26:17 2016

@author: shivani
"""
from enum import Enum

class ApplicationStatus(Enum):
    IncompleteApplication = 'IncompleteApplication'
    UnderReview = 'UnderReview'
    Accepted = 'Accepted'
    Rejected = 'Rejected'
    Deleted = 'Deleted'
    

    