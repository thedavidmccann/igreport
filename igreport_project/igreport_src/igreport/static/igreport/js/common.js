$(function() {
	$('#logout').click(function() {
		$.post('/logout', $(this).parents('li').find('form').serialize(), function() {
			window.location = '/';
		});
	});
})