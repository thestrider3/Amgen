# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 21:32:52 2016

@author: shivani
"""

ReferenceStatus = {'ReferenceRequired':'ReferenceRequired',
                   'ReferenceSubmitted':'ReferenceSubmitted'}
                   
UserType = {'Student':"Student",
            'Mentor' : 'Mentor',
            'Admin' : 'Admin',
            'Referal' : 'Referal'}
            
ApplicationStatus={'IncompleteApplication' : 'IncompleteApplication',
    'ReferencesRequired2' : 'ReferencesRequired2',
    'ReferencesRequired1' : 'ReferencesRequired1',
    'UnderReview' : 'UnderReview',
    'Accepted' : 'Accepted',
    'Rejected' : 'Rejected',
    'Deleted' : 'Deleted',
    'PlaceholderAppStatus':'PlaceholderAppStatus'}
    
messages={
    'alreadyParticipated': 'Sorry! You are not eligible to apply to the Amgen Scholars Program at Columbia University and Barnard College.',
    'incompleteApplication':'Your application is incomplete! To proceed, you must complete all necessary fields.',
    'essayTooLong':'Your %s response is too long. Please make certain that your character counts include spaces, and decrease the character count until the application goes through.',
    'applicationSubmitted':'Success!! Your application has been received. To check the status of your application, please login into your account.',
    'incompleteApplicationMessage': 'Your application is incomplete, please resend request to your recommender or change your recommender(s) contact information. Please be aware that if you change your \
         recommender a message will be sent to your recommender cancelling the recommender request.',
    'recommendationSubmission':'Success! Thank you submitting the student’s recommendation.'


    
}

emailMessages = {
    'studentApplicationSubmission':'Dear %s, \n Your application has been received! \n To check the status of your application, please login into your account.',
    
    'recommenderRequestMail':'Dear %s %s,\n %s has requested that you recommend him or her to the AMGEN Scholars Summer Research Program affiliated with \
    Columbia University, a 10-week, full-time research program. \n Recommendations, only accepted online as a pdf, are due no later than Feb. 1st. \n \
    Please visit http://xxx and login using the following: \n Login: %s \n Password: %s'   ,
    
    'recommendationSubmission':'Thank you for your submission! \n Thank you! \n AMGEN Scholars Program at Columbia University and Barnard College',
    'recommendationSubmissionStudent':'%s has submitted their recommendation.\n Thank you! \n AMGEN Scholars Program at Columbia University and Barnard College',
    'recommendationCancellation':'The student that previously requested a recommendation from you has cancelled their request. \n Thank you! \n AMGEN Scholars Program at Columbia University and Barnard College'

}