# README.md

## EmailSMTPTool

### Description
The EmailSMTPTool is a Python class that allows an AI agent to send emails using the Simple Mail Transfer Protocol (SMTP). This tool provides an interface to compose an email with a subject and body, and send it to a specified recipient.

### Dependencies
This tool requires the following Python libraries to be installed:
- smtplib: for handling the SMTP protocol
- email.mime.multipart: for creating the email
- email.mime.text: for attaching text to the email

### Installation
To install the required dependencies, you can use pip:
```bash
pip install smtplib email.mime.multipart email.mime.text
```

### Usage
Here is an example of how to initialize and use this tool:
```python
from EmailSMTPTool import EmailSMTPTool

# Initialize the tool
tool = EmailSMTPTool('smtp.example.com', 587, 'myemail@example.com', 'mypassword')

# Use the tool to send an email
result = tool.forward('Hello World', 'This is a test email.', 'recipient@example.com')

print(result)  # "Email sent successfully."
```

### Configuration
You need to pass the following parameters when initializing the tool:
- `smtp_server`: The SMTP server to use (string).
- `smtp_port`: The SMTP port to use (integer).
- `from_email`: The sender's email address (string).
- `from_password`: The password for the sender's email account (string).

You also need to provide the following inputs when calling the `forward` method:
- `subject`: The subject of the email (string).
- `body`: The body content of the email (string).
- `to_email`: The recipient's email address (string).

The `forward` method returns a string indicating whether the email was sent successfully or not. In case of an error, it provides a message with the details of the error.