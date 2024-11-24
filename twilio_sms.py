from twilio.rest import Client


# account_sid = 'ACb4c3162a42cb3fa401e8e1f3b5ccef7b'
# auth_token = '9a7bccfbce611c140fdf55371843b3b6'
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     body='Hello Rider, Please wear Helmet While riding your vehicle',
#   to='+918660349500'
# )

# print(message.sid)

from twilio.rest import Client

# Your Twilio account credentials
account_sid = 'ACb4c3162a42cb3fa401e8e1f3b5ccef7b'
auth_token = '9a7bccfbce611c140fdf55371843b3b6'

client = Client(account_sid, auth_token)

sender_number = '+18506417136'
recipient_number = '+918660349500'

# Your message content
message_body = 'Hello Rider, Kindly waer your helmet while riding the bike'

try:
    # Send the SMS
    message = client.messages.create(
        body=message_body,
        from_=sender_number,
        to=recipient_number
    )
    print("SMS sent successfully!")
    print("Message SID:", message.sid)
except Exception as e:
    print("Error:", e)