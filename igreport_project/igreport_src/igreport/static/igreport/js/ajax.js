//
function ajax_wait(msg) {
        try { 
                var dialog = $('#waitdlg').dialog({
			closeOnEscape: false,
			open: function(event, ui) {
				$(this).parent().children().children('.ui-dialog-titlebar-close').hide();
			},
                        autoOpen:false, modal:true, minHeight:100, minWidth:500, 'title': 'Processing',
                        });
                dialog.dialog('open');
		document.getElementById('waitmsg').innerHTML = msg;
        } catch(a) {alert(a);}	
};

function ajax_wait_update(msg) {
	document.getElementById('waitmsg').innerHTML = msg;
};

function ajax_done() {
	$('#waitdlg').dialog('close');
	
};

function createHttpRequest(){
        var request;
        try{request = new ActiveXObject("Msxml2.XMLHTTP"); }
        catch(e){
                try{request = new ActiveXObject("Microsoft.XMLHTTP");}
                catch(e){request = new XMLHttpRequest(); }
        }
        return request;
};
