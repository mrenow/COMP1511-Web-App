"""
Author: Ezra Hui

"""
# Overwrite send_mail with the definition given in the program's entry point if applicable
# If testing, __main__ will not contain send_mail. 
try:
    from __main__ import send_mail 
except(ImportError):
    # send_mail to do nothing for local testing
    def send_mail(msg):
        pass