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
            contentType: 'application/json',
            data: JSON.stringify({ user_message: userMessage }),
            success: function(response) {
                if (response.imageUrl) {
                    displayImage(response.imageUrl);
                }
                if (response.message) {
                    displayMessage('bot', response.message);
                }
            },
            error: function(error) {
                console.log("Error: ", error);
            }
        });
    });

    // Function to display messages in the chat box
    function displayMessage(sender, message) {
        var messageClass = (sender === 'user') ? 'user-message' : 'bot-response';
        var messageElement = $('<div>', { class: messageClass });
        messageElement.text(message);
        $('#chat-box').append(messageElement);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    }

    // Function to display images in the chat box
    function displayImage(imageUrl) {
        var imageElement = $('<img>', { src: imageUrl, class: 'chat-image' });
        $('#chat-box').append(imageElement);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    }

    // Additional existing functionality
    $('#new-session-btn').click(function() {
        var confirmedNewSession = confirm('Are you sure you want to start a new session?');
        if (confirmedNewSession) {
            $.ajax({
                url: '/start-new-session',
                type: 'POST',
                data: { previous_session_id: '{{ session.get("session_id") }}' },
                success: function(response) {
                    $('#chat-box').empty();
                },
                error: function(error) {
                    console.log("Error: ", error);
                }
            });
        }
    });

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
                console.log("Error: ", error);
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
                                data: JSON.stringify({ user_message: userMessage, conversation_history: conversationHistory.join('\n') }),
                                contentType: 'application/json',
                                success: function(response) {
                                    conversationHistory.push(`Assistant: ${response.message}`);
                                    displayMessage('bot', response.message);
                                },
                                error: function(error) {
                                    console.log("Error: ", error);
                                }
                            });
                        });
                    },
                    error: function(error) {
                        console.log("Error: ", error);
                    }
                });
            },
            error: function(error) {
                console.log("Error: ", error);
            }
        });
    }
});
