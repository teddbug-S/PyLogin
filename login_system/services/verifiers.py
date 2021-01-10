from enum import Enum, unique
from email.message import EmailMessage
import smtplib, socket


@unique
class VerifyInfo(Enum):
    SUCCESS = 1
    CONNECTION_FAILED = 2
    CONNECTION_TIMED_OUT = 3


class Action(Enum):
    VERIFY         =   0
    AUTHENTICATE   =   1


class Verify():
    """
    A subclass of the Email Message to facilitate email services
    """
    def __init__(self, action) -> None:
        super().__init__()
        self.EMAIL_ADDRESS = "" # pylogin email, currently not available you can use yours
        self.PASSWORD = "" # your email password
        self.action = action

    def _get_body_html(self):
        """
        Generates an HTML message body
        """
        bodies = (
        """\
        <!DOCTYPE html>
        <html>
            <body>
               <header>
                    <h1 style = "color:blue;">Verify your email account.✔</h1>
                    <p style="font-size: 14px;">Hey {username}, you created an account on <span style="color:green;">
                    <a href="https://github.com/Unicorn-Code-Inc/PyLogin">PyLogin 🐍</a></span>.
                    Please verify your email💌 to enable others to see👀 you.</p>
                <article>
                    <p style="font-size: 14px;">Your token is: <span style="font-size:18px;"><b>{token}</b></span>
                </article>
                <footer>
                    <p>Thank You! ❤💞
                    <p>Unicorn Code Inc.<br/>&copy; 2021</p>
                </footer>
            </body>
        </html>
        """,
        """\
        <!DOCTYPE html>
        <html>
            <body>
                <header>
                    <h1 style="color:purple;">PyLogin 🐍</h1>.
                      <hr/>
                      <h2 style="color:blue;">Authenticate action.🔐</h2>
                </header>
                <article>
                    <p style="font-size: 14px"> Seems like you want to delete  <span style="color:aqua;">{username}</span>  from the database but first you
                    need to authenticate the action by using the token below.</p>
                    <p style="font-size: 14px">Your token is:  <span style="font-size:18px;"><b>{token}</b></span></p>
                    <a style="color:green", href="https://github.com/Unicorn-Code-Inc/PyLogin">
                    Learn why you need to authenticate this action</a>
                </article>
                <footer>
                    <p>Thank You! ❤💞
                    <p>Unicorn Code Inc.<br/>&copy; 2021</p>
                </footer>
            </body>
        </html>
        """
        )
        return bodies[self.action.value] # get body based on action value

    
    def _get_body(self):
        """
        Generates a plain text body
        """
        bodies = (
            """
            VERIFY YOUR ACCOUNT!✅
            =========+++========
            
            Hey {username}, you created an account on PyLogin please verify your
            email to enable others to see you.

            Your token is🔐:   {token}


            ⚠ NOTE ⚠: Do not share this message or the token with anyone.

            Thank You!💖💞

            Unicorn Code Inc
            © 2021
            """,
            """
            AUTHENTICATE ACTION ✅
           !=======++⚡⚡++=======!
            
            Hello {username}, seems like you want to perform an administrative action
            on users in PyLogin, please for security reasons we want you to authenticate your
            email to be able to carry on with the process.

            Your token is🔐:   {token}


            ⚠ NOTE ⚠: Do not share this message or the token with anyone.

            Thank You!💖💞

            Unicorn Code Inc
            © 2021
            """
        )
        return bodies[self.action.value]

    
    def generate_message(self, *, to, token, username,):
        """
        Generates an email message
        """
        msg = EmailMessage()
        # choose a subject for the message
        subject = "Get Authenticated!" if self.action.value == 1 else "Let Them Know You're Legit."
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = self.EMAIL_ADDRESS
        msg.set_content(self._get_body().format(token=token, username=username)) # body raw text
        # add alternative body html
        msg.add_alternative(self._get_body_html().format(token=token, username=username), subtype='html')
        return msg

    
    def send_message(self, msg):
        """
        Sends the generated email message using the smtp_ssl method.
        """
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com') as smtp: # ssl smtp
                smtp.login(self.EMAIL_ADDRESS, self.PASSWORD) # login
                smtp.send_message(msg) # try to send the message

        # catch some errors
        except smtplib.SMTPConnectError:
            return VerifyInfo.CONNECTION_FAILED
        except socket.gaierror:
            return VerifyInfo.CONNECTION_FAILED
        except socket.timeout:
            return VerifyInfo.CONNECTION_TIMED_OUT
        else:
            return VerifyInfo.SUCCESS
