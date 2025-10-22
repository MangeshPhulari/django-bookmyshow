# movies/payu_utils.py

import hashlib
from django.conf import settings

def generate_hash(txnid, amount, productinfo, firstname, email, udf1='', udf2='', udf3='', udf4='', udf5=''):
    """
    Generates the SHA512 hash required by PayU, including UDFs.
    """
    key = settings.PAYU_MERCHANT_KEY
    salt = settings.PAYU_MERCHANT_SALT

    # PayU Hash Sequence:
    # key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt
    hash_string_parts = [
        key, txnid, str(amount), productinfo, firstname, email,
        udf1, udf2, udf3, udf4, udf5, # Include UDFs being used
        '', '', '', '', '', # Empty placeholders for udf6-udf10
        salt
    ]
    hash_string = '|'.join(hash_string_parts)
    hash_hex = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
    return hash_hex

def verify_hash(status, txnid, amount, productinfo, firstname, email, response_hash, udf1='', udf2='', udf3='', udf4='', udf5=''):
    """
    Verifies the hash received in the response from PayU, including UDFs.
    """
    key = settings.PAYU_MERCHANT_KEY
    salt = settings.PAYU_MERCHANT_SALT

    # PayU Response Hash Sequence:
    # salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key
    hash_string_parts = [
        salt, status,
        '', '', '', '', '', # Empty placeholders (reverse order compared to request)
        udf5, udf4, udf3, udf2, udf1, # Include UDFs from response
        email, firstname, productinfo, str(amount), txnid, key
    ]
    hash_string = '|'.join(hash_string_parts)
    generated_hash_hex = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

    # Debugging print for hash verification
    # print("--- Hash Verification ---")
    # print(f"String to hash: {hash_string}")
    # print(f"Generated Hash: {generated_hash_hex}")
    # print(f"Received Hash:  {response_hash}")
    # print("-------------------------")

    return generated_hash_hex == response_hash