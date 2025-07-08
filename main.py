import tkinter as tk  # Import Tkinter for GUI
from threading import Thread  # Import Thread for running the server concurrently
# Add the Client folder (one level up) to the Python path so we can import NewWindow
from Client.client import NewWindow  # Import the client's main window class
# Add the Server folder (one level up) to the Python path so we can import ChatServer
from Server.server import ChatServer  # Import the chat server class


class MainApp:
    """
        -Main application class for launching the GUI chat client and starting the server.
        -This class sets up the main Tkinter window and initializes the interface for signing in to the chat room.
        -When the sign-in button is clicked, it launches a new chat window.
    """
    def __init__(self, root, host, port):  # Initialize the main application
        """
               -Initialize the main application window and GUI layout.
               -Argument:
                   root(tk.Tk): The root Tkinter window.
                   host(str): The host address for the chat server.
                   port(int): The port number for the chat server.
               -call the Method:
                    *create_widgets()
        """
        self.root = root      # Reference to the root Tkinter window
        self.host = host      # Store server host address
        self.port = port      # Store server port number

        self.root.title("Chat Room")        # Set the title of the main window
        self.root.resizable(False, False)   # Disable window resizing
        self.root.geometry("400x200")       # Set fixed window size

        # Configure the root window's grid to make the single cell expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a frame inside the root window with a border and background color
        self.frame = tk.Frame(root, borderwidth=5, relief="ridge", bg="#67AB9F")
        self.frame.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)  # Place and pad the frame
        self.frame.grid_columnconfigure(0, weight=1)  # Make the frame's column expandable
        self.frame.grid_rowconfigure(0, weight=1)     # Make the frame's row expandable

        self.create_widgets()  # Build the child widgets inside the frame

    def create_widgets(self):
        """
                -Create and place the widgets inside the main application window.
                -This includes the "Sign in" button which launches the chat window.
                -call the Method:
                    *open_login_window
        """
        login_button = tk.Button(
            self.frame,
            text="Sign in",                # Button text
            command=self.open_login_window,  # Callback to open the chat window
            font=('Times New Roman', 20, 'bold'),
            bg='#A9C4EB'
        )
        login_button.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="we")

    def open_login_window(self):
        """
                -Open a new chat window (client) by creating an instance of NewWindow.
                -Passes the root Tkinter instance, server host, and port to the client.
        """
        NewWindow(self.root, self.host, self.port)

def start_server_in_thread(host, port):
    """
       -Start the chat server in the background.
       -This function runs the server in a blocking loop, so it should be called from a separate daemon thread.
       -Argument:
           host(str): Host address for the server to bind.
           port(int): Port number for the server to listen on.
        -call the
            *Create an instance of the ChatServer class (from the Server module)
            *call its start() method to launch the server.

    """
    server = ChatServer(host, port)
    server.start()

if __name__ == "__main__":
    # Set up the server to run on localhost and a specific port
    # Run the server in a background thread to allow GUI interaction
    # Start the main GUI loop for user interaction


    host = '127.0.0.1'  # Localhost address for server
    port = 5084         # Port number for the chat server

    # Launch the server in a daemon thread so it runs alongside the GUI
    server_thread = Thread(target=start_server_in_thread, args=(host, port), daemon=True)
    server_thread.start()

    # Initialize the Tkinter root window and start the GUI loop
    root = tk.Tk()
    app = MainApp(root, host, port)
    root.mainloop()  # Enter Tkinter's main event loop

