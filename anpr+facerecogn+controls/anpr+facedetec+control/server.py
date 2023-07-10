
import socket

SERVER_IP = '192.168.1.23' \
            '' \
            ''
SERVER_PORT = 9999

def handle_client(conn):
    while True:
        # receive the command from the client
        command = conn.recv(1024).decode()
        if not command:
            break
        # process the command
        if command == 'forward':
            print('Moving forward')
        elif command == 'left':
            print('Turning left')
        elif command == 'right':
            print('Turning right')
        elif command == 'backward':
            print('Moving backward')

        elif command == 'diagonal_forward_left':
            print('diagonal_forward_left')
        elif command == 'diagonal_forward_right':
            print('diagonal_forward_right')
        elif command == 'diagonal_backward_left':
            print('diagonal_backward_left')
        elif command == 'diagonal_backward_right':
            print('diagonal_backward_right')

        elif command == 'rotate_left':
            print('rotate_left')
        elif command == 'rotate_right':
            print('rotate_right')

        else:
            print('Invalid command')
        # send a response to the client
        response = 'Command received: ' + command
        conn.send(response.encode())
    # close the connection
    conn.close()

# create a socket object
s = socket.socket()
# bind the socket to a specific IP address and port
s.bind((SERVER_IP, SERVER_PORT))
# start listening for incoming connections
s.listen()
print('Server is listening on {}:{}'.format(SERVER_IP, SERVER_PORT))
while True:
    # wait for a client to connect
    conn, addr = s.accept()
    print('Connected by', addr)
    # handle the client's requests in a separate thread
    handle_client(conn)
