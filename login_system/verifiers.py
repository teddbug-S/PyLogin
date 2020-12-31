from hmac import compare_digest
import smtplib
from email.message import EmailMessage

from services._crypt import generate_key


EMAIL_ADDRESS = "divinedarkey47@gmail.com"
PASSWORD = "stonebwoy"

def generate_message(receiver, body) -> EmailMessage:
    """
    Generates a message setting the receiver and the body using the 
    EmailMessage from email.message package

    :param receiver: the receiver of te email.
    :type receiver: str
    :param body: the body of the message.
    :type body: str
    :return: an email message
    :rtype: EmailMessage
    """
    msg = EmailMessage()
    msg['To'] = receiver
    msg['From'] = EMAIL_ADDRESS
    msg.set_content(body)
    return msg


def get_body(name, token):
    """ 
    This method generates the body which will be passed to generate_message.
    The body of the message may vary due to the kind of action to perform.
    Actions may be:
      * Verify a user email
      * Verify an admin before a process is completed 

    Action Names:
      * action-verify
      * action-auth

    :param name: name of action to perform
    :type name: str
    """
    bodies = [
        """
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style = "color:blue;">Verify your email</h1>
                <p>Hey {username}, you created an account on <span style="color:green;">
                <a href="https://github.com/Unicorn-Code-Inc/PyLogin">PyLogin</a></span>.
                <br/>
                Please verify your email to enable others to see you.
                </p>
                <p>Your token is: <span style="font-size:18px;">{token}</span>
                <br/>
                <p>Unicorn Code Inc.<br/>&copy; 2020</p>
            </body>
        </html>
        """
    ]