import datetime

#maximum amount of shorten links produced in a row
MAX_NUM = 3

#check if cookies could be deleted after some period
def request_checker(request, error):
	if not request.session.get('used'):
		request.session['used'] = 0

	if request.session.get('used')>MAX_NUM:
		time = datetime.datetime.now().strftime("%H")
		if int(time) - int(request.session.get('time')) > 1:
			request.session['used'] = 0
		else:
			return 'wait a bit!'

	request.session['used'] = request.session['used']+1
	request.session['time'] = datetime.datetime.now().strftime("%H")
	request.session['success'] = True
	request.session.modified = True

	return error
