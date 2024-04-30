$(document).ready(function() {
    // Function to handle form submission
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        var userMessage = $('#user-input').val();
        
        // Display user message with user label
        $('#chat-box').append('<div class="message user-message">User: ' + userMessage + '</div>');
        
        // Clear input field
        $('#user-input').val('');
        
        // Scroll to bottom of chat box
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
        
        // AJAX request to send message to server
        $.ajax({
            url: '/api/chat',
            type: 'POST',
            data: { user_message: userMessage },
            success: function(response) {
                // Display bot response with AI_TA label
                $('#chat-box').append('<div class="message bot-response">AI_TA: ' + response.bot_response + '</div>');
                // Scroll to bottom of chat box
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
