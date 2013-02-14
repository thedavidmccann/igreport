function jqpopup(title, btns, w, h)
{
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
	var url = '/getreport/?id=' + rid + '&t=' + (new Date().getTime());
	var r = createHttpRequest();
	r.open('GET', url, true);
	
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			
			if(/{error:true/.test(r.responseText)) {
				var res= eval('('+ r.responseText +')');
				alert('ERR: ' + res.msg);
			} else if(/{error:false/.test(r.responseText)) {
				var o = eval('('+ r.responseText +')');
				var rpt = o.res.rpt;
				var dist = o.res.dist;
				var scty = o.res.scty;
				var cat = o.res.cat;
				var comm = o.res.comm;
				
				var doptions = '';
				for(var i=0; i<dist.length; i++) {
					doptions += '<option value="'+dist[i].id+'"'+(dist[i].id==rpt.district_id?' selected="selected"':'')+'>'+dist[i].name+'</option>';
				}
				var soptions='';
				for(var i=0; i<scty.length; i++) {
					soptions += '<option value="'+scty[i].id+'"'+(scty[i].id==rpt.subcounty_id?' selected="selected"':'')+'>'+scty[i].name+'</option>';
				}
				var cathtml = '';
				if(cat.length) {
					for(var i=0; i<cat.length; i++) {
						cathtml += '<div style="padding-bottom:3px"><input type="checkbox" id="cat_'+cat[i].id+'" name="cat_'+cat[i].id+'" value="'+cat[i].id+'"'+(cat[i].checked?' checked="checked"':'')+'/>&nbsp;<label class="rpt-option-label" for="cat_'+cat[i].id+'">'+cat[i].name+'</label></div>';
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
				var html = '<div class="report"><form id="rptform"><table border="0" cellpadding="0" cellspacing="0"><tr><td colspan="2"><div class="rpt-title">Submitted by <span style="color:#ff6600;font-weight:bold">'+rpt.sender+'</span> on <span style="color:#ff6600;font-weight:bold">'+rpt.date+'</span></div></td></tr><tr><td><div class="rpt-label">Report</div><div><textarea id="report" name="report" class="rpt-ta">'+rpt.report+'</textarea></div></td><td><div class="rpt-label">Accused</div><div><textarea id="accused" name="accused" class="rpt-ta">'+rpt.accused+'</textarea></div></td></tr><tr><td><div class="rpt-label">Amount</div><div><input type="text" id="amount" name="amount" value="'+rpt.amount+'" /><br/>(User reported: '+rpt.amount_ff+')</div></td><td><div class="rpt-label">Date of Incident</div><div><input type="text" id="date" name="date" style="cursor:pointer" title="Click to choose date" readonly="readonly" value="'+rpt.when+'"/><br/>(User reported: '+rpt.when_ff+')</div></td></tr><tr><td><div class="rpt-label">District</div><div><select id="dist" name="dist" class="rpt-list">'+doptions+'</select></div></td><td><div class="rpt-label">Subcounty</div><div><select id="sc" name="sc" class="rpt-list">'+soptions+'</select><br/>(User reported: '+rpt.sc_ff+')</div></td></tr><tr><td><div class="rpt-label">Category</div><div>'+cathtml+'</div></td><td><div class="rpt-label">Comments</div><div><textarea id="comments" class="rpt-ta"></textarea></div>'+comments+'</td></tr></table></form></div>';
				
				var title = 'User Report Details';
				var btns = [{text:'Submit', click:function(){ update_rpt(rid); }}]
				
				document.getElementById('jqpopup').innerHTML = html;
				jqpopup(title, btns, 850, 450);
				
				$.datepicker.setDefaults({ dateFormat: 'yy-mm-dd' });
				$("#date").datepicker();
			}
		}
	}
	r.send(null);	
};

function update_rpt(rid) {

	var f = document.getElementById('rptform');
	var report = f.report.value;
	var accused = f.accused.value;
	var amount = f.amount.value;
	var date = f.date.value;
	var dist = f.dist[f.dist.selectedIndex].value;
	var sc = f.sc[f.sc.selectedIndex].value;
	var comments = f.comments.value;
	
	if(report.length < 1) {
		alert('Report not valid');
		return false;
	}
	if(accused.length < 1) {
		alert('Accused not valid');
		return false;
	}
	if(!(/^[0-9]+$/.test(amount))) {
		alert('Amount not valid');
		return false;
	}
	if(!(/^\d{4}-\d{2}-\d{2}$/.test(date))) {
		alert('Date not valid');
		return false;
	}	
	if(!(/^[0-9]+$/.test(dist))) {
		alert('District not valid');
		return false;
	}
	if(!(/^[0-9]+$/.test(sc))) {
		alert('Subcounty not valid');
		return false;
	}
	if(comments.length < 1) {
		/* please provide some comments */
	}
	/* get the cats */
	cats = new Array();
	var l = f.getElementsByTagName('input');
	for(var i=0, j=0; i<l.length; i++) {
		if(/checkbox/i.test(l[i].type) && l[i].checked) {
			cats[j++]=l[i].value;
		}
	}

	var params = 'id='+rid+'&report='+encodeURIComponent(report)+'&accused='+encodeURIComponent(accused)+'&amount='+amount+'&date='+encodeURIComponent(date)+'&dist='+dist+'&sc='+sc+'&comments='+encodeURIComponent(comments);

	if(cats.length > 0) {
		params += '&catl=' + encodeURIComponent( cats.join(',') );
	}
	params += '&t=' + ( new Date().getTime() );

	ajax_wait('Updating Report. Please wait ..');
	
        var r = createHttpRequest();
	
        r.open('POST', '/updatereport/', true);
        r.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
        r.onreadystatechange = function(){
                if(r.readyState == 4){
			ajax_done();
			var rtext = r.responseText;
			if(/{error:\s*false/.test(rtext)) {
				// success reload page
				$('#jqpopup').dialog('close');
				ajax_wait_update('Report updated. Refreshing ..')
				window.location.replace(window.location);
			}
			else if(/{error:\s*true/.test(rtext)) {
				var js = eval('('+ r.responseText +')');
				ajax_done();
				//alert(js.msg);
				alert(r.responseText);
			} else {
				alert(r.responseText);
			}
		}
	}
	r.send(params);
	
	return true;	
};

function syncit(rid) {
	ajax_wait('Syncing Report. Please wait ..');

	var url = '/syncreport/?id=' + rid + '&t=' + (new Date().getTime());
	var r = createHttpRequest();
	r.open('GET', url, true);
	
	r.onreadystatechange = function() {
		if(r.readyState == 4) {
			ajax_done();
			if(/{error:true/.test(r.responseText)) {
				var res = eval('('+ r.responseText +')');
				alert('ERR: ' + res.msg);
			} else if(/{error:false/.test(r.responseText)) {
				var res= eval('('+ r.responseText +')');
				alert(res.msg);
				window.location.replace(window.location);
			}
		}
	}
	r.send(null);
}