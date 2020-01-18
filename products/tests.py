import random
import string


def create_ref_code():
    ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(ref_code)
    return ref_code
create_ref_code()