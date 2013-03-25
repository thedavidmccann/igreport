//
function jqpopup(title, btns, w, h) {
	buttons = {};

	if (btns) {
		for(var i=0; i<btns.length; i++) {
			buttons['b'+i] = {text:btns[i].text, click:btns[i].click};
		}
	}

	buttons['Cancel'] = function() { $(this).dialog('destroy'); };

        try {
                var d = $('#jqpopup').dialog({
                        autoOpen: false,
			modal: true,
			minHeight: h,
			minWidth: w,
			title: title,
			closeOnEscape: false,
                        buttons: buttons,
                 });
                d.dialog('open');
		d.dialog('option', 'position', "center");

        } catch(a) {alert(a);}
	
	return false;
};

function editrpt(rid) {
	
	ajax_wait('Getting Report Information ..');
//
	var url = '/igreports/' + rid + '/getreport/';
	var r = createHttpRequest();
	r.open('GET', url, true);
	
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			if(r.status != 200) {
				alert(r.responseText);
				return;
			}
			if(/{error:false/.test(r.responseText)) {
				var o = eval('('+ r.responseText +')');
				var rpt = o.res.rpt;
				var dist = o.res.dist;
				//var scty = o.res.scty;
				var cat = o.res.cat;
				var comm = o.res.comm;
				
				var doptions = '';
				for(var i=0; i<dist.length; i++) {
					doptions += '<option value="'+dist[i].id+'"'+(dist[i].id==rpt.district_id?' selected="selected"':'')+'>'+dist[i].name+'</option>';
				}
				var cathtml = '';
				if(cat.length) {
					for(var i=0; i<cat.length; i++) {
						cathtml += '<div style="padding-bottom:3px"><input type="checkbox" id="cat_'+cat[i].id+'" name="category" value="'+cat[i].id+'"'+(cat[i].checked?' checked="checked"':'')+'/>&nbsp;<label class="rpt-option-label" for="cat_'+cat[i].id+'">'+cat[i].name+'</label></div>';
					}
				}
				if(!cathtml) {
					cathtml = '<h3>[No Report Categories Configured]</h3>';
				} else {
					cathtml = '<div style="border:solid #ccc 1px;height:70px;overflow:auto;padding:10px">'+cathtml+'</div>';
				}
				var comments = '';
				if(comm.length>0) {
					for(var i=0; i<comm.length; i++) {
						comments += '<div style="padding-top:7px">#'+(i+1)+'.&nbsp;'+comm[i].comment+' by <strong>'+comm[i].user+
						'</strong> on <strong>'+comm[i].date+'</strong></div>';
					}
					comments = '<div style="padding-top:5px"><strong>Current Comments</strong>:<br/>'+comments+'</div>';
				}
				var html = '<div class="report"><form id="rptform"><table border="0" cellpadding="0" cellspacing="0"><tr><td colspan="2"><div class="rpt-title">Submitted by <span style="color:#ff6600;font-weight:bold">'+rpt.sender+'</span> on <span style="color:#ff6600;font-weight:bold">'+rpt.date+'</span></div></td></tr><tr><td><div class="rpt-label">Report</div><div><textarea id="report" name="report" class="rpt-ta">'+rpt.report+'</textarea></div></td><td><div class="rpt-label">Accused</div><div><textarea id="subject" name="subject" class="rpt-ta">'+rpt.accused+'</textarea></div></td></tr><tr><td><div class="rpt-label">District</div><div><select id="dist" name="district" class="rpt-list">'+doptions+'</select><br/>(User reported: <span style="color:#CC0000">'+rpt.district_ff+'</span>)</div></td><td><div class="rpt-label">Amount</div><div><input type="text" id="amount" name="amount" value="'+rpt.amount+'" /><br/>(User reported: '+rpt.amount_ff+')</div></td></tr><tr><td><div class="rpt-label">Name of Reporter</div><div><textarea id="names" name="names" class="rpt-ta">'+rpt.names+'</textarea></div></td><td><div class="rpt-label">Case Category</div><div>'+cathtml+'</div></td></tr><tr><td><div class="rpt-label">Comments</div><div><textarea id="comments" name="comments" class="rpt-ta"></textarea><input type="hidden" name="id" value="'+rid+'" /><input type="hidden" name="csrfmiddlewaretoken" value="'+getCookie('csrftoken')+'" /></div></td><td>'+comments+'</td></tr></table></form></div>';
				
				var title = 'User Report Details';
				var btns = [{text:'Submit', click:function(){ update_rpt(rid); }}]
				
				document.getElementById('jqpopup').innerHTML = html;
				jqpopup(title, btns, 850, 450);
				
				//$.datepicker.setDefaults({ dateFormat: 'mm/dd/yy' });
				//$("#date").datepicker();
			}
		}
	}
	r.send(null);	
};

function update_rpt(rid) {

	var params = $('#rptform').serialize();
	ajax_wait('Updating Report. Please wait ..');
        var r = createHttpRequest();
	
        r.open('POST', '/igreports/' + rid + '/', true);
        r.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
        r.onreadystatechange = function(){
                if(r.readyState == 4){
			ajax_done();
			if(r.status != 200) {
				//alert(r.statusText);
				alert(r.responseText);
				return;
			}
			// success reload page
			$('#jqpopup').dialog('close');
			ajax_wait_update('Report updated. Refreshing ..')
			window.location.replace(window.location);
		}
	}
	r.send(params);
	
	return true;	
};

function syncit(rid) {
	//if(!confirm('Sync Report?')) {
	//	return;
	//}
	ajax_wait('Syncing Report. Please wait ..');
	
	var r = createHttpRequest();
        r.open('POST', '/igreports/' + rid + '/sync/', true);
        r.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			if(r.status != 200) {
				alert(r.responseText);
				return;
			}
			alert('Report Successfuly synced');
			window.location.replace(window.location);
		}
	}
	r.send('csrfmiddlewaretoken='+getCookie('csrftoken'));
}

function smsp(id, msisdn) {
	
	var title = 'Send SMS to ' + msisdn;
	var btns = [{text:'Send SMS', click:function(){ send_(); }}]
	var txt = document.getElementById('rpt_' + id).innerHTML;
	
	var html = '<form id="msgf"><div style="padding:30px 0px 0px 30px">\
	    <div class="rpt-label">User Report</div><div style="padding-bottom:20px">' + txt + '</div>\
	    <div class="rpt-label">SMS Message</div><div><textarea name="message" rows="5" cols="50" class="rpt-ta-general" onkeydown="track_msg_len(this)" onkeyup="track_msg_len(this)"></textarea><br/>\
	    <input type="text" size="10" id="id_chars" readonly="readonly" value="0 Chars" style="color:#666" />\
	    <input type="hidden" name="id" value="'+id+'" /><input type="hidden" name="msisdn" value="'+msisdn+'" />\
	    </div>\
	</div></form>';				
	document.getElementById('jqpopup').innerHTML = html;
	jqpopup(title, btns, 600, 300);	
};

function send_() {
	var f = document.getElementById('msgf');
	if(f.message.value.length < 2) {
		alert('Specify a valid message to send');
		return;
	}
	ajax_wait('Sending SMS to ' + f.msisdn.value + '. Please wait ..');
	
	var r = createHttpRequest();
        r.open('POST', '/igreports/' + f.id.value + '/sms/', true);
        r.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			if(r.status != 200) {
				alert(r.responseText);
				return;
			}
			alert('SMS Successfuly sent to ' + f.msisdn.value);
			$('#jqpopup').dialog('destroy');
			//window.location.replace(window.location);
		}
	}
	r.send('text='+encodeURIComponent(f.message.value)+'&csrfmiddlewaretoken='+getCookie('csrftoken'));	
}

function rptsetc() {
	//alert('setting color!');
};

function track_msg_len(f) {
	var limit = 160;
	if(f.value.length == 0) {
		document.getElementById('id_chars').value = '0 Chars';
		return;
	}
	if(f.value.length > limit) {
		f.value = (f.value).substr(0, limit);
		document.getElementById('id_chars').value = limit + ' Chars';
	}
	document.getElementById('id_chars').value = f.value.length + ' Chars';
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
