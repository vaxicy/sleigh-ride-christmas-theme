from pathlib import Path
import base64
import json
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
def embedded(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()

with Image.open(ROOT/'source/logo.png') as image:
    image = image.convert('RGBA')
    image = image.crop(image.getchannel('A').point(lambda a:255 if a>32 else 0).getbbox())
    image.thumbnail((112,112), Image.Resampling.LANCZOS)
    icon = Image.new('RGBA',(128,128))
    icon.alpha_composite(image,((128-image.width)//2,(128-image.height)//2))
    (ROOT/'logo').mkdir(exist_ok=True)
    icon.save(ROOT/'logo/logo128.png')

logo = embedded(ROOT/'logo/logo128.png')
sleigh = embedded(ROOT/'source/sleigh.png')
css = '''
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:#244C3D}h1{font-family:Georgia,serif;font-weight:normal}
.browser{width:1280px;height:800px;background:#244C3D;position:relative;overflow:hidden}.tabs{height:38px;background:#244C3D;display:flex;align-items:end;gap:8px;padding:0 12px;color:#FBF6ED;font-size:12px}.tab{width:200px;padding:11px 15px}.active{background:#F7EEDF;color:#244C3D;border-radius:12px 12px 0 0}.tools{height:48px;background:#F7EEDF;display:flex;align-items:center;gap:22px;padding:0 18px;font-size:20px}.omni{border:2px solid #7A8DAB;border-radius:24px;flex:1;background:white;height:35px;padding:6px 12px;font-size:14px;color:#4285F4}.bookmarks{background:#F7EEDF;height:28px;padding:7px 18px;display:flex;gap:25px;font-size:11px}.page{position:relative;height:686px;text-align:center;padding-top:64px;color:#EEE}.page:before{content:'';position:absolute;top:0;left:0;right:0;height:80px;background:linear-gradient(#0003,transparent);pointer-events:none}.art{display:block;width:210px;height:67px;object-fit:contain;margin:auto}.google{font-size:80px;letter-spacing:-4px;margin:8px 0 35px;line-height:1.1}.search{width:720px;height:54px;border-radius:30px;background:white;color:#9AA0A6;margin:auto;display:flex;align-items:center;text-align:left;padding:0 22px;gap:18px;font-size:17px}.search b{color:#202124;font-size:23px;font-weight:normal}.ai{margin-left:auto;background:#F3F5F6;color:#202124;padding:9px 12px;border-radius:20px;font-size:13px}.cards{display:flex;justify-content:center;gap:12px;margin-top:15px}.cards>div{width:232px;background:#3C4043;color:#E8F0FE;border-radius:17px;padding:13px 18px;text-align:left;font-size:14px}.cards small{display:block;margin:5px 0 0 22px;font-size:12px}.shortcuts{display:flex;gap:28px;justify-content:center;margin-top:55px;font-size:12px}.shortcut{width:80px}.circle{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;margin:0 auto 13px;background:#1A3C30;font-size:21px}.customize{position:absolute;right:15px;bottom:16px;width:37px;height:37px;border-radius:50%;background:#102B22;color:white;display:grid;place-items:center}.kicker{font-size:11px;letter-spacing:3px}.intro{width:1280px;height:800px;background:#E6E9EC;padding:58px 65px}.intro h1{font-size:52px;margin:20px 0 12px}.intro p{font-size:21px}.palette{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:35px}.swatch{height:185px;border-radius:18px;padding:28px;display:flex;flex-direction:column;justify-content:end}.swatch b{font-size:25px}.swatch span{font-size:15px;margin-top:12px}.intro .foot{font-size:15px;margin-top:28px}.intro img{float:right;width:100px;height:100px}.small{width:440px;height:280px;background:#F3F1EB;display:flex;align-items:center;justify-content:center;text-align:center}.small img{display:block;width:88px;height:88px;margin:0 auto 12px}.small h1{font-size:28px;margin:0 0 14px}.small p{font-size:13px;margin:0 0 21px}.wide{width:1400px;height:560px;background:#F3F1EB;position:relative;overflow:hidden}.copy{position:absolute;left:58px;top:68px;width:400px}.copy img{width:100px;height:100px;display:block;margin-bottom:8px}.copy h1{font-size:53px;line-height:1.05;margin:10px 0 22px}.copy p{font-size:19px;line-height:1.55;margin:0 0 25px}.preview{position:absolute;left:510px;top:77px;transform:scale(.66);transform-origin:top left;border:1px solid #244C3D33;border-radius:15px;overflow:hidden;box-shadow:0 16px 40px #244C3D22}.wide .browser{height:614px}.wide .page{height:500px;padding-top:30px}.wide .google{margin-bottom:23px}.wide .shortcuts{margin-top:28px}
'''

def browser():
    return f'''<div class="browser"><div class="tabs"><div class="tab">Reading list　×</div><div class="tab">Inspiration　×</div><div class="tab active">New Tab　×</div><span style="margin-left:auto;padding:10px">−　□　×</span></div><div class="tools">←　→　↻　⌂<div class="omni">G</div>♧　⋮</div><div class="bookmarks"><span>▱ Tools</span><span>▱ Reading</span><span>▱ Inspiration</span><span>▱ Design</span></div><div class="page"><img class="art" src="{sleigh}"><div class="google">Google</div><div class="search"><b>+</b>Ask Google<span style="margin-left:auto;color:#202124">♩　▣</span><span class="ai">✧ AI Mode</span></div><div class="cards"><div>✧　Try AI Mode<small>Create, summarize, plan</small></div><div>▣　Create images<small>Imagine, edit, draw</small></div></div><div class="shortcuts"><div class="shortcut"><div class="circle" style="color:#FF0033">▶</div>YouTube</div><div class="shortcut"><div class="circle">▣</div>Web Store</div><div class="shortcut"><div class="circle">+</div>Add shortcut</div></div><div class="customize">✎</div></div></div>'''

palette=[('Pine Green','#244C3D','Window frame & New Tab page','#FBF6ED'),('Warm Cream','#F7EEDF','Toolbar & active tab','#244C3D'),('Christmas Red','#B53238','Sleigh illustration','#FFFFFF'),('Warm Gold','#D6A553','Sleigh details & logo','#244C3D')]
swatches=''.join(f'<div class="swatch" style="background:{hex};color:{ink}"><b>{name}</b><span>{hex} · {role}</span></div>' for name,hex,role,ink in palette)
intro=f'<div class="intro"><img src="{logo}"><div class="kicker">A QUIET CHRISTMAS MOMENT</div><h1>Sleigh Ride Christmas Theme</h1><p>A little Christmas magic above every search.</p><div class="palette">{swatches}</div><p class="foot">Static sleigh artwork · Pine green & cream · No permissions required</p></div>'
small=f'<div class="small"><div><img src="{logo}"><h1>Sleigh Ride Christmas</h1><p>A little Christmas magic in every tab.</p><div class="kicker">CHROME THEME</div></div></div>'
native = embedded(ROOT/'store-assets/screenshots/en/screenshot-1-browser.png')
css += '.preview{left:510px;top:26px;transform:none;width:840px;height:508px;background:#244C3D;display:flex;align-items:center}.native-preview{display:block;width:100%;height:auto}'
wide=f'<div class="wide"><div class="copy"><img src="{logo}"><h1>Sleigh Ride<br>Christmas</h1><p>Pine green. Warm cream.<br>A little Christmas magic in every tab.</p><div class="kicker">CHROME THEME</div></div><div class="preview"><img class="native-preview" src="{native}"></div></div>'
jobs=[('screenshot-1-browser',1280,800,browser(),'screenshots/en/screenshot-1-browser.png'),('screenshot-2-introduction',1280,800,intro,'screenshots/en/screenshot-2-introduction.png'),('promo-440x280',440,280,small,'promo/440x280.png'),('promo-1400x560',1400,560,wide,'promo/1400x560.png')]
with sync_playwright() as p:
    engine=p.chromium.launch(headless=True,executable_path=str(Path.home()/'AppData/Local/ms-playwright/chromium-1248/chrome-win64/chrome.exe'))
    page=engine.new_page(device_scale_factor=1)
    for name,w,h,body,dest in jobs:
        if name == 'screenshot-1-browser' and (ROOT/'store-assets'/dest).exists():
            print('Preserved native browser screenshot')
            continue
        html='<html lang="en"><meta charset="utf-8"><style>'+css+'</style><body>'+body+'</body></html>'
        ref=ROOT/'store-assets/references'/f'{name}.html'
        ref.parent.mkdir(parents=True,exist_ok=True)
        ref.write_text(html,encoding='utf-8')
        target=ROOT/'store-assets'/dest
        target.parent.mkdir(parents=True,exist_ok=True)
        page.set_viewport_size({'width':w,'height':h})
        page.set_content(html)
        page.evaluate('document.fonts.ready')
        if name=='screenshot-2-introduction':
            assert page.locator('.intro').evaluate('(el)=>el.scrollHeight<=el.clientHeight')
        page.screenshot(path=str(target))
        assert Image.open(target).size==(w,h)
        print('Rendered',dest)
    engine.close()
