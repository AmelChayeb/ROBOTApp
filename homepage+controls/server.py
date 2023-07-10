import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

SERVER_IP = '192.168.1.23'
SERVER_PORT = 9999

def handle_client(conn):
    try:
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
                print('Stop')
            # send a response to the client
            response = 'Command received: ' + command
            conn.send(response.encode())
    except ConnectionResetError:
        print("Connection forcibly closed by the remote host")
    finally:
        # close the connection
        conn.close()

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr[0]}:{addr[1]} established!")
    handle_client(conn)
    print(f"Connection from {addr[0]}:{addr[1]} closed.")
