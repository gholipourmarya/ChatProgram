import socket  # Import socket for network communication
import select  # Import select for monitoring multiple sockets
import sys  # Import sys for system operations
import os  # Import os for path manipulations
import colorama

# Add parent directory to sys.path to import from sibling folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import header constants and format function
from Header.header import LENGTH_HEADER_SIZE, USER_HEADER_SIZE


class ChatServer:
    """
       - A TCP-based chat server that handles multiple clients using select.
        -The server accepts incoming client connections
        -receives messages
        -broadcasts them to all other connected clients.
        -It uses non-blocking I/O
        -the select module to manage multiple socket connections.
    """
    def __init__(self, host, port, backlog=10):  # Initialize server with host, port, and backlog
        """
                -Initialize the chat server with host, port, and backlog settings.
                -Argument:
                    *host(str): The IP address or hostname to bind the server to.
                    *port(int): The port number to listen on.
                    *backlog(int, optional): Maximum number of queued connections. Defaults to 10.
        """
        self.host = host  # Server IP address or hostname
        self.port = port  # Server port number
        self.backlog = backlog  # Maximum number of queued connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP server socket socket_family=AF_INET,socket_type=SOCK_STREAM
        self.all_sockets = []  # List to track all sockets activ (server and clients)

    def start(self):  # Start listening for client connections and handle them
        """
                -Start the chat server and handle incoming connections and messages.
                -Continuously listens for client activity
                -using select
                -accepts new-connections
                -handles incoming messages from connected clients.
                -call the Method:
                    *accept_connection()
                    *handle_client_message()
                    *disconnect()
        """
        self.server_socket.bind((self.host, self.port))  # Bind server socket to host and port
        self.server_socket.listen(self.backlog)  # Start listening with a backlog limit----waiting for new connections from clients.
        self.all_sockets = [self.server_socket]  # Add server socket to list of monitored sockets -----which contains all active connections, including the server itself.---The server_socket is added to this list first,
        print(colorama.Fore.GREEN+f"Listening on {colorama.Fore.YELLOW}{self.host}{colorama.Fore.GREEN} : {colorama.Fore.YELLOW}{self.port}")  # Log that the server has started

        while True:  # Infinite loop to keep the server running
            # Monitor sockets for activity using select
            read_sockets, _, error_sockets = select.select(self.all_sockets, [], self.all_sockets)

            for sock in read_sockets:  # For each socket ready to be read
                if sock == self.server_socket:  # New connection attempt on server socket
                    self.accept_connection()  # Accept the new client
                else:
                    self.handle_client_message(sock)  # Handle a message from an existing client

            for err_sock in error_sockets:  # Handle sockets with errors
                self.disconnect(err_sock)  # Cleanly disconnect and remove the socket

    def accept_connection(self):  # Accept new incoming client connection
        """
                -Accept a new incoming client connection.
                -Adds the client socket to the list of all active sockets.
        """
        client_socket, client_address = self.server_socket.accept()  # Accept connection
        self.all_sockets.append(client_socket)  # Add new client to list
        print(colorama.Fore.BLUE+f"Established connection to {colorama.Fore.YELLOW}{client_address[0]}{colorama.Fore.BLUE}:{colorama.Fore.YELLOW}{client_address[1]}")  # Log connection details

    def handle_client_message(self, client_socket):  # Receive and handle message from client
        """
            -Handle an incoming message from a client
            -If Attempts to receive a message and broadcasts it to all other clients
            -call the Method:
                    *broadcast()
                    *disconnect()
            -Disconnects the client on failure or disconnection
            -Argument:
                *client_socket: The socket of the client sending the message.
        """
        try:
            message = self.receive(client_socket)  # Try to receive a message
            if message:  # If message was received
                self.broadcast(client_socket, message)  # Broadcast it to all other clients
            else:
                self.disconnect(client_socket)  # Client disconnected
        except (ConnectionResetError, OSError):  # Handle client crashing/disconnecting
            self.disconnect(client_socket)
            print(colorama.Fore.LIGHTRED_EX+"Client forcefully closed the connection.")  # Log abrupt disconnect

    def receive(self, client_socket):  # Receive full message from client socket
        """
               -Receive a full message from the client socket.
               -Receives the length header, user header, and actual message content.
               -Returns:
                    * the formatted message string if successful
                    * None if on failure.
               -Argument:
                    *client_socket: The client socket to read from.
               -Returns:
                    *str: The full formatted message
                    *None: None if an error occurred.
        """
        try:
            size_header = client_socket.recv(LENGTH_HEADER_SIZE)  # Receive message length
            if not size_header:  # If nothing is received, client likely disconnected
                return None

            size_header = size_header.decode('utf-8')  # Decode the length header
            message_size = int(size_header.strip())  # Convert header to integer

            user_header = client_socket.recv(USER_HEADER_SIZE).decode('utf-8')  # Receive and decode username
            user = user_header.strip()  # Strip extra spaces
            message = client_socket.recv(message_size).decode('utf-8')  # Receive the actual message

            print(colorama.Fore.LIGHTBLUE_EX+f"{user} >> {colorama.Fore.YELLOW} {message}")  # Log the message on server side
            return f"{size_header}{user_header}{message}"  # Return raw formatted message for broadcasting
        except:  # If any issue occurs during receiving, treat as disconnect
            return None

    def broadcast(self, sender_socket, message):  # Send message to all connected clients except sender
        """
                -Broadcast a message to all connected clients except the sender.
                -call the Method:
                    *send()
                    *disconnect()
                -Argument:
                    *sender_socket: The socket that sent the original message.
                    *message(str): The message to broadcast.
        """
        for sock in self.all_sockets:
            if sock != sender_socket and sock != self.server_socket:  # Skip sender and server socket
                try:
                    sock.send(message.encode('utf-8'))  # Send message
                except:  # If sending fails, disconnect client
                    self.disconnect(sock)

    def disconnect(self, sock):  # Cleanly disconnect a client
        """
               -Disconnect and clean up a socket.
               -Removes the socket from the tracking list and closes it.
               -Argument:
                    *sock: The socket to disconnect and remove.
        """
        if sock in self.all_sockets:
            print(colorama.Fore.RED+f"Disconnected: {sock.getpeername()}")  # Log the disconnection##name
            self.all_sockets.remove(sock)  # Remove from the socket list
            sock.close()  # Close the socket
