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
				alert(r.statusText);
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
				/*
				var soptions='';
				for(var i=0; i<scty.length; i++) {
					soptions += '<option value="'+scty[i].id+'"'+(scty[i].id==rpt.subcounty_id?' selected="selected"':'')+'>'+scty[i].name+'</option>';
				}*/
				var cathtml = '';
				if(cat.length) {
					for(var i=0; i<cat.length; i++) {
						cathtml += '<div style="padding-bottom:3px"><input type="checkbox" id="cat_'+cat[i].id+'" name="category" value="'+cat[i].id+'"'+(cat[i].checked?' checked="checked"':'')+'/>&nbsp;<label class="rpt-option-label" for="cat_'+cat[i].id+'">'+cat[i].name+'</label></div>';
					}
				}
				if(!cathtml) {
					cathtml = '<h3>[No Report Categories Configured]</h3>';
				}
				var comments = '';
				if(comm.length>0) {
					for(var i=0; i<comm.length; i++) {
						comments += '<div style="padding-top:7px">#'+(i+1)+'.&nbsp;'+comm[i].comment+' by <strong>'+comm[i].user+
						'</strong> on <strong>'+comm[i].date+'</strong></div>';
					}
					comments = '<div style="padding-top:5px"><strong>Current Comments</strong>:<br/>'+comments+'</div>';
				}
				var html = '<div class="report"><form id="rptform"><table border="0" cellpadding="0" cellspacing="0"><tr><td colspan="2"><div class="rpt-title">Submitted by <span style="color:#ff6600;font-weight:bold">'+rpt.sender+'</span> on <span style="color:#ff6600;font-weight:bold">'+rpt.date+'</span></div></td></tr><tr><td><div class="rpt-label">Report</div><div><textarea id="report" name="report" class="rpt-ta">'+rpt.report+'</textarea></div></td><td><div class="rpt-label">Accused</div><div><textarea id="subject" name="subject" class="rpt-ta">'+rpt.accused+'</textarea></div></td></tr><tr><td><div class="rpt-label">Amount</div><div><input type="text" id="amount" name="amount" value="'+rpt.amount+'" /><br/>(User reported: '+rpt.amount_ff+')</div></td><td><div class="rpt-label">District</div><div><select id="dist" name="district" class="rpt-list">'+doptions+'</select><!--br/>(User reported: '+rpt.district_ff+')--></div></td></tr><tr><td><div class="rpt-label">Place of Incident</div><div><textarea id="where" name="where" class="rpt-ta">'+rpt.where+'</textarea></div></td><td><div class="rpt-label">Name of Reporter</div><div><textarea id="names" name="names" class="rpt-ta">'+rpt.names+'</textarea></div></td></tr><tr><td><div class="rpt-label">Category</div><div>'+cathtml+'</div></td><td><div class="rpt-label">Comments</div><div><textarea id="comments" name="comments" class="rpt-ta"></textarea><input type="hidden" name="id" value="'+rid+'" /><input type="hidden" name="csrfmiddlewaretoken" value="'+getCookie('csrftoken')+'" /></div>'+comments+'</td></tr></table></form></div>';
				
				var title = 'User Report Details';
				var btns = [{text:'Submit', click:function(){ update_rpt(rid); }}]
				
				document.getElementById('jqpopup').innerHTML = html;
				jqpopup(title, btns, 850, 450);
				
				$.datepicker.setDefaults({ dateFormat: 'mm/dd/yy' });
				$("#date").datepicker();
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
	ajax_wait('Syncing Report. Please wait ..');
	
	var r = createHttpRequest();
        r.open('POST', '/igreports/' + rid + '/sync/', true);
        r.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			if(r.status != 200) {
				alert(r.statusText);
				return;
			}
			alert('Report Successfuly synced');
			window.location.replace(window.location);
		}
	}
	r.send('csrfmiddlewaretoken='+getCookie('csrftoken'));
}
function rptsetc() {
	//alert('setting color!');
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