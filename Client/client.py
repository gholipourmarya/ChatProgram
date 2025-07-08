import tkinter as tk  # Import Tkinter for GUI creation
from tkinter import messagebox  # For showing pop-up message boxes
from threading import Thread  # For running background tasks using threads
import socket  # For creating network connections
import sys  # For system-level operations
import errno  # For handling specific socket error codes
import os  # For working with file paths and directories
import colorama

# Add the parent directory to the system path so we can import from sibling folders
header_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Header'))
sys.path.append(header_path)
# Import constants and message formatting function from the header module
from header import LENGTH_HEADER_SIZE, USER_HEADER_SIZE, format_message



class NewWindow:
    """
        -A GUI chat window that connects to a server via TCP socket
        -Creates a new chat interface using Tkinter
        -connects to the specified server
        -enables sending and receiving messages using threads
        -displays incoming messages in a chat log
    """
    def __init__(self, master, host, port):  # Initialize the chat window
        """
             -Initialize the chat window and establish a connection to the server.
             -Argument:
                 * master(tk.Tk): The main/root Tkinter window.
                 * host(str): The server's IP address.
                 * port(int): The server's port number.
                 -call the Method:
                    *build_ui()
                    *start_receive_thread()
        """
        self.host = host  # Store the server IP address
        self.port = port  # Store the server port number
        self.master = master  # Store reference to the main/root Tkinter window

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP server socket socket_family=AF_INET,socket_type=SOCK_STREAM
        self.client_socket.connect((self.host, self.port))  # Connect to the chat server
        self.client_socket.setblocking(False)  # Set socket to non-blocking mode to prevent GUI freezing

        self.window = tk.Toplevel(master)  # Create a new top-level window (separate from the root)
        self.window.title("Chatroom")  # Set the title of the window
        self.window.geometry("530x450")  # Set the size of the chat window
        self.window.resizable(False, False)  # Disable resizing of the window

        self.build_ui()  # Call function to build the user interface
        self.start_receive_thread()  # Start a background thread to receive incoming messages

    def build_ui(self):  # Define and build the chat window UI elements
        """
               -Build the graphical user interface for the chat window.
               -Creates labels, entry, text, buttons, and the chat display area.
               -call the Method:
                    *send()
                    *exit()
        """
        frame = tk.Frame(self.window, borderwidth=7, relief="ridge", bg="lightblue")  # Main frame container
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Add padding and make frame expand to window

        tk.Label(frame, text='Name', bg="lightblue", font=('Times New Roman', 12, 'bold')).grid(row=0, column=0, sticky='w')  # Name label
        self.name_input = tk.Entry(frame, font=('Times New Roman', 12, 'bold'))  # Entry field for username
        self.name_input.grid(row=0, column=1, sticky='we')  # Place name input field in the grid

        self.confirm_btn = tk.Button(frame, text="Confirm", command=self.lock_username, bg="#3399FF", font=('Times New Roman', 12, 'bold'))  # Button to lock username
        self.confirm_btn.grid(row=0, column=2, padx=5)  # Position confirm button with padding

        self.chat_log = tk.Text(frame, state='disabled', height=20, font=('Times New Roman', 12, 'bold'), fg='blue')  # Text area for chat log
        self.chat_log.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=5)  # Make chat log span across columns

        tk.Label(frame, text='Message', bg="lightblue", font=('Times New Roman', 12, 'bold')).grid(row=2, column=0)  # Message label
        self.message_input = tk.Entry(frame, state='disabled', font=('Times New Roman', 12, 'bold'))  # Input for sending messages (initially disabled)
        self.message_input.grid(row=2, column=1)  # Place message input box

        self.send_btn = tk.Button(frame, text='Send', command=self.send, state='disabled', bg="#3399FF", font=('Times New Roman', 12, 'bold'))  # Send button (initially disabled)
        self.send_btn.grid(row=2, column=2)  # Place send button

        self.exit_btn = tk.Button(frame, text='Exit', command=self.exit, state='disabled', bg="#3399FF",
                                  font=('Times New Roman', 10, 'bold'))  # Send button (initially disabled)
        self.exit_btn.grid(
            row=3, column=0, columnspan=3,
            padx=10, pady=10,
            ipadx=10, ipady=10,
            sticky="we"
        ) # Place EXIT button

        frame.grid_rowconfigure(1, weight=1)  # Make chat log row expandable
        frame.grid_columnconfigure(1, weight=1)  # Make message input column expandable

    def lock_username(self):  # Function to lock the username after confirmation
        """
                -Lock the username after confirmation and enable chat controls.
                -Activates message input, send, and exit buttons after a name is entered.
                -Shows an error dialog if the name is empty.
        """
        if self.name_input.get():  # Check if user entered a name
            self.username = self.name_input.get()  # Store the username
            self.message_input.config(state='normal')  # Enable the message input field
            self.send_btn.config(state='normal')  # Enable the send button
            self.exit_btn.config(state='normal')  # Enable the exit button
            self.name_input.config(state='disabled')  # Disable name input field
            self.window.title(f'{self.username}')  # Set the window title to the username
        else:
            messagebox.showinfo('Error', 'Please enter your name!!')  # Show error if username is empty

    def send(self):  # Function to send a message to the server
        """
            -Send the message entered by the user to the server.
            -Displays the send message in the chat log.
            -call the Method:
                    *print_message
                    *format_message of haeder Modul
        """
        message = self.message_input.get()  # Get text from the message input field
        if message:  # If message is not empty
            self.print_message(f'\n{self.username} > {message}')  # Display the message locally
            formatted_message = format_message(self.username, message).encode('utf-8')  # Format and encode message---socket only byte read---not char
            self.client_socket.send(formatted_message)  # Send message to the server
            self.message_input.delete(0, tk.END)  # Clear the message input field

    def receive(self):  # Function to receive messages from the server
        """
                -Receive messages from the server in a continuous loop.
                -Reads and decodes incoming messages and updates the chat log.
                -Handles non-blocking socket errors gracefully.
                -call the Method:
                    *print_message
        """
        try:
            while True:  # Infinite loop to keep checking for new messages
                message_size = self.client_socket.recv(LENGTH_HEADER_SIZE)  # Read length header
                if not message_size:
                    break  # Exit if no data is received

                message_size = int(message_size.decode('utf-8').strip())  # Convert length to integer
                sender = self.client_socket.recv(USER_HEADER_SIZE).decode('utf-8').strip()  # Read sender's username
                message = self.client_socket.recv(message_size).decode('utf-8')  # Read message content
                self.print_message(f'\n{sender} > {message}')  # Display message in chat window
        except IOError as e:
            if e.errno not in (errno.EAGAIN, errno.EWOULDBLOCK):  # Handle non-blocking socket errors
                print(colorama.Fore.RED+'Error reading', e)
                self.client_socket.close()
                sys.exit()
        except Exception as e:  # Catch any unexpected error
            print(colorama.Fore.RED+'Unexpected error', e)
            self.client_socket.close()
            sys.exit()

    def exit(self):
        """
                -Send a sign-out message to the server
                -close the socket
                -close the chat window.
                -call the Method:
                    *print_message
        """
        message = format_message(self.username, 'Signing out')  # Format a sign-out message
        self.client_socket.send(message.encode('utf-8'))  # Send sign-out message
        self.print_message('\nSigned out')  # Print local confirmation
        self.client_socket.close()  # Close socket connection
        self.window.destroy()  # Close the chat window

    def start_receive_thread(self):  # Start background thread for receiving messages
        """
                Start a background thread to continuously receive messages without blocking the main GUI thread.
                -call the Method:
                    *receive_loop
        """
        receive_thread = Thread(target=self.receive_loop, daemon=True)  # Create a daemon thread
        receive_thread.start()  # Start the thread

    def receive_loop(self):  # Continuously call receive in a loop
        """
                -Continuously call the receive function in an infinite loop
                -Intended to run inside a background thread
                -call the Method:
                    *resive()
        """
        while True:
            self.receive()

    def print_message(self, message):  # Display message in the chat log
        """
               -Display a message in the chat log text area.
               -Argument:
                    *message(str): The message to be displayed.
        """
        self.chat_log.config(state='normal')  # Enable editing chat log
        self.chat_log.insert(tk.END, message)  # Insert new message at the end
        self.chat_log.config(state='disabled')  # Disable editing again to prevent user input
