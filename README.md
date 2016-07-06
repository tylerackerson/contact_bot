# Contact
Contact uses Twilio and Slack to facilitate communication between two users. Messages are created from a chat interface using Twilio IP Messaging and are routed to the owner in Slack to respond. The owner can respond to the user directly from Slack, and the response will appear for the user in their chat window.

**Primary use case:** (implemented)
  - I want users to be able to chat with me from the site
  - I want to facilitate my end of the chat via Slack
  - Respond to users using "/respond [message]" slash-command

**Secondary use case:** (not yet implemented)
  - Users could ask that I connect with them via text/SMS
  - I still want to facilitate my end of the conversation via slack
  - Could be a "/sms [message]" slash-command

# Usage
### Set up environment variables
1. Copy `config.env.example` and rename it `config.env`
2. Fill in all the environment variables

### Start the app
1. virtualenv contact_bot
2. source contact_bot/bin/activate
3. . ./config.env
4. python app.py
5. Go to localhost:3000

### Start the contact bot app
1. virtualenv contact_bot
2. source contact_bot/bin/activate
3. . ./config.env
4. python contact_bot.py