#!/usr/bin/env python3

import http.server
import json
import os
import re
import subprocess
import tempfile
import threading
import time
import webbrowser

PORT = 7777

HTML = """<!DOCTYPE html>
<html lang="bs">
<head>
<meta charset="UTF-8">
<title>BADA APK Pusher</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@800&display=swap');
:root {
  --bg:#07070f; --sur:#0d0d1c; --brd:#181830; --acc:#00e5ff;
  --ora:#ff6b35; --txt:#dde0f5; --dim:#3a3a60; --ok:#00ff88;
  --err:#ff4466; --warn:#ffcc00;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--txt);font-family:'JetBrains Mono',monospace;min-height:100vh;display:flex;justify-content:center;padding:36px 20px;}
body::before{content:'';position:fixed;inset:0;pointer-events:none;background:radial-gradient(ellipse 55% 35% at 10% 10%,rgba(0,229,255,.07) 0%,transparent 60%),radial-gradient(ellipse 45% 45% at 90% 90%,rgba(255,107,53,.05) 0%,transparent 60%);}
.wrap{width:100%;max-width:620px;}
.eyebrow{font-size:9px;font-weight:700;letter-spacing:.35em;color:var(--acc);text-transform:uppercase;margin-bottom:4px;}
h1{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;letter-spacing:-.02em;}
h1 span{color:var(--ora);}
.sub{font-size:11px;color:var(--dim);margin-top:4px;margin-bottom:28px;}
.steps{display:flex;border:1px solid var(--brd);border-radius:8px;overflow:hidden;margin-bottom:20px;}
.step{flex:1;padding:9px 8px;font-size:9px;font-weight:700;letter-spacing:.12em;text-align:center;color:var(--dim);text-transform:uppercase;border-right:1px solid var(--brd);transition:all .2s;}
.step:last-child{border-right:none;}
.step.active{color:var(--acc);background:rgba(0,229,255,.06);}
.step.done{color:var(--ok);background:rgba(0,255,136,.04);}
.step.fail{color:var(--err);background:rgba(255,68,102,.06);}
.card{background:var(--sur);border:1px solid var(--brd);border-radius:10px;padding:20px;margin-bottom:14px;position:relative;overflow:hidden;}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--acc),transparent);opacity:.25;}
.clbl{font-size:9px;font-weight:700;letter-spacing:.22em;color:var(--dim);text-transform:uppercase;margin-bottom:14px;}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;}
.field{display:flex;flex-direction:column;gap:5px;}
.field.full{grid-column:1/-1;}
.field label{font-size:9px;color:var(--dim);letter-spacing:.1em;text-transform:uppercase;}
input[type=text]{background:var(--bg);border:1px solid var(--brd);border-radius:6px;color:var(--txt);font-family:'JetBrains Mono',monospace;font-size:12px;padding:9px 12px;outline:none;transition:border-color .2s;width:100%;}
input[type=text]:focus{border-color:var(--acc);}
.presets{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px;}
.pre{font-family:'JetBrains Mono',monospace;font-size:9px;padding:3px 9px;border-radius:4px;border:1px solid var(--brd);background:transparent;color:var(--dim);cursor:pointer;transition:all .15s;}
.pre:hover{border-color:var(--ora);color:var(--ora);}
.tog-row{display:flex;align-items:center;gap:9px;margin-top:9px;}
.tog{appearance:none;width:30px;height:16px;background:var(--brd);border-radius:8px;cursor:pointer;position:relative;transition:background .2s;flex-shrink:0;}
.tog:checked{background:var(--acc);}
.tog::after{content:'';position:absolute;width:10px;height:10px;background:#fff;border-radius:50%;top:3px;left:3px;transition:transform .2s;}
.tog:checked::after{transform:translateX(14px);}
.tog-lbl{font-size:10px;color:var(--dim);}
.dz{border:1.5px dashed var(--brd);border-radius:9px;padding:34px 20px;text-align:center;cursor:pointer;transition:all .2s;background:var(--bg);}
.dz:hover,.dz.over{border-color:var(--acc);background:rgba(0,229,255,.03);}
.dz.has{border-color:var(--ok);border-style:solid;background:rgba(0,255,136,.03);}
.dz-icon{font-size:30px;margin-bottom:8px;display:block;}
.dz-title{font-size:13px;font-weight:600;margin-bottom:3px;}
.dz-sub{font-size:10px;color:var(--dim);}
.dz-badge{display:none;font-size:12px;color:var(--ok);font-weight:600;margin-top:5px;}
.dz.has .dz-badge{display:block;}
.dz.has .dz-txt{display:none;}
#fi{display:none;}
.btn-row{display:flex;gap:9px;margin-bottom:14px;}
.btn{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;letter-spacing:.1em;padding:12px 18px;border-radius:7px;border:none;cursor:pointer;transition:all .18s;text-transform:uppercase;flex:1;}
.btn:disabled{opacity:.3;cursor:not-allowed;}
.b-pri{background:var(--acc);color:#000;}
.b-pri:hover:not(:disabled){background:#33eeff;transform:translateY(-1px);box-shadow:0 4px 20px rgba(0,229,255,.25);}
.b-sec{background:transparent;color:var(--txt);border:1px solid var(--brd);}
.b-sec:hover:not(:disabled){border-color:var(--acc);color:var(--acc);}
.b-rst{background:transparent;color:var(--dim);border:1px solid var(--brd);flex:0;padding:12px 14px;}
.b-rst:hover{border-color:var(--err);color:var(--err);}
.sbar{display:none;align-items:center;gap:8px;padding:9px 14px;border-radius:7px;font-size:10px;font-weight:700;letter-spacing:.08em;margin-bottom:12px;}
.sbar.show{display:flex;}
.s-run{background:rgba(0,229,255,.08);border:1px solid rgba(0,229,255,.2);color:var(--acc);}
.s-ok{background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.2);color:var(--ok);}
.s-err{background:rgba(255,68,102,.08);border:1px solid rgba(255,68,102,.2);color:var(--err);}
.spin{width:12px;height:12px;border:2px solid transparent;border-top-color:currentColor;border-radius:50%;animation:sp .7s linear infinite;flex-shrink:0;}
@keyframes sp{to{transform:rotate(360deg)}}
.term-wrap{display:none;}
.term-wrap.show{display:block;}
.term{background:#03030a;border:1px solid var(--brd);border-radius:8px;padding:14px 16px;font-size:11px;line-height:1.85;min-height:100px;max-height:300px;overflow-y:auto;}
.term p{margin:0;}
.l-i{color:var(--acc);} .l-ok{color:var(--ok);} .l-er{color:var(--err);} .l-w{color:var(--warn);} .l-d{color:var(--dim);}
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Android Debug Bridge</div>
  <h1><span>APK</span> Pusher</h1>
  <p class="sub">// Connect → Root → Remount → Push → Reboot &nbsp;|&nbsp; one click deployment</p>

  <div class="steps">
    <div class="step active" id="s1">① Connect</div>
    <div class="step" id="s2">② Root</div>
    <div class="step" id="s3>">③ Remount</div>
    <div class="step" id="s4">④ Push</div>
    <div class="step" id="s5">⑤ Reboot</div>
  </div>

  <div class="sbar" id="sbar">
    <div class="spin" id="spin"></div>
    <span id="stext"></span>
  </div>

  <div class="card">
    <div class="clbl">Configuration</div>
    <div class="row2">
      <div class="field">
        <label>Device IP Address</label>
        <input type="text" id="ip" value="10.78.211.102">
      </div>
      <div class="field">
        <label>ADB Port</label>
        <input type="text" id="port" value="5555">
      </div>
      <div class="field full">
        <label>Destination on device</label>
        <input type="text" id="dest" value="/system/priv-app/BADA_GA/">
      </div>
    </div>
  </div>

  <div class="card">
    <div class="clbl">APK File</div>
    <div class="dz" id="dz" onclick="document.getElementById('fi').click()">
      <span class="dz-icon">📦</span>
      <div class="dz-txt">
        <div class="dz-title">Drag &amp; drop APK here</div>
        <div class="dz-sub">or click to select</div>
      </div>
      <div class="dz-badge" id="badge"></div>
    </div>
    <input type="file" id="fi" accept=".apk">
  </div>

  <div class="btn-row">
    <button class="btn b-sec" id="btnConnect" onclick="doConnect()">🔌 Test Connection</button>
    <button class="btn b-pri" id="btnPush" onclick="doPush()" disabled>⚡ Push APK</button>
    <button class="btn b-rst" onclick="resetAll()">↺</button>
  </div>

  <div class="term-wrap" id="termWrap">
    <div class="card" style="padding:16px;">
      <div class="clbl">Log</div>
      <div class="term" id="term"></div>
    </div>
  </div>
</div>

<script>
let apkFile = null;
const dz = document.getElementById('dz');
const fi = document.getElementById('fi');

dz.addEventListener('dragover',  e=>{e.preventDefault();dz.classList.add('over');});
dz.addEventListener('dragleave', ()=>dz.classList.remove('over'));
dz.addEventListener('drop', e=>{
  e.preventDefault(); dz.classList.remove('over');
  const f=e.dataTransfer.files[0]; if(f) setFile(f);
});
fi.addEventListener('change', e=>{if(e.target.files[0]) setFile(e.target.files[0]);});

function setFile(f){
  if(!f.name.endsWith('.apk')){log('er','Not an .apk file!');return;}
  apkFile=f;
  dz.classList.add('has');
  document.getElementById('badge').textContent='✓  '+f.name+'   ('+(f.size/1024/1024).toFixed(1)+' MB)';
  document.getElementById('btnPush').disabled=false;
  log('ok','APK selected: '+f.name+' ('+(f.size/1024/1024).toFixed(1)+' MB)');
}

function setDest(p){document.getElementById('dest').value=p;}

function log(type,msg){
  const t=document.getElementById('term');
  document.getElementById('termWrap').classList.add('show');
  const p=document.createElement('p');
  p.className={ok:'l-ok',er:'l-er',i:'l-i',w:'l-w',d:'l-d'}[type]||'l-d';
  p.textContent='['+new Date().toLocaleTimeString('bs')+']  '+msg;
  t.appendChild(p); t.scrollTop=t.scrollHeight;
}

function setSt(cls,msg,spin){
  const b=document.getElementById('sbar');
  b.className='sbar show '+cls;
  document.getElementById('stext').textContent=msg;
  document.getElementById('spin').style.display=spin?'block':'none';
}

function setStep(n,state){
  const el=document.getElementById('s'+n);
  if(el) el.className='step '+(state||'');
}

async function doConnect(){
  const ip=document.getElementById('ip').value.trim();
  const port=document.getElementById('port').value.trim()||'5555';
  if(!ip){log('er','Please enter an IP address!');return;}
  document.getElementById('btnConnect').disabled=true;
  setSt('s-run','Connecting to '+ip+':'+port+'...',true);
  setStep(1,'active');
  log('i','Testing connection to '+ip+':'+port+'...');
  try{
    const r=await fetch('/connect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ip,port})});
    const d=await r.json();
    if(d.ok){
      log('ok','✓ Connected! '+d.msg);
      setStep(1,'done');
      setSt('s-ok','✓ Device connected',false);
    } else {
      log('er','✗ '+d.msg);
      setStep(1,'fail');
      setSt('s-err','✗ Connection failed',false);
    }
  }catch(e){
    log('er','✗ '+e.message);
    setSt('s-err','✗ Error',false);
  }
  document.getElementById('btnConnect').disabled=false;
}

async function doPush(){
  if(!apkFile) return;
  const ip=document.getElementById('ip').value.trim();
  const port=document.getElementById('port').value.trim()||'5555';
  const dest=document.getElementById('dest').value.trim();
  const remount=true;
  const reboot=true;
  if(!ip){log('er','Please enter an IP address!');return;}

  document.getElementById('btnPush').disabled=true;
  document.getElementById('btnConnect').disabled=true;
  setSt('s-run','Uploading APK...',true);
  log('d','─── Starting deployment ───');

  const fd=new FormData();
  fd.append('apk',apkFile,apkFile.name);
  fd.append('ip',ip); fd.append('port',port); fd.append('dest',dest);
  fd.append('remount',remount?'1':'0'); fd.append('reboot',reboot?'1':'0');

  try{
    const resp=await fetch('/push',{method:'POST',body:fd});
    if(!resp.ok){log('er','HTTP '+resp.status);setSt('s-err','✗ Error',false);return;}
    const reader=resp.body.getReader();
    const dec=new TextDecoder();
    let buf='';
    while(true){
      const{value,done}=await reader.read();
      if(done) break;
      buf+=dec.decode(value,{stream:true});
      const lines=buf.split('\\n'); buf=lines.pop();
      for(const line of lines){
        if(!line.trim()) continue;
        try{
          const o=JSON.parse(line);
          if(o.m) log(o.t,o.m);
          if(o.step) setStep(o.step,o.state||'active');
          if(o.done) setSt('s-ok','✓ Deployment complete!',false);
          if(o.fail) setSt('s-err','✗ Error — check the log',false);
        }catch(_){}
      }
    }
  }catch(e){
    log('er','Connection interrupted: '+e.message);
    setSt('s-err','✗ Error',false);
  }
  document.getElementById('btnPush').disabled=false;
  document.getElementById('btnConnect').disabled=false;
}

function resetAll(){
  apkFile=null; dz.classList.remove('has');
  document.getElementById('badge').textContent='';
  fi.value=''; document.getElementById('btnPush').disabled=true;
  document.getElementById('term').innerHTML='';
  document.getElementById('termWrap').classList.remove('show');
  document.getElementById('sbar').className='sbar';
  ['s1','s2','s3','s4'].forEach((id,i)=>{
    document.getElementById(id).className='step'+(i===0?' active':'');
  });
}
</script>
</body>
</html>"""


def parse_multipart(data: bytes, boundary: bytes) -> dict:
    fields = {}
    sep = b'--' + boundary
    for part in data.split(sep)[1:]:
        if part.strip() in (b'--', b'--\r\n'):
            continue
        if part.startswith(b'\r\n'):
            part = part[2:]
        if b'\r\n\r\n' not in part:
            continue
        head_raw, _, body = part.partition(b'\r\n\r\n')
        body = body.rstrip(b'\r\n')
        head = head_raw.decode('utf-8', errors='replace')
        name = filename = None
        for line in head.split('\r\n'):
            if 'Content-Disposition' not in line:
                continue
            m = re.search(r'name="([^"]+)"', line)
            if m: name = m.group(1)
            m = re.search(r'filename="([^"]+)"', line)
            if m: filename = m.group(1)
        if name:
            fields[name] = body
            if filename:
                fields['__filename__'] = filename
    return fields


def adb(args: list, timeout: int = 90):
    try:
        r = subprocess.run(['adb'] + args, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout + r.stderr).strip()
        return r.returncode == 0, out
    except FileNotFoundError:
        return False, 'adb not found in PATH!'
    except subprocess.TimeoutExpired:
        return False, f'Timeout ({timeout}s)'


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode())

    def do_POST(self):
        if   self.path == '/connect': self._connect()
        elif self.path == '/push':    self._push()
        else: self.send_response(404); self.end_headers()

    def _connect(self):
        length = int(self.headers.get('Content-Length', 0))
        data   = json.loads(self.rfile.read(length))
        ip     = data.get('ip', '').strip()
        port   = data.get('port', '5555').strip() or '5555'
        target = f'{ip}:{port}'

        ok, out = adb(['connect', target], timeout=15)
        success = ok and ('connected' in out.lower() or 'already connected' in out.lower())

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': success, 'msg': out}).encode())

    def _push(self):
        ct     = self.headers.get('Content-Type', '')
        length = int(self.headers.get('Content-Length', 0))
        body   = self.rfile.read(length)

        boundary = None
        for part in ct.split(';'):
            s = part.strip()
            if s.startswith('boundary='):
                boundary = s[9:].strip('"').encode()
                break

        if not boundary:
            self.send_response(400); self.end_headers()
            self.wfile.write(b'Missing boundary'); return

        form      = parse_multipart(body, boundary)
        ip        = form.get('ip',      b'').decode().strip()
        port      = form.get('port',    b'5555').decode().strip() or '5555'
        dest      = form.get('dest',    b'/sdcard/').decode().strip()
        remount   = form.get('remount', b'0').decode() == '1'
        do_reboot = form.get('reboot',  b'0').decode() == '1'
        apk_data  = form.get('apk')
        apk_name  = form.get('__filename__', 'app.apk')
        device    = f'{ip}:{port}'

        if not apk_data:
            self.send_response(400); self.end_headers()
            self.wfile.write(b'Nema APK Filea'); return

        self.send_response(200)
        self.send_header('Content-Type', 'application/x-ndjson')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Accel-Buffering', 'no')
        self.end_headers()

        def emit(t='d', m='', **kw):
            obj = {'t': t, 'm': m, **kw}
            try:
                self.wfile.write((json.dumps(obj, ensure_ascii=False) + '\n').encode())
                self.wfile.flush()
            except Exception:
                pass

        def run(args, label, step=None):
            emit('i', '$ adb -s ' + device + ' ' + ' '.join(str(a) for a in args))
            ok, out = adb(['-s', device] + args)
            for line in out.split('\n'):
                if line.strip(): emit('d', '  ' + line.strip())
            if ok:
                emit('ok', '✓ ' + label)
                if step: emit(step=step, state='done')
            else:
                emit('er', '✗ ' + label + ' failed')
                if step: emit(step=step, state='fail')
            return ok

        tmp = tempfile.NamedTemporaryFile(suffix='.apk', delete=False)
        tmp.write(apk_data); tmp.close()

        try:
            emit('i', f'Device : {device}')
            emit('i', f'APK    : {apk_name} ({len(apk_data)/1024/1024:.1f} MB)')
            emit('i', f'Dest   : {dest}')

            # 1. connect
            emit(step=1, state='active')
            ok, out = adb(['connect', device], timeout=15)
            for line in out.split('\n'):
                if line.strip(): emit('d', '  ' + line.strip())
            if not ('connected' in out.lower() or 'already connected' in out.lower()):
                emit('er', 'Connection failed!', fail=True)
                emit(step=1, state='fail'); return
            emit('ok', 'Connected to ' + device)
            emit(step=1, state='done')
            time.sleep(0.5)

            # 2. root
            emit(step=2, state='active')
            if not run(['root'], 'root', step=2):
                emit('er', 'Root failed!', fail=True); return
            time.sleep(1.5)

            # remount
            if remount:
                run(['remount'], 'remount')
                time.sleep(0.5)

            # 3. push
            emit(step=3, state='active')
            if not run(['push', tmp.name, dest], 'push APK', step=3):
                emit('er', 'Push failed!', fail=True); return

            # 4. reboot
            if do_reboot:
                emit(step=4, state='active')
                run(['reboot'], 'reboot', step=4)
                emit('w', 'Device is rebooting...')

            emit('ok', 'Deployment complete!', done=True)
        finally:
            os.unlink(tmp.name)


def main():
    print('Starting BADA APK Pusher...', flush=True)
    try:
        server = http.server.HTTPServer(('localhost', PORT), Handler)
    except OSError as e:
        print(f'ERROR: Port {PORT} is already in use: {e}', flush=True)
        print('Run: sudo lsof -i :7777', flush=True)
        return

    url = f'http://localhost:{PORT}'

    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')


if __name__ == '__main__':
    main()