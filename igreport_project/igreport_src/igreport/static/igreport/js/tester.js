var refreshUrl = '';

$(function() {
	reloadMessages();
	var d = new Date();
	$('#button-test-message').click(sendMessage);
	refreshMessageInterval = setInterval(advanceProgress, 1000);
	$('#messages span a').click(reloadMessages);
});

function reloadMessages() {
	var d = new Date();
	sender = $('*[name="sender"]').val();
	refreshUrl = '/messages/' + sender + '/' + d.getFullYear() + '/' + pad(d.getMonth()) + '/' + pad(d.getDate()) + '/' + pad(d.getHours()) + '/' +
        pad(d.getMinutes()) + '/' + pad(d.getSeconds()) + '/';
	$('#messages p').load(refreshUrl + '' + new Date().getTime() + '/');
}

function loadMessages() {
	// load the messages
	$('#messages p').load(refreshUrl + '' + new Date().getTime() + '/');
	
	// re-enable the button, if necessary
	$('#button-test-message').removeAttr('disabled');
	
	return true;
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

function advanceProgress() {
	// advance script progress
	$.post('/test/progress/' + new Date().getTime() + '/', $('*[name="csrfmiddlewaretoken"]').serialize(), loadMessages);
	return true;
}



function pad(s) {
	s = "0" + s;
	return s.substring(s.length - 2);
}