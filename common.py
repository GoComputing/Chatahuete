CODE_COMMON__ERROR  = 0
CODE_SERVER__FULL   = 1
CODE_SERVER__OK     = 2
CODE_CLIENT__EXIT   = 3
CODE_CLIENT__IDLE   = 4


def str_code(code):
    if code == CODE_COMMON__ERROR:
        return "common->error"
    elif code == CODE_SERVER__FULL:
        return "server->full"
    elif code == CODE_SERVER__OK:
        return "server->ok"
    elif code == CODE_CLIENT__EXIT:
        return "client->exit"
    elif code == CODE_CLIENT__IDLE:
        return "client->idle"
    return "<unkown>"


def header(message_length, code):
    
    return format(message_length, '08d') + format(code, '08d')


def read_message(connection):
    
    length = connection.recv(8).decode()
    code = connection.recv(8).decode()
    if len(length) != 0 and len(code) != 0:
        length = int(length)
        code = int(code)
        msg = connection.recv(length)
    else:
        length = 0
        code = CODE_COMMON__ERROR
        msg = ''
    return code, msg


def send_message(connection, code, msg):
    
    package = (header(len(msg), code)+msg).encode()
    connection.send(package)
