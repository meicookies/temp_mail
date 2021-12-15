#!/usr/bin/python3
import requests, json, os

r = requests.session()
os.system("python3 -m http.server --bind 0.0.0.0 8080 &")

banner = """
Free Temporary Email address for verification

[0] Generate new address
[1] View message
"""
def response(payload):
    api = f"https://www.1secmail.com/api/v1/?action={payload}"                                                            
    return json.loads(r.get(api).text)

create_mail = lambda email: open(".email", 'w').write(email)
check_email = lambda: open(".email", 'r').read()

payloads = ["genRandomMailbox&count=1", "getMessages", "readMessage"]                                                 
generate = response(payloads[0])
view_read = response                                                                                                  
while True:
    os.system("clear")
    print(banner)
    try:
        print(f"[*] Your current Email: {check_email()}")
        from_mail = check_email().split("@")
        usr = from_mail[0]
        dom = from_mail[1]
        for_auth = f"&login={usr}&domain={dom}"
        print(f"[*] Username: {usr}\n[*] Domain: {dom}\n")
        try:
            opt = int(input("[+] Choose: "))
            if opt == 0:
                yn = str(input("[+] Want to change your email? [yn]: "))
                if yn == "y":
                    create_mail(generate[0])
            elif opt == 1:
                check = view_read(f"{payloads[1] + for_auth}")
                if len(check) < 1:
                    print(f"[-] No messages yet len(check) = {len(check)}")
                    os.system("sleep 2")
                elif len(check) >= 1:
                    data = [check[0]["id"], check[0]["from"], check[0]["subject"], check[0]["date"]]
                    print(f"\nid: {data[0]}\nfrom: {data[1]}\nsubject: {data[2]}\ndate: {data[3]}\n")
                    yn = str(input("[+] Want to read this message? [yn]: "))
                    if yn == "y":
                        html = view_read(f"{payloads[2] + for_auth}&id={data[0]}")["body"]
                        open("index.html", 'w').write(html)
                        os.system("xdg-open http://0.0.0.0:8080/index.html")
        except ValueError:
            print("[-] Input Integer")
            os.system("sleep 2")
        except (KeyboardInterrupt, EOFError):
            print("Byee...")
            os.system("killall -9 python3 2>/dev/null")
            break
    except FileNotFoundError:
        create_mail(generate[0])
