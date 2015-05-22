def keygen_version2(username):
    for i, u in enumerate(username):
        if i%2:
            key += str(ord(u.upper()))
        else:
            key += str(ord(u.lower()))
    return key[:8]
