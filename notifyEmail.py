import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "jamesmorritttest@gamil.com"
password = "T3sttest"

def complete(receiver_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Image stitching complete"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
            Hi,
            Your image set has finished being processed.
            It can be seen at http://localhost:8000/dashboard/"""

    html = """\
            <html>
              <body>
                <p>Hi, <br>
                 Your image set has finished being processed.<br>
                 It can be found <a href="http://localhost:8000/dashboard/">here</a>
                </p>
              </body>
            </html>
        """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

def failure(receiver_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Image stitching has failed"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
            Hi,
            Your image set has failed to complete.
            For more information go to http://localhost:8000/dashboard/"""

    html = """\
            <html>
              <body>
                <p>Hi, <br>
                 Your image set has failed to complete.<br>
                 More information can be found <a href="http://localhost:8000/dashboard/">here</a>
                </p>
              </body>
            </html>
        """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
