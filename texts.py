from twilio.rest import Client
import random

# Twilio account info
account_sid = '***'
auth_token = '***'
client = Client(account_sid, auth_token)
twilio_number = '+12762262715'

# Numbers of recipients
n_num = '+919352939475'
l_num = '+919080356802'
d_num = '+918905959835'
command_numbers = [d_num]

# Function to send a custom message to recipients
def send_message(body):
    for num in command_numbers:
        message = client.messages.create(
            body=body,
            from_=twilio_number,
            to=num
        )
    print(message.sid)

def create_code():
    code = 0
    for _ in range(0, 6):
        code = code * 10 + random.randint(0, 9)
    return int(code)

def main():
    code = create_code()  # Add parentheses to call the function
    send_message("Enter the following code to cancel auto-launch sequence: " + str(code))

# Run main function
main()
