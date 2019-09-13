import requests
import re
import execjs

def NECreditHomepage(search_word):
    homepage_url = 'http://www.gsxt.gov.cn/corp-query-homepage.html'
    search_url = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
    header = {
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        'Host': 'www.gsxt.gov.cn',
        'Referer': 'http://www.gsxt.gov.cn/corp-query-homepage.html',
        'Upgrade-Insecure-Requests': '1'
    }

    payload = {'tab': 'ent_tab',
               'province': '',
               'geetest_challenge': '',
               'geetest_validate': '',
               'geetest_seccode': '',
               'token': '2016',
               'searchword': search_word}
    s = requests.session()
    dead_homepage = s.post(homepage_url, headers=header)
    execjs.eval(r'var x="substr@@@@Oct@join@createElement@firstChild@@@@3D@@f@innerHTML@PF@@@toString@fromCharCode@18@a@else@C@@g@8@0xEDB88320@@@catch@2@@@div@25@08@GMT@replace@11@TrmB8D@function@String@pathname@@CZ@0xFF@36@@try@FA@@Array@@location@@chars@Thu@mz7O@reverse@@@var@RegExp@__jsl_clearance@1500@DOMContentLoaded@charCodeAt@@3@rOm9XFMtA3QKV7nYsPGT4lifyWwkq5vcjH2IdxUoCbhERLaz81DNB6@@@JgSe0upZ@if@@new@toLowerCase@34@match@5R@0@split@@Path@href@search@@@1540451494@https@while@captcha@length@@cookie@@1@eval@addEventListener@@@challenge@charAt@Expires@document@for@534@parseInt@@e@false@window@@@@setTimeout@return@@@@@d@@@attachEvent@@onreadystatechange".replace(/@*$/,"").split("@"),y="2b 4h=1g(){4d(\'23.38=23.1i+23.39.1d(/[\\\\?|&]3f-3p/,\\\\\'\\\\\')\',2e);42.3i=\'2d=3c.44|34|\'+(1g(){2b 4h=21(+[[-~[]]+(-~{}-~{}-~~~{}-~[]+(-~{}+[-~(+!~~[])]>>-~(+!~~[]))+[]+[[]][34])]),4n=[\'27\',(16+[]+[]),\'33\',[!{}+[[]][34]][34].40((-~{}+[-~(+!~~[])]>>-~(+!~~[]))),\'1k\',(+[~~\'\', ~~\'\']+[[]][34]).40((+[])),\'g\',[!-[]+[]+[[]][34]][34].40(-~(+!~~[])),\'1f\',[(16)*[-~(2i)]],\'3k\',(~~\'\'+[]+[[]][34]),\'o\',(~~\'\'+[]+[[]][34]),\'%\',[{}+[]+[[]][34]][34].40(-~~~{}-~[]+(-~{}+[-~(+!~~[])]>>-~(+!~~[]))),\'1p%c\'];43(2b 2=34;2<4n.3g;2++){4h.28()[2]=4n[2]};4e 4h.6(\'\')})()+\';41=26, 1a-5-l 1b:1e:31 1c;37=/;\'};2n((1g(){1o{4e !!49.3m;}15(47){4e 48;}})()){42.3m(\'2f\',4h,48)}n{42.4m(\'4o\',4h)}",f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},z=f(y.match(/\\w/g).sort(function(x,y){return f(x)-f(y)}).pop());while(z++)try{eval(y.replace(/\\b\\w+\\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));break}catch(_){}')

    homepage_cookies = dead_homepage.headers['Set-Cookie']
    header['Cookie'] = homepage_cookies
    alive_homepage = s.post(homepage_url)
    captcha = s.get('http://www.gsxt.gov.cn/SearchItemCaptcha?t=1540445574755').text
    html_content = s.post(homepage_url, data=payload, headers=header).text
    return html_content