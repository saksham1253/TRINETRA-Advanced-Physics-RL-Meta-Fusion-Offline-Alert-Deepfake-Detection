// Frame-exact recorder for TRINETRA Live Flow (Node >= 22, Chromium, ffmpeg; no npm packages).
// node TRINETRA/ANIM/tools/record.mjs --url file:///.../TRINETRA_live_flow.html --out out.mp4 --fps 30 [--from 0 --to 295] [--times 1,2,3]
import {spawn, execFileSync} from 'node:child_process';
import {mkdtempSync, writeFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const url = arg('url'), out = arg('out', 'trinetra_live_flow.mp4'), fps = +arg('fps', 30), from = +arg('from', 0), to = arg('to'), times = arg('times');
const port = 9300 + Math.floor(Math.random() * 500), prof = mkdtempSync(join(tmpdir(), 'chp-')), frames = mkdtempSync(join(tmpdir(), 'frames-'));
const chrome = spawn(arg('chrome', 'chromium'), ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--window-size=1920,1080', 'about:blank'], {stdio: 'ignore'});
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map();
const cdp = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pend.set(i, {res, rej}); ws.send(JSON.stringify({id: i, method, params})); });
async function main() {
  let page;
  for (let k = 0; k < 50 && !page; k++) { await sleep(200); try { page = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(p => p.type === 'page'); } catch {} }
  ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { const p = pend.get(m.id); pend.delete(m.id); m.error ? p.rej(m.error) : p.res(m.result); } };
  await cdp('Emulation.setDeviceMetricsOverride', {width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false});
  await cdp('Page.navigate', {url: url + (url.includes('?') ? '&' : '?') + 'record=1&noexplore'});
  for (let k = 0; k < 100; k++) { await sleep(150); const r = await cdp('Runtime.evaluate', {expression: 'typeof window.__TRINETRA_SEEK', returnByValue: true}); if (r.result.value === 'function') break; }
  const total = (await cdp('Runtime.evaluate', {expression: 'window.__TRINETRA_TOTAL', returnByValue: true})).result.value;
  const T = times ? times.split(',').map(Number) : Array.from({length: Math.floor(((to ? +to : total) - from) * fps)}, (_, i) => from + i / fps);
  for (let i = 0; i < T.length; i++) {
    await cdp('Runtime.evaluate', {expression: `window.__TRINETRA_SEEK(${T[i]})`});
    let shot;
    for (let k = 0; k < 5 && !shot; k++) { try { shot = await cdp('Page.captureScreenshot', {format: 'jpeg', quality: 92}); } catch (e) { await sleep(300 * (k + 1)); } }
    if (!shot) throw new Error(`capture failed at t=${T[i]}`);
    writeFileSync(join(frames, `f${String(i).padStart(6, '0')}.jpg`), Buffer.from(shot.data, 'base64'));
    if (i % (fps * 10) === 0) console.log(`[record] ${i}/${T.length} t=${T[i].toFixed(1)}s`);
  }
  ws.close(); chrome.kill();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', join(frames, 'f%06d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out]);
  rmSync(frames, {recursive: true, force: true}); rmSync(prof, {recursive: true, force: true});
  console.log(`[record] wrote ${out} (${T.length} frames @ ${fps} fps)`);
}
main().catch(e => { console.error(e); chrome.kill(); process.exit(1); });
