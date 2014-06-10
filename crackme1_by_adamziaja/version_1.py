def keygen_version1(username):
    key = '' 
    for u in username:
        key += str(ord(u))
    return key[:8]
