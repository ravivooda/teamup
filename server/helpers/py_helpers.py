#!/usr/bin/python

import random,crypt

def hash_password(password):
    # valid characters: a-zA-Z0-9./
    CHARS = range(46, 58) + range(65, 91) + range(97, 123)
    salt = '$1$%s$' % ''.join(chr(CHARS[random.randint(0,63)]) for i in xrange(8))
    return crypt_password(password, salt)

def crypt_password(password, salt):
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    return crypt.crypt(password, salt)

def check_password(password, password_hash):
    if isinstance(password_hash, unicode):
        password_hash = password_hash.encode('utf-8')
    return crypt_password(password, password_hash) == password_hash
