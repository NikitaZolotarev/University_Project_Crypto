import socket
import select
import errno
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def generate_keys():
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

#генерим здесь ключи и отправляем паблик клиенту ИЛИ делаем абстракцию на классе
# достаем ключ or генерим их при подключении
def get_keys():
    with open('public_Alice.pem', 'rb') as f:
        public_key = RSA.import_key(f.read())
    with open('private_Bob.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())
    return private_key, public_key


private_key, public_key = get_keys()

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
print("sending public key")
client_socket.send(username_header + username)

#foreign_public_key = select(client_socket.recv(2048))

# создаем объект для шифрования/дешифрования
cipher_rsa = PKCS1_OAEP.new(public_key)
decipher_rsa = PKCS1_OAEP.new(private_key)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        # шифруем
        encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
        message_header = f"{len(encrypted_message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + encrypted_message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
#оно не декодит
#"хедер_нешифрованный + шифрованный месендж" - получить полный мессендж, отрезать хедер, декодить шифровку
#проверить recv
            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)
            #HEADER_LENGTH + message_length
         #   message.replace(message)
            #дешифруем
            decrypted_message = decipher_rsa.decrypt(message).decode('utf-8')
            # Print message
            print(f'{username} > {decrypted_message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading__ error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('__Reading error: '.format(str(e)))
        sys.exit()