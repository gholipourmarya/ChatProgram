# Constants defining fixed sizes for message headers
LENGTH_HEADER_SIZE = 8  # Number of characters used to encode the length of the message
USER_HEADER_SIZE = 16  # Number of characters used to encode the sender's username


def format_message(username, message):
    """
    -Format a chat message with fixed-length headers for length and username.
    -This function ensures that each message sent over the network has a consistent format, which includes:
        - A fixed-length header indicating the length of the message content.
        - A fixed-length header containing the username of the sender.
        - The actual message content.
    -Argument:
        username (str): The username of the sender.
        message (str): The message content to be sent.
    Returns:
        str: A string combining the length header, user header, and message,formatted as: "<length_header><user_header><message>".
        None: If the message is empty or None.
    Example:
        format_message("monik", "Hi")
        '2       monik           Hi'
    """
    if not message:
        return None  # Return None if there is no message content

    # Format the length of the message to a fixed width
    length_header = f'{len(message):<{LENGTH_HEADER_SIZE}}'

    # Format the username to a fixed width
    user_header = f'{username:<{USER_HEADER_SIZE}}'

    # Concatenate all parts into one formatted message
    return f'{length_header}{user_header}{message}'
