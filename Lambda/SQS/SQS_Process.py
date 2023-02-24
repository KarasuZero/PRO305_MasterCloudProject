import json
import smtplib
from email.message import EmailMessage

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # get the record
    records = event['Records']

    # smtp stuff
    sender = "citlalli.macgyver@ethereal.email"
    password = "9nH1pz8mzaFs4u4UhZ"

    msg = EmailMessage()

    for record in records:
        body = record['body']
        # split the body with :
        body_split = body.split(':')

        # grab attributes
        email = body_split[0]
        subject = body_split[1]
        message = body_split[2]

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        msg.set_content(message)

        print("connecting to smtp server\n")

        try:
            with smtplib.SMTP("smtp.ethereal.email", 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sender, password)

                smtp.send_message(msg)
                print("email sent\n")

        except Exception as e:
            print("could not send email\n")
            print("Error: " + e)


