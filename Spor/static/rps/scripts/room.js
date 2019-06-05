    var chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/game/' + roomName + '/');
    var username = "{{request.user.username}}";



    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        //var message = data.message + " via " + data.username + "winner:" + data.winner;
       // var winner = data.winner
        console.log(data.message)

        if (data.message=="closed") {
             document.querySelector('#winner').textContent = "Sorry... This  game is completed.  Redirecting to lobby";
             document.getElementById('chat-message-rock').style.visibility = 'hidden';
             document.getElementById('chat-message-scissors').style.visibility = 'hidden';
             document.getElementById('chat-message-paper').style.visibility = 'hidden';
             setTimeout(3000);
             document.location.replace("http://127.0.0.1:8000/");
        }
        else if (data.result != "tai") {
            if (data.winner != "") {
                if (username == data.winner) {
                    document.querySelector('#winner').textContent = "You WIN!";
                } else {
                    document.querySelector('#winner').textContent = "You LOSE!";
                }
            }
        } else {
            document.querySelector('#winner').textContent = "You opponent is a genius like you...Try again!\n Waiting for opponent choice...";
            document.getElementById('chat-message-rock').style.visibility = 'visible';
            document.getElementById('chat-message-scissors').style.visibility = 'visible';
            document.getElementById('chat-message-paper').style.visibility = 'visible';

        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        //document.location.replace("http://127.0.0.1:8000/lobby");
    };



    document.querySelector('#chat-message-rock').onclick = function(e) {

        var message = "rock"
        chatSocket.send(JSON.stringify({
            'message': message,
        }));
        document.getElementById('chat-message-rock').style.visibility='hidden';
        document.getElementById('chat-message-scissors').style.visibility='hidden';
        document.getElementById('chat-message-paper').style.visibility='hidden';

    };

     document.querySelector('#chat-message-scissors').onclick = function(e) {

        var message = "scissors"
        chatSocket.send(JSON.stringify({
            'message': message,

        }));
       document.getElementById('chat-message-rock').style.visibility='hidden';
        document.getElementById('chat-message-scissors').style.visibility='hidden';
        document.getElementById('chat-message-paper').style.visibility='hidden';

    };

      document.querySelector('#chat-message-paper').onclick = function(e) {

        var message = "paper"
        chatSocket.send(JSON.stringify({
            'message': message,

        }));
        document.getElementById('chat-message-rock').style.visibility='hidden';
        document.getElementById('chat-message-scissors').style.visibility='hidden';
        document.getElementById('chat-message-paper').style.visibility='hidden';

    };