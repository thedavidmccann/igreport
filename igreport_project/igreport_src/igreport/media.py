"""
Pulled from URLs below:
http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/redmond/jquery-ui.css
http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js
http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js
-- Johnson
"""
from django.conf import settings
class JQueryUIMedia:
	jqroot = '%s/igreport/jquery' % settings.STATIC_URL
	root = '%s/igreport' % settings.STATIC_URL
	js = (
		'%s/jquery.min.js' % jqroot,
		'%s/jquery-ui.min.js' % jqroot,
		'%s/js/ajax.js' % root,
		'%s/js/custom.js' % root,
	)
	css = {
		'all': (
			'%s/jquery-ui.css' % jqroot,
			'%s/css/custom.css' % root,
		)
	}
