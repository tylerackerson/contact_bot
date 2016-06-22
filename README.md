# Contact Bot
Contact Bot will use Twilio and Slack to facilitate communication between two users. Messages will be created from a chat interface using Twilio IP Messaging and will be routed to the owner in Slack to respond. The owner can respond to the user directly from Slack, and the response will appear for the user in their chat window.

**Example use case:**
  - I want users to be able to chat with while they're on my site
  - I want to facilitate my end of the chat via Slack
  - Could be a "/chat [message]" slash-command

**Or:**
  - Users could, from my site, ask that I talk to them via text/SMS
  - I still want to facilitate my end of the conversation via slack
  - Could be a "/sms [message]" slash-command

# Usage
### Set up environment variables
1. Copy `config.env.example` and rename it `config.env`
2. Fill in all the environment variables

### Start the contact bot app
1. virtualenv contact_bot
2. source contact_bot/bin/activate
3. . ./config.env
4. python app.py
5. Go to localhost:3000
6. Start chatting