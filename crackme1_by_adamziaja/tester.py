from subprocess import Popen, PIPE, STDOUT
import keygen
import random

def test(username, serial):
    p = Popen(['./crackme1'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input='{}\n{}\n'.format(username, serial))
    if grep_stdout[0].split()[-1].strip() != "OK!":
        return False
    else:
        return True

def generate_random_username():
    l = random.randint(8, 12)
    username = ''
    for i in range(l):
        username += chr( random.randint(65, 122))
    return username

nr_of_tests = 100   
for i in range(nr_of_tests):
    username = generate_random_username()
    serial = keygen.generate_key(username)
    res = test(username, serial)

    print("username: {}, serial: {}, result {}".format(
            username,
            serial,
            res))
    if not res:
        print("failed serial!")
        quit()
