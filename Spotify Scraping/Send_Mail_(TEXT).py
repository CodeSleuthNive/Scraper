import smtplib
import warnings
import traceback
warnings.filterwarnings("ignore")
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart


def send_mail_alert(subject, output, sender_email, sender_password, recipient_emails):
    """
    Sends an email alert with filtered data.

    This function sends an email with the provided filtered data to the specified recipients.

    Args:
        subject (str): The subject of the email.
        output (str): The output content to include in the email.
        sender_email (str): The sender's email address (e.g., 'your_email@gmail.com').
        sender_password (str): The sender's email account password.
        recipient_emails (list of str): A list of recipient email addresses to send the email to.

    Raises:
        smtplib.SMTPException: If there is an issue with the SMTP server or sending the email.
    """
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipient_emails)
        msg['Subject'] = subject

        # Add the filtered data to the email body
        body = output
        msg.attach(MIMEText(body, 'plain'))

        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login with sender's credentials
        server.login(sender_email, sender_password)

        # Send the message to all recipients
        text = msg.as_string()
        server.sendmail(sender_email, recipient_emails, text)

        # Close the SMTP session
        server.quit()

        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print("An error occurred while sending the email:", e)
        traceback.print_exc()
        raise e