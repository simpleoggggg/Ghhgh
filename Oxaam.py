import requests
import random
import string
import re
import json
from bs4 import BeautifulSoup
BASE_URL="https://www.oxaam.com/"
FREE_URL="https://www.oxaam.com/freeservice.php"
PASS_PREFIX="@SajagOG"
NAME_FIXER={
"Krunshyrole":"Crunchyroll","Traddingvu":"TradingView","Ghramlee":"Grammarly","Skrybd":"Scribd","Skyillchare":"Skillshare","Phaphauz":"Firehouse","Apliv":"Apple","Phankode":"FanCode","Utubye":"YouTube","Prayhm":"Prime Video","Ziyu":"Zee5","Tiedla":"Tidal","Aapik":"Epic","Adubye":"Adobe","Gei5":"ZEE5"}
def fix_name(raw_name):
    clean=re.sub(r'(?i)click here to activate|free|\s+',' ',raw_name).strip()
    for typo,correct in NAME_FIXER.items():
        if typo.lower() in clean.lower():
            tier=re.search(r'(?i)premium|pro|ultra',raw_name)
            return f"{correct} {tier.group(0) if tier else ''}".strip()
    return clean
def convert_to_netscape(cookie_dict):
    netscape_text="# Netscape HTTP Cookie File\n"
    for name,value in cookie_dict.items():
        netscape_text+=f".oxaam.com\tTRUE\t/\tFALSE\t0\t{name}\t{value}\n"
    return netscape_text
def run_extractor():
    session=requests.Session()
    user={"name":"Sajag_User","email":f"tester_{''.join(random.choices(string.ascii_lowercase,k=5))}@gmail.com","phone":"9"+"".join(random.choices(string.digits,k=9)),"password":"GlobalPass123!","country":"India"}
    headers={"User-Agent":"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"}
    print(f"[*] Registering User: {user['email']}")
    try:
        session.post(BASE_URL,data=user,headers=headers)
        r=session.get(FREE_URL,headers={**headers,"Referer":BASE_URL+"dashboard.php"})
        soup=BeautifulSoup(r.text,'html.parser')
        print("\n"+"═"*40+"\n      MADE BY @SAJAGOG\n"+"═"*40+"\n")
        for details in soup.find_all('details'):
            summary=details.find('summary')
            if not summary:continue
            display_name=fix_name(summary.get_text())
            content_html=str(details)
            print(f"🔹 {display_name}")
            emails=re.findall(r'[\w\.-]+@[\w\.-]+\.\w+',content_html)
            if emails:print(f"   📧 Email: {emails[0]}")
            pass_match=re.search(rf'{PASS_PREFIX}\d+[#@!]?',content_html)
            js_pass=re.search(r'"password"\s*:\s*"([^"➜]+)"',content_html)
            text_pass=re.search(r'(?i)password[:\s]+([a-zA-Z0-9@#!\$\%\^\&\*]{6,})',details.get_text())
            if pass_match:print(f"   🔑 Pass : {pass_match.group(0)}")
            elif js_pass:print(f"   🔑 Pass : {js_pass.group(1)}")
            elif text_pass:print(f"   🔑 Pass : {text_pass.group(1)}")
            if "cookie" in content_html.lower() or "session" in content_html.lower():
                json_match=re.search(r'\[\s*\{.*\}\s*\]',content_html,re.DOTALL)
                save_name=display_name.replace(' ','_')
                if json_match:
                    with open(f"{save_name}.json","w") as f:f.write(json_match.group(0))
                    print(f"   ✅ Data: JSON Cookies saved.")
                else:
                    with open(f"{save_name}_session.txt","w") as f:f.write(convert_to_netscape(session.cookies.get_dict()))
                    print(f"   ✅ Data: Netscape Session saved.")
            print("─"*40)
    except Exception as e:print(f"[-] Error: {e}")
if __name__=="__main__":
    run_extractor()
