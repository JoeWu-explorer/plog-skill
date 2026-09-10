// Optional integration check: the three-photo examples/album/story.json sample.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');const fs=require('node:fs');
const path=require('node:path');const {pathToFileURL}=require('node:url');
if(process.argv.length!==4)throw new Error('Usage: node tests/album_browser.cjs sample.html new-output-directory');
(async()=>{
const b=await chromium.launch({headless:true});
const dir=path.resolve(process.argv[3]);fs.mkdirSync(dir);
const url=pathToFileURL(path.resolve(process.argv[2])).href;
const errors=[],requests=[];
const p=await b.newPage({viewport:{width:1440,height:1050},acceptDownloads:true});
p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
await p.goto(url);await p.waitForFunction(()=>document.body.classList.contains('ready'));
assert.equal(await p.locator('#book').getAttribute('data-state'),'0');
await p.screenshot({path:dir+'/book-cover.png'});
const turn=async(dir,state)=>{await p.locator(dir>0?'#next':'#previous').click();await p.waitForFunction(s=>document.querySelector('#book').dataset.state===String(s)&&document.querySelector('#book').dataset.busy==='false',state)};
await turn(1,1);
await p.locator('#next').click();
await p.waitForFunction(()=>document.querySelector('#book').dataset.busy==='true');
await new Promise(r=>setTimeout(r,380));
await p.screenshot({path:dir+'/book-turn.png'});
await p.waitForFunction(()=>document.querySelector('#book').dataset.state==='2'&&document.querySelector('#book').dataset.busy==='false');
await p.screenshot({path:dir+'/book-spread.png'});
await turn(-1,1);await p.locator('#book').focus();await p.keyboard.press('ArrowRight');
await p.waitForFunction(()=>document.querySelector('#book').dataset.state==='2'&&document.querySelector('#book').dataset.busy==='false');
await turn(1,3);await turn(1,4);assert(await p.locator('#next').isDisabled());
await p.locator('#play').click();await p.waitForFunction(()=>document.querySelector('#book').dataset.state==='1'&&document.querySelector('#book').dataset.busy==='false');await p.locator('#play').click();
assert.equal(await p.locator('#play').textContent(),'自动翻阅');
// Export the complete movie through the user-facing button.
const downloadPromise=p.waitForEvent('download',{timeout:90000});await p.locator('#export').click();
const download=await downloadPromise;const videoFile=download.suggestedFilename();await download.saveAs(path.join(dir,videoFile));
await p.waitForFunction(()=>!document.querySelector('#export').disabled);
assert((await p.locator('#status').textContent()).includes('动画已生成'));
assert.equal(await p.locator('#book').getAttribute('data-state'),'1');
// Cancelled recordings must not produce partial downloads or leave controls locked.
let extraDownloads=0;p.on('download',()=>extraDownloads++);
await p.locator('#export').click();await p.locator('#cancel').click();
await p.waitForFunction(()=>document.querySelector('#status').textContent.includes('已取消'));
assert.equal(extraDownloads,0);assert.equal(await p.locator('#book').getAttribute('data-state'),'1');
// The downloadable book must reopen with all images embedded and working animation.
const htmlDownload=p.waitForEvent('download');await p.locator('#save-html').click();
await (await htmlDownload).saveAs(dir+'/saved-book.html');await p.goto('file://'+dir+'/saved-book.html');
await p.waitForFunction(()=>document.body.classList.contains('ready'));assert.equal(await p.locator('img').count(),4);
await p.emulateMedia({media:'print'});await p.evaluate(()=>window.dispatchEvent(new Event('beforeprint')));
assert.equal(await p.locator('.spread:visible').count(),3);
await p.emulateMedia({media:'screen'});await p.evaluate(()=>window.dispatchEvent(new Event('afterprint')));
assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
const mobile=await b.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});await mobile.goto(url);await mobile.waitForFunction(()=>document.body.classList.contains('ready'));
assert(await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
await mobile.locator('#next').click();await mobile.waitForFunction(()=>document.querySelector('#book').dataset.state==='1');
await mobile.screenshot({path:dir+'/book-mobile.png'});
await mobile.locator('summary').click();assert.equal(await mobile.locator('.spread:visible').count(),3);
const nojs=await b.newPage({javaScriptEnabled:false});await nojs.goto(url);assert.equal(await nojs.locator('.spread:visible').count(),3);
const report={forward:true,backward:true,keyboard:true,autoPlay:true,video:videoFile,cancel:true,saveHTML:true,print:true,mobile:true,reducedMotion:true,noJavaScript:true,errors,requests};
fs.writeFileSync(dir+'/book-browser-checks.json',JSON.stringify(report,null,2));console.log({...report,output:dir});await b.close();
})().catch(e=>{console.error(e);process.exit(1)});
