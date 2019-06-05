        var isAccept = false;
        var lobbySocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/');


         lobbySocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data.message;
        var dani = data.dani;
        console.log(dani);

        if(message=="accept"){

            var roomName = document.querySelector('#room-name-input').value;
                window.location.pathname = '/game/' + roomName + '/';
        }
        if(message=="deny"){
                document.querySelector('#access').textContent = "The room with this name is already exist..." +
                    "Try something other !";
        }
        if(message=="random"){
            if(data.randomgame != ""){
            window.location.pathname = '/game/' + data.randomgame + '/';}
            else {
                 document.querySelector('#access').textContent = "There are no available games...Sorry";
            }
        }
    };

    lobbySocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };


        document.querySelector('#room-name-input').focus();
        document.querySelector('#room-name-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#room-name-submit').click();
            }
        };

        document.querySelector('#room-name-submit').onclick = function(e) {
            var roomName = document.querySelector('#room-name-input').value;
            lobbySocket.send(JSON.stringify({
                'action': "create",
            'message': roomName

            }));
        };
        document.querySelector('#random-game').onclick = function(e) {
            lobbySocket.send(JSON.stringify({
            'action': "random",
                'message': ""


            }));
        };