import smtplib
from smolagents import Tool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSMTPTool(Tool):
    """
    This class is a tool for an AI agent to send emails using SMTP.
    """
    name = "email_smtp"
    description = "Sends an email using SMTP"
    inputs = {
        "subject": {
            "type": "string",
            "description": "The subject of the email"
        },
        "body": {
            "type": "string",
            "description": "The body content of the email"
        },
        "to_email": {
            "type": "string",
            "description": "The recipient email address"
        }
    }
    output_type = "string"

    def __init__(self, smtp_server, smtp_port, from_email, from_password):
        """
        Initialize the tool with the necessary parameters.

        Args:
            smtp_server: The SMTP server to use.
            smtp_port: The SMTP port to use.
            from_email: The sender email address.
            from_password: The password for the sender email account.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.from_password = from_password
        self.is_initialized = True  # Make sure this is set to True! VERY IMPORTANT!

    def forward(self, subject: str, body: str, to_email: str) -> str:
        """
        Sends an email using SMTP.

        Args:
            subject: The subject of the email.
            body: The body content of the email.
            to_email: The recipient email address.

        Returns:
            A string indicating whether the email was sent successfully.
        """
        try:
            # Create a MIME object
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(body, 'plain'))

            # Setup the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()

            # Login to the email account
            server.login(self.from_email, self.from_password)

            # Send the email
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)

            # Terminate the SMTP session
            server.quit()

            return "Email sent successfully."

        except Exception as e:
            return f"Failed to send email. Error: {e}"