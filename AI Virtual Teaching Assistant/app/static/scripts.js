$(document).ready(function() {

    // Function to handle form submission
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        var userMessage = $('#user-input').val();
        
        displayMessage('user', userMessage);

        $('#user-input').val('');

        // AJAX request to send message to server
        $.ajax({
            url: '/api/chat',
            type: 'POST',
            data: { user_message: userMessage },
            success: function(response) {
                displayMessage('bot', response.bot_response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    // Function to display messages in the chat box
   // Function to display messages in the chat box
function displayMessage(sender, message) {
    var messageClass = (sender === 'user') ? 'user-message' : 'bot-response';
    var messageElement = $('<li>', { class: messageClass });
        $('#chat-box').append(messageElement);
   
    if (sender === 'bot' && message.startsWith('http')) { // Check if the message is a URL
    var imageElement = $('<img>', { src: message, alt: 'Image from Bot', style: 'max-width: 100%;' });
    messageElement.append(imageElement);
    }
    if (sender === 'bot') {
            typeMessage(messageElement, message);
    } else {
            messageElement.html(marked.parse(message));
    }
    console.log($('#chat-box')[0]); // Check what this returns
    $('hashtag#chat-box').append(messageElement);
    $('hashtag#chat-box').scrollTop($('hashtag#chat-box')[0].scrollHeight);
   }

            // Function to simulate typing effect
    function typeMessage(messageElement, message) {
        var currentText = '';
        var messageHTML = marked.parse(message);

        var typeInterval = setInterval(function() {
            if (currentText === messageHTML) {
                clearInterval(typeInterval);
                return;
            }

            currentText = messageHTML.substring(0, currentText.length + 1);
            messageElement.html(currentText);
        }, 5); 
    }

    //Function to display messages in the chat box

    function displayMessage(sender, message) {
        var messageClass = (sender === 'user')? 'user-message' : 'bot-response';
        var messageElement = $('<li>', { class: messageClass, html: marked.parse(message) });
        $('#chat-box').append(messageElement);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    }

    $('#new-session-btn').click(function() {
        var confirmedNewSession = confirm('Are you sure you want to start a new session? ');
        if (confirmedNewSession) {
            $.ajax({
                url: '/start-new-session',
                type: 'POST',
                data: { previous_session_id: '{{ session.get("session_id") }}' },
                success: function(response) {
                    
                    $('#chat-box').empty();
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

    // Function to handle view history button click
    $('#view-history-btn').click(function() {
        $.ajax({
            url: '/chat-history',
            type: 'GET',
            success: function(data) {
                
                $('#chat-sessions').empty();
            
                const sessionGroups = {};
                for (const entry of data.chat_history) {
                    const sessionId = entry.session_id;
                    if (!sessionGroups[sessionId]) {
                        sessionGroups[sessionId] = [];
                    }
                    sessionGroups[sessionId].push(entry);
                }
            
                
                for (const sessionId in sessionGroups) {
                    const sessionContainer = $('<div>', { class: 'chat-session' });
                    const sessionHeader = $('<h3>', { text: `Session ID: ${sessionId}` });
                    sessionContainer.append(sessionHeader);
            
                    
                    for (const entry of sessionGroups[sessionId]) {
                        const messageClass = entry.message.startsWith('Human:') ? 'user-message' : 'bot-response';
                        const messageText = entry.message.split(': ')[1];
                        const messageElement = $('<li>', { class: messageClass, text: messageText });
                        sessionContainer.append(messageElement);
                    }
            
                    $('#chat-sessions').append(sessionContainer);
                }
            
                
                $('.chat-session').click(function() {
                    const sessionId = $(this).find('h3').text().split(':')[1].trim();
                    resumeSession(sessionId);
                });
            
                $('#chat-history-modal').show();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.close-btn').click(function() {
        $('#chat-history-modal').hide();
    });


    $(window).click(function(event) {
        if ($(event.target).parents('#chat-history-modal').length === 0) {
            $('#chat-history-modal').hide();
        }
    });

    // Function to resume a session
    function resumeSession(sessionId) {
        $('#chat-box').empty();
    
        $.ajax({
            url: '/get-conversation-history',
            type: 'POST',
            data: { session_id: sessionId },
            success: function(data) {
                const conversationHistory = data.conversation_history;
    
                for (const message of conversationHistory) {
                    const messageClass = message.startsWith('Human:') ? 'user-message' : 'bot-response';
                    const messageElement = $('<li>', { class: messageClass, html: marked.parse(message.substr(7)) });
                    $('#chat-box').append(messageElement);
                }
    
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
        
        $('#chat-history-modal').hide();
    
        $.ajax({
            url: '/start-new-session',
            type: 'POST',
            data: { previous_session_id: sessionId },
            success: function(response) {
                
                $('#chat-form').off('submit').submit(function(event) {
                    event.preventDefault();
                    var userMessage = $('#user-input').val();

                    displayMessage('user', userMessage);

                    $('#user-input').val('');

                    conversationHistory.push(`Human: ${userMessage}`);

                    $.ajax({
                        url: '/api/chat',
                        type: 'POST',
                        data: { user_message: userMessage, conversation_history: conversationHistory.join('\n') },
                        success: function(response) {
                            
                            conversationHistory.push(`Assistant: ${response.bot_response}`);

                            displayMessage('bot', response.bot_response);
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    },
    error: function(error) {
        console.log(error);
    }
});
    }

});