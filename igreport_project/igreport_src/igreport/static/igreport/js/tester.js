var refreshUrl = '';

$(function() {
	reloadMessages();
	var d = new Date();
	$('#button-test-message').click(sendMessage);
	refreshMesageInterval = setInterval(loadMessages, 5000);
	
	$('#messages span a').click(reloadMessages);
});

function reloadMessages() {
	var d = new Date();
	sender = $('*[name="sender"]').val();
	refreshUrl = '/messages/' + sender + '/' + d.getFullYear() + '/' + pad(d.getMonth()) + '/' + pad(d.getDate()) + '/' + pad(d.getHours()) + '/' +
        pad(d.getMinutes()) + '/' + pad(d.getSeconds()) + '/';
	$('#messages p').load(refreshUrl);
}

function sendMessage() {
	// create a dummy message while waiting for the refresh from the DB
	$('#messages p span').remove();
	messageLi = $('<li/>').addClass('incoming');
	messageLabel = $('<div/>').addClass('alert alert-info');
	messageLi.append(messageLabel);
	messageLabel.text($('*[name="message"]').val());
	$('#messages ul').append(messageLi);
	
	// disable the button to avoid double-sending a message
	$('#button-test-message').attr('disabled', 'disabled');
	

	params = $('#form-test-message').serialize();
	// clear the input field
	$('*[name="message"]').val('');
	
	// send the message to the router
	$.get('/router/receive/', params);
	
}

function loadMessages() {
	// advance script progress
	$.get('/test/progress/', '', function() {
		
		// load the messages
		$('#messages p').load(refreshUrl);
		
		// re-enable the button, if necessary
		$('#button-test-message').removeAttr('disabled');
	});
}

function pad(s) {
	s = "0" + s;
	return s.substring(s.length - 2);
}