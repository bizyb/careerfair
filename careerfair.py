from bs4 import Beautifulsoup as bsoup
import csv
import json
import random
import re
import requests
from time import time
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
USER_AGENT += "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 "
USER_AGENT += "Safari/537.36"


class CareerFair(object):
	'''
	Parses and outputs employer names and descriptions from the Viterbi Career 
	Gateway for a given major. Currently, it's not possible to sort the search 
	results by industry or major. This should fix that problem. 
	'''

	def __init__(self, *args, **kwargs):
		self.landing_url = kwargs.get('base')
		# self.ajax_base = kwargs.get('ajax')
		self.major = kwargs.get('major')
		self.headers = self._set_header()
		

	def get_employers(self):
		landing_page = self._get_request(self.landing_url)
		page_count = self._get_pagination(response)
		url_list = self._build_urls()
		response_list = []
		for url in url_list:
			response = self._get_request(url)
			response_list.append(response)
			time.sleep(3) # 3-second throttle

	def _get_pagination(self, response):
		soup = bsoup(response.text, 'lxml')
		interval = soup selector here
		employer_count = soup selector here
		num_pages = employer_count/interval
		if employer_count % interval != 0:
			num_pages += 1
		return num_pages

	def _parse_json(self, responses):
		'''
		Parse the json and build a csv-friendly data structure. 

		NB: This is where we determine which columns to include or exclude from 
		the csv. Refer to the actual json (in Chrome or Firefox) and add more 
		columns in the for loop if desired. Data passed to csv must be a 
		key-value pair with 'flat' values, i.e. primitive strings or numbers 
		only.
		'''
		filtered_employers = []
		all_employers = []
		for response in responses:
			try:
				raw_json = json.loads(response.text)
				models_list = raw_json.get('models') 
				for data in models_list:
					employer_dict = {
						'name': data.get('name'),
						'positions': self._parse_list(data.get('position_types'), pos=True),
						'degrees': self._parse_list(data.get('degree_level'), degrees=True),
						'majors': self._parse_list(data.get('major'), majors=True),
						'description': data.get('overview'),
					}
					# only add employer data for the requested major
					if self.major in majors.get('majors'):
						filtered_employers.append(employer_dict)

					# unfiltered
					all_employers.append(employer_dict)

			except Exception as e:
				msg = '{}: {}'.format(type(e).__name__, e.args[0])
				print msg

		self._save_to_csv(filtered_employers, filtered=True)
		self._save_to_csv(all_employers, filtered=False)

	def _save_to_csv(self, data, filtered=False):
		filename = 'usc_viterbi_careerfair_unfiltered.csv'
		if filtered:
			filename.replace('unfiltered', 'filtered_{}'.format(self.major))

		# build field names	
		fields = data[0].keys()

		with open(filename, 'w') as csv_out:
			writer = csv.DictWriter(csv_out, fieldnames=fields)
			writer.writeheader()
			for row_dict in data:
				writer.writerow(row_dict)
		msg = 'Outputted file with name={}\n'.format(filename)
		print msg

	def _parse_list(self, list_data, majors=False, degrees=False, pos=False):
		'''
		'Flatten' a list object containing dictionary elements by turning them 
		into a single key-value pair, where the values are comma-separated 
		elements.
		Input:
			degrees = 
			[
				{
					"_id": 1,
					"_label": "Bachelors"
				},
				{
					"_id": 2,
					"_label": "Masters"
				},
				{
					"_id": 3,
					"_label": "PhD"
				}
			]

		Output:
			degrees = {'Bachelors, 'Masters, 'PhD'}

		'''
		data_dict = {}
		for ld in list_data:
			if majors:
				key = 'majors'
			elif degrees:
				key = 'degrees'
			elif pos:
				key = 'positions'
			if data_dict:
				data_dict[key] += ', ' + ld.get('_label')
			else:
				data_dict[key] = ld.get('_label')
		return data_dict

	def _get_request(self, url):
		params = {'headers': self.headers}
		response = requests.get(self.landing_url, **params)
	
	def _set_header(self):
		headers = requests.utils.default_headers()
		headers.update({'User-Agent': USER_AGENT})
		return headers

	def _build_url():
		pass

	def _build_ajax_base():
		'''
		Parse out session-specific uid from the landing url and build 
		the base url for ajax requests. 

		Base url format: 'https://viterbi-usc-csm.symplicity.com/events/
								c495591c0cb4d00420fb15c629163e76/employers'
		session_uid: c495591c0cb4d00420fb15c629163
		'''
		UID_LENGTH = 32
		ajax_base = ''
		pattern = '\w+['+UID_LENGTH+']'
		session_uid = re.findall(pattern, url)
		if session_uid:
			session_uid = session_uid[0]
			prefix = 'https://viterbi-usc-csm.symplicity.com/api/v2/'
			prefix += 'eventRegistration?approved=1&event='
			suffix = session_uid + '&id=' + session_uid
			ajax_base = prefix + suffix
		
		return ajax_base




