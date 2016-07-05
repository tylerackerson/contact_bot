IPM = {

  start: function (user_name) {

    var $chatWindow = $('#messages');
    var accessManager;
    var messagingClient;
    var generalChannel;
    var username = user_name;

    // Helper function to print info messages to the chat window
    function print(infoMessage, asHtml) {
        var $msg = $('<div class="info">');
        if (asHtml) {
            $msg.html(infoMessage);
        } else {
            $msg.text(infoMessage);
        }
        $chatWindow.append($msg);
    }

    // Helper function to print chat message to the chat window
    function printMessage(fromUser, message) {
        debugger;
        var $user = $('<span class="username">').text(fromUser + ':');
        if (fromUser === username) {
            $user.addClass('me');
        }
        var $message = $('<span class="message">').text(message);
        var $container = $('<div class="message-container">');
        $container.append($user).append($message);
        $chatWindow.append($container);
        $chatWindow.scrollTop($chatWindow[0].scrollHeight);
    }

    $.getJSON('/token', {
        identity: username,
        device: 'browser'
    }, function(data) {

        print('Starting chat...');

        accessManager = new Twilio.AccessManager(data.token);
        messagingClient = new Twilio.IPMessaging.Client(accessManager);

        var channelName = 'chat-' + username;
        var promise = messagingClient.getChannelByUniqueName(channelName);

        promise.then(function(channel) {
            generalChannel = channel;
            if (!generalChannel) {
                messagingClient.createChannel({
                    uniqueName: channelName,
                    friendlyName: channelName
                }).then(function(channel) {
                    console.log('Created channel:' );
                    console.log(channel);

                    generalChannel = channel;
                    setupChannel();
                });
            } else {
                console.log('Found channel:');
                console.log(generalChannel);
                setupChannel();
            }
        });
    });

    function setupChannel() {
        generalChannel.join().then(function(channel) {
            print('Joined chat as '
                + '<span class="me">' + username + '</span>.', true);
        });

        // Listen for new messages sent to the channel
        generalChannel.on('messageAdded', function(message) {
          var ipm_channel = this.sid;

          $.post('/incoming', {
            user: message.author,
            message: message.body,
            ipm_channel: ipm_channel,
          });

          printMessage(message.author, message.body);
        });
    }

    // Send a new message to the general channel
    var $input = $('#chat-input');
    $input.on('keydown', function(e) {
        if (e.keyCode == 13) {
            generalChannel.sendMessage($input.val())
            $input.val('');
        }
    });
  }
}