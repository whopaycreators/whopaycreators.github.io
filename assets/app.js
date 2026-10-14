const FREE=10,$=s=>document.querySelector(s);
document.getElementById('upd').textContent=new Date(UPDATED+'T12:00:00').toDateString()===new Date().toDateString()?'today':UPDATED;
document.querySelectorAll('.cnt').forEach(e=>{let n=+e.dataset.n,i=0,t=setInterval(()=>{e.textContent=++i>=n?(clearInterval(t),n):i},900/n)});
const fill=(id,k)=>[...new Set(DEALS.map(d=>k(d)))].sort().forEach(v=>$(id).add(new Option(v,v)));
fill('#fn',d=>d.niche);fill('#fp',d=>d.kind=='live_post'?'Live sponsored posts':'Open programs');fill('#ft',d=>d.deal_type);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function draw(){const q=$('#q').value.toLowerCase(),n=$('#fn').value,p=$('#fp').value,t=$('#ft').value;
const r=DEALS.filter(d=>(!q||JSON.stringify(d).toLowerCase().includes(q))&&(!n||d.niche==n)&&(!t||d.deal_type==t)&&(!p||(d.kind=='live_post'?'Live sponsored posts':'Open programs')==p));
const ph=(q||n||p||t)?0:LOCKED;$('#list').innerHTML=r.map((d,i)=>`<div class="deal"><div class="top"><div class="brand">${esc(d.brand)}</div>${d.kind=='live_post'?'<span class="chip live">● LIVE POST</span>':''}</div><div class="pay">${esc(d.pay)}</div><div>${esc(d.creator_size)}</div><div class="chips"><span class="chip">${esc(d.niche)}</span><span class="chip">${esc(d.deal_type)}</span><span class="chip">${esc(d.platform)}</span></div><div style="margin-top:8px"><a href="${esc(d.source)}" target="_blank" rel="noopener">Source ↗</a> · <span class="chip">seen ${esc(d.date_seen)}</span></div></div>`).join('')+Array.from({length:Math.min(ph,3)},()=>'<div class="deal locked"><div class="brand">██████ ████</div><div class="pay">██% recurring ███</div><div>████ ██ ███ █████</div></div>').join('')||'<p>No matches.</p>';
const h=LOCKED;$('#hidden').textContent=h;$('#lockbox').style.display=h?'block':'none';}
['#q','#fn','#fp','#ft'].forEach(s=>$(s).addEventListener('input',draw));draw();
if(location.hash=='#thanks')$('#thanks').textContent='Thanks! Deal received.';
