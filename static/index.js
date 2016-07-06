IPM = {

  start: function (user_name) {

    var $chatWindow = $('#messages');
    var accessManager;
    var messagingClient;
    var generalChannel;
    var username = user_name;

    function print(infoMessage, asHtml) {
      var $msg = $('<div class="info">');
      var $waiting = $('<div class="waiting starting">')
      if (asHtml) {
        $msg.html(infoMessage);
      } else {
        $msg.addClass('starting')
        $msg.text(infoMessage);
        $chatWindow.append($waiting);
      }

      $chatWindow.append($msg);
    }

    function printMessage(fromUser, message) {
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
        $('.info, .waiting').removeClass('starting');
        $('#chat-input').prop('disabled', false);

        print('Joined chat as ' + '<span class="me">' + username + '</span>.', true);
      });

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

    var $input = $('#chat-input');
    $input.on('keydown', function(e) {
      if (e.keyCode == 13) {
        generalChannel.sendMessage($input.val())
        $input.val('');
      }
    });
  }
}