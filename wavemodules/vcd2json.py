from vcdparser import *

def vcd2json(file):
	vcd = parse_vcd(file)
	units = get_timescale()
	i = 0
	time = 0
	endtime = get_endtime()
	data = {'file': file, 'scale': units, 'endtime': endtime, 'signals': []}
	for key, value in vcd.iteritems():
		name = value['nets'][0]['hier'] + "." +value['nets'][0]['name']
		size = value['nets'][0]['size']
		data['signals'].append({'name': name, 'size': size, 'wave':[]})
		time = 0
		
		for item in value['tv']:
			wavestruct = []
			val = item[1]
			wavestruct.append(item[0])
			if val.find('z') > -1:
				wavestruct.append('z')
			elif val.find('x') > -1:
				wavestruct.append('x')
			else:
				wavestruct.append(val)
			data['signals'][i]['wave'].append(wavestruct)
		i+=1
	return data