import string
import secrets

#a function to randomly append certain chars together x number of times
def put_chars_at_random(min_range:int,max_range:int,chars_group:str) -> str:
    psw = ""
    range_choice = secrets.choice(range(min_range,max_range))
    for _ in range(range_choice):
        psw += ''.join(secrets.choice(chars_group))
    return psw

def gen_strong_password() -> str:
    secretsGenerator = secrets.SystemRandom()
    special_chars = '!@#$%^&*<>?{}'
    digits = string.digits
    upper_letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase

    length = secrets.choice(range(8,13))

    # start generating password, starting with special characters
    password = put_chars_at_random(3,length-4,special_chars)

    # make sure the max of the range will be valid for digits
    check_range1 = 4 if length - len(password) < 2 else length - len(password) -1
    password += put_chars_at_random(3,check_range1,digits)

    # make sure the max of the range will be valid for the uppercase
    check_range2 = 2 if length - len(password) == 1 else length - len(password)
    password += put_chars_at_random(1,check_range2,upper_letters)

    # if there is more available space until we reach the length, fill it with lowercase
    while len(password) != length:
        password += ''.join(secrets.choice(lower_letters))
    
    #lastly shuffle to ensure extra randomness
    password = list(password)
    secretsGenerator.shuffle(password)

    return "".join(password)

if __name__ == "__main__":
    print(gen_strong_password())


        
