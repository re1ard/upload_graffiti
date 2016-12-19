# -*- coding: utf-8 -*-

#######################################
##contact: https://vk.com/id27919760 ##
#######################################

import vk_api
import os
import time
import sys

#transliterate.translit(element, 'ru', reversed=True)


def upload(file_path,uploadgroup,api):
	values = {'group_id':uploadgroup,'type':'graffiti'}
	url = api.method('docs.getUploadServer', values)['upload_url']
	with open(file_path, 'rb') as file:
	        response = api.http.post(url, files={'file': file}).json()
	response.update({'title':file_path.split('/')[len(file_path.split('/')) - 1],'tags':''})
	return response

path = os.getcwd() + u'/stickers'

def dirtest():
	if not os.path.exists('stickers'):
		os.mkdir('stickers')
		print u'папка stikers не была,найдена\nона была создана,теперь загрузи туда картинки в формате PNG'
		return False
	else:
		return True

def main(login,password,glink):
	if len(os.listdir(path)) > 39:
		print u'слишком много файлов в папке'
		return

	api = vk_api.VkApi(login,password)
	api.authorization()


	link = glink.split('/')
	link.reverse()
	response = api.method('groups.getById',{'group_ids':link[0],'fields':'can_upload_doc'})[0]
	if response['can_upload_doc'] == 0:
		print u'ты не можешь загружать документы в данную группу'
		return
	group_id = response['id']
	code = u''
	codeline = u''
	for sticker in os.listdir(path):
		updata = upload(path + u'/' + sticker,group_id,api)
		try:
			response = api.method('docs.save',updata)
			print u'//'+sticker
			print u'API.docs.add({"owner_id":' + str(response[0]['owner_id']) + u',"doc_id":' + str(response[0]['id']) + '});'
		except vk_api.Captcha as error:
			print u'//разгадка капчи:\n//ссылка на картинку: ' + error.get_url()
			captcha_code = raw_input('//response: ')
			try:
				error.try_again(captcha_code)
			except:
				print u'//ты ее наверно не так ввел,пропускаем картинку ' + sticker
				pass
			pass
		except vk_api.ApiError as error:
			if error.code == 100:
				print u'//картинка была с русским названием '
				print '//' + sticker
				pass
			pass
	print u'return ["cool"];\n\n'
	print u'//теперь перейди на https://vk.com/dev/execute и вставь в code то что было напечатано скриптом и нажми на выполнить,после все картинки увидишь в документах'
	return

if __name__ == '__main__':
	if dirtest():
		print '\n\n'
		main(sys.argv[1],sys.argv[2],sys.argv[3])