import base64


def encode64(string):
    temp = string.encode("ascii")
    temp = base64.b64encode(temp)
    return temp.decode("ascii")
