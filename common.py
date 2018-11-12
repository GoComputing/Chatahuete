CODE_COMMON__ERROR              = 1000
CODE_SERVER__FULL               = 1001

CODE_SERVER__OK                 = 2000
CODE_CLIENT__EXIT               = 2001
CODE_CLIENT__IDLE               = 2002

CODE_CLIENT__TRY_NICK           = 3000
CODE_SERVER__NICK_OK            = 3001
CODE_SERVER__NICK_DENY          = 3002
CODE_SERVER__USER_NICK_CHANGED  = 3003

CODE_SERVER__ROOMS_MODIFIED     = 4000
CODE_CLIENT__CONNECT_ROOM       = 4001
CODE_SERVER__ROOM_CONNECTED     = 4002
CODE_SERVER__ROOM_DENY          = 4003
CODE_SERVER__USERS_ROOM_CHANGED = 4004
CODE_CLIENT__REQUEST_ROOMS      = 4005

CODE_CLIENT__NEW_MESSAGE        = 5000
CODE_SERVER__BAD_LAST_MESSAGE   = 5001
CODE_SERVER__MESSAGE_OK         = 5002
CODE_SERVER__NEW_MESSAGE        = 5003


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
    elif code == CODE_CLIENT__TRY_NICK:
        return "client->try_nick"
    elif code == CODE_SERVER__NICK_OK:
        return "server->nick_ok"
    elif code == CODE_SERVER__NICK_DENY:
        return "server->nick_deny"
    elif code == CODE_SERVER__ROOMS_MODIFIED:
        return "server->rooms_modified"
    elif code == CODE_CLIENT__CONNECT_ROOM:
        return "client->connect_room"
    elif code == CODE_SERVER__ROOM_CONNECTED:
        return "server->room_connected"
    elif code == CODE_SERVER__ROOM_DENY:
        return "server->room_deny"
    elif code == CODE_SERVER__USERS_ROOM_CHANGED:
        return "server->users_room_changed"
    elif code == CODE_CLIENT__REQUEST_ROOMS:
        return "client->request_rooms"
    return "<unkown>"


def header(message_length, code):
    
    return format(message_length, '08d') + format(code, '08d')


def read_message(connection):
    
    length = connection.recv(8).decode()
    code = connection.recv(8).decode()
    if len(length) != 0 and len(code) != 0:
        length = int(length)
        code = int(code)
        msg = connection.recv(length).decode()
    else:
        length = 0
        code = CODE_COMMON__ERROR
        msg = ''
    return code, msg


def send_message(connection, code, msg):
    
    package = (header(len(msg), code)+msg).encode()
    connection.send(package)
