import string
import random

"""
Get a unique reference number. The generated reference 
number should start in the primary key value.

@param int pk   The primary key IGReport.id
                whose max value is 2147483647
                
@return str returns the reference number
"""
def get_reference_number(pk):
    
    sep = '0'
    maxval = 2147483647
    
    if pk >= maxval:
        return '%s%s' % (pk, sep)
    
    maxlen = len('%s' % maxval)
    pklen = len( '%s' % pk ) 
    digits = maxlen - pklen
    
    rand = generate_random_str(digits, string.digits)
    reference_number = '%s%s%s' % (pk, sep, rand)
    
    return reference_number
    
def generate_random_str(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))