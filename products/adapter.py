from allauth.account.adapter import DefaultAccountAdapter 
from django.forms import ValidationError 
  
class RestrictEmailAdapter(DefaultAccountAdapter): 
    def clean_email(self, email): 
        RestrictedList = ['m_milann@outlook.com'] 
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.') 
        return email 

  
# class UsernameMaxAdapter(DefaultAccountAdapter): 
#     def clean_username(self, username): 
#         if len(username) > 'Your Max Size': 
#             raise ValidationError('Please enter a username value\ 
#                                       less than the current one') 
          
#         # For other default validations. 
#         return DefaultAccountAdapter.clean_username(self, username)