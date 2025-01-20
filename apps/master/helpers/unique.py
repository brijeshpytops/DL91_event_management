import random
import string

def generate_otp(length=6):
    """
    Generates a random OTP of specified length.
    
    :param length: The length of the OTP. Default is 6.
    :return: A random OTP of the specified length.
    """
    otp_chars = string.digits
    return ''.join(random.choice(otp_chars) for _ in range(length))
