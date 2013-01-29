$(function() {
	loadReports();
	$('#subcounty').load('/subcounties/');
	$('#district').load('/districts/');
	$('#category').load('/categories/');
	$('#whendatetime').datepicker();
	$('#save').click(save);
	$('#cancel').click(clearEditRow);
	$('ul.nav a').click(filter);
	
});

function filter() {
	filter = $(this).data('filter');
	$('ul.nav li').removeClass('active');
	$(this).parents('li').addClass('active');
	$('#content tbody').load('/igreports/?filter=' + filter, '', function() {
		$('.edit-btn').click(edit);
		$('.sync-btn').click(sync);
	});
}

function loadReports() {
	$('#content tbody').load('/igreports/', '', function() {
		$('.edit-btn').click(edit);
		$('.sync-btn').click(sync);
	});
}

function clearEditRow() {
    $('#editForm form')[0].reset();
   
    if ($('#editFormRow').length) {
        $('#editForm').hide();
        $('#content').after($('#editForm'));
        $('#editFormRow').remove();
    }
}

function save() {
	params = $('#editForm form').serialize();
	id = $('*[name="id"]').val();
	clearEditRow();
	$.post('/igreports/' + id + '/' , params, loadReports);
}

function sync() {
        csrf = $('input[name="csrfmiddlewaretoken"]').val();
	id = $(this).parents('tr').find('*[name="data"]').data('id');
	$.post('/igreports/' + id + '/sync/', 'csrfmiddlewaretoken='+csrf, loadReports);
}

function edit() {
	formData = $(this).parents('tr').find('*[name="data"]').data();
    for (key in formData) {
        $('#editForm *[name="' + key + '"]').val('' + formData[key]);
        $('span[id="' + key + '"]').text(formData[key])
    }
    colSpan = $('#content tbody tr').first().find('td').length;
    $(this).parents('tr').after('<tr id="editFormRow"><td colspan="' + colSpan + '"></td></tr>');
    comments = $(this).parents('tr').find('.row-comments').clone();
    $('#comments').append(comments);
    $('#comments .row-comments').show();
    $('#editFormRow td').append($('#editForm'));
    $('#editForm').show(100);

}
