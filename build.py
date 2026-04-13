#!/usr/bin/env python3
"""
Sev's Knowledge Hub - Build Script
Generates the interactive HTML file from calls.json and entries.json
Usage: python build.py
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "docs")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

def build():
    calls = load_json("calls.json")
    entries = load_json("entries.json")

    calls_js = json.dumps(calls, indent=2)
    entries_js = json.dumps(entries, indent=2)

    # Count stats
    call_ids_with_entries = set(e["sourceId"] for e in entries)
    extracted = sum(1 for c in calls if c["id"] in call_ids_with_entries)
    pending = len(calls) - extracted

    html = HTML_TEMPLATE.replace("__CALLS_DATA__", calls_js)
    html = html.replace("__ENTRIES_DATA__", entries_js)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    outpath = os.path.join(OUTPUT_DIR, "knowledge-hub.html")
    with open(outpath, "w") as f:
        f.write(html)

    print(f"Built knowledge-hub.html")
    print(f"  {len(entries)} entries from {len(calls)} calls")
    print(f"  {extracted} calls extracted, {pending} awaiting extraction")
    print(f"  Output: {outpath}")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sev's Knowledge Hub</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --surface:#ffffff;--bg:#F8FAFC;--text-primary:#0F172A;--text-secondary:#475569;
  --text-muted:#94A3B8;--border:#E2E8F0;--tag-bg:#F1F5F9;--teal:#0D9488;
  --amber:#F59E0B;--violet:#8B5CF6;--blue:#3B82F6;--pink:#EC4899;--red:#EF4444;
  --emerald:#10B981;--indigo:#6366F1;--orange:#F97316;
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text-primary);-webkit-font-smoothing:antialiased}
.header{background:#0F172A;padding:32px 24px 24px;color:#fff}
.header-inner{max-width:960px;margin:0 auto}
.header-title-row{display:flex;align-items:center;gap:12px;margin-bottom:4px}
.header-title-row span{font-size:28px}
.header h1{font-size:28px;font-weight:700;font-family:'DM Serif Display',serif}
.header p{font-size:14px;color:#94A3B8;margin:4px 0 20px;max-width:600px}
.stats-row{display:flex;gap:16px;flex-wrap:wrap}
.stat-card{background:rgba(255,255,255,0.06);border-radius:10px;padding:12px 20px;min-width:120px}
.stat-num{font-size:24px;font-weight:700;font-family:'DM Mono',monospace;color:#fff}
.stat-num.teal{color:var(--teal)}.stat-num.amber{color:var(--amber)}
.stat-label{font-size:11px;color:#94A3B8;letter-spacing:0.5px}
.nav{background:#fff;border-bottom:1px solid var(--border);position:sticky;top:0;z-index:10}
.nav-inner{max-width:960px;margin:0 auto;display:flex;padding:0 24px}
.nav-btn{padding:14px 20px;border:none;background:none;cursor:pointer;font-size:14px;font-weight:500;color:var(--text-muted);border-bottom:3px solid transparent;transition:all .15s;font-family:'DM Sans',sans-serif}
.nav-btn:hover{color:var(--text-secondary)}.nav-btn.active{font-weight:700;color:var(--text-primary);border-bottom-color:var(--teal)}
.main{max-width:960px;margin:0 auto;padding:24px}
.search-input{width:100%;padding:14px 20px;border-radius:10px;border:1px solid var(--border);font-size:15px;background:#fff;outline:none;margin-bottom:16px;font-family:'DM Sans',sans-serif}
.search-input:focus{border-color:var(--teal);box-shadow:0 0 0 3px rgba(13,148,136,0.1)}
.chip-row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}.chip-row.sm{margin-bottom:20px}
.chip{padding:6px 14px;border-radius:100px;border:1px solid var(--border);background:#fff;color:var(--text-secondary);font-size:12px;font-weight:600;cursor:pointer;transition:all .15s;font-family:'DM Sans',sans-serif;white-space:nowrap}
.chip:hover{border-color:var(--text-muted)}.chip.active{background:#0F172A;color:#fff;border-color:#0F172A}.chip.sm{padding:4px 12px;font-size:11px}
.result-count{font-size:13px;color:var(--text-muted);margin-bottom:12px}
.badge{display:inline-block;padding:3px 10px;border-radius:100px;font-size:11px;font-weight:600;letter-spacing:.5px;white-space:nowrap}
.badge.sm{padding:2px 8px;font-size:10px}
.entry-card{background:var(--surface);border-radius:12px;padding:20px 24px;margin-bottom:12px;cursor:pointer;border-left:4px solid transparent;box-shadow:0 1px 3px rgba(0,0,0,.04);transition:all .2s ease}
.entry-card:hover{box-shadow:0 2px 8px rgba(0,0,0,.08)}.entry-card.expanded{box-shadow:0 4px 20px rgba(0,0,0,.08)}
.entry-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
.entry-content{flex:1}.entry-badges{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
.entry-title{font-size:18px;font-weight:700;margin:0 0 6px;line-height:1.3}
.entry-desc{font-size:14px;color:var(--text-secondary);margin:0;line-height:1.5}
.entry-desc.clamped{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.entry-arrow{font-size:18px;color:var(--text-muted);flex-shrink:0;transition:transform .2s}
.entry-card.expanded .entry-arrow{transform:rotate(180deg)}
.entry-detail{margin-top:16px;padding-top:16px;border-top:1px solid var(--border);display:none}
.entry-card.expanded .entry-detail{display:block}
.detail-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px}
.detail-text{font-size:13px;color:var(--text-secondary);margin:0;line-height:1.5}.detail-text.italic{font-style:italic}
.detail-row{display:flex;gap:24px;flex-wrap:wrap;margin:12px 0}
.detail-col .detail-text{color:var(--text-primary)}
.tag-row{display:flex;gap:6px;flex-wrap:wrap}
.tag{font-size:10px;padding:2px 8px;border-radius:4px;background:var(--tag-bg);color:var(--text-muted);font-family:'DM Mono',monospace}
.call-card{background:var(--surface);border-radius:12px;padding:16px 20px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:12px;border-left:4px solid #CBD5E1}
.call-card.has-entries{border-left-color:var(--teal)}
.call-info{flex:1}.call-name-row{display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap}
.call-name{font-size:15px;font-weight:700}.call-meta{font-size:12px;color:var(--text-muted)}
.call-right{display:flex;align-items:center;gap:12px;flex-shrink:0}
.call-count{font-size:12px;font-weight:700;color:var(--teal);background:rgba(13,148,136,.08);padding:2px 10px;border-radius:100px}
.call-pending{font-size:11px;color:var(--amber);font-weight:600;background:rgba(245,158,11,.08);padding:2px 10px;border-radius:100px}
.call-link{font-size:12px;color:var(--blue);text-decoration:none;font-weight:600}.call-link:hover{text-decoration:underline}
.topic-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.topic-card{background:#fff;border-radius:14px;padding:24px;cursor:pointer;border-top:4px solid var(--teal);box-shadow:0 1px 4px rgba(0,0,0,.06);transition:transform .15s,box-shadow .15s}
.topic-card:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1)}
.topic-icon{font-size:32px;margin-bottom:8px}.topic-name{font-size:18px;font-weight:700;margin:0 0 4px}
.topic-count{font-size:28px;font-weight:700;font-family:'DM Mono',monospace;margin-bottom:8px}
.topic-types{display:flex;gap:6px;flex-wrap:wrap}
.topic-type{font-size:10px;padding:2px 8px;border-radius:4px;background:var(--tag-bg);color:var(--text-muted)}
.footer{text-align:center;padding:32px 24px;font-size:12px;color:var(--text-muted);border-top:1px solid var(--border);margin-top:48px}
.footer p{margin:0}.footer .sub{margin-top:4px;font-size:11px}
.empty{text-align:center;padding:48px 24px;color:var(--text-muted)}.empty-icon{font-size:32px;margin-bottom:8px}
.hidden{display:none !important}
@media(max-width:640px){.header h1{font-size:22px}.stats-row{gap:8px}.stat-card{min-width:100px;padding:10px 14px}.stat-num{font-size:20px}.entry-card{padding:16px}.entry-title{font-size:16px}.call-card{flex-direction:column;align-items:flex-start}.call-right{width:100%;justify-content:flex-start}}
</style>
</head>
<body>
<div class="header"><div class="header-inner">
<div class="header-title-row"><span>🧠</span><h1>Sev's Knowledge Hub</h1></div>
<p>Every framework, tactic, case study, and rant from advisory calls, sales conversations, audits, and podcasts. Searchable. Filterable. Growing.</p>
<div class="stats-row">
<div class="stat-card"><div class="stat-num teal" id="stat-entries">0</div><div class="stat-label">Knowledge Entries</div></div>
<div class="stat-card"><div class="stat-num" id="stat-calls">0</div><div class="stat-label">Calls Indexed</div></div>
<div class="stat-card"><div class="stat-num" id="stat-extracted">0</div><div class="stat-label">Fully Extracted</div></div>
<div class="stat-card"><div class="stat-num amber" id="stat-pending">0</div><div class="stat-label">Awaiting Extraction</div></div>
</div></div></div>
<div class="nav"><div class="nav-inner">
<button class="nav-btn active" data-view="knowledge" onclick="switchView('knowledge')">📚 Knowledge Base</button>
<button class="nav-btn" data-view="calls" onclick="switchView('calls')">📞 Call Archive</button>
<button class="nav-btn" data-view="topics" onclick="switchView('topics')">🗺️ Topic Explorer</button>
</div></div>
<div class="main">
<div id="view-knowledge">
<input class="search-input" id="search" placeholder="Search frameworks, tactics, case studies, tags..." oninput="renderEntries()">
<div class="chip-row" id="cat-chips"></div>
<div class="chip-row sm" id="funnel-chips"></div>
<div class="result-count" id="result-count"></div>
<div id="entries-container"></div>
</div>
<div id="view-calls" class="hidden">
<div class="chip-row sm" id="call-type-chips"></div>
<div id="calls-container"></div>
</div>
<div id="view-topics" class="hidden">
<div class="topic-grid" id="topics-container"></div>
</div>
</div>
<div class="footer">
<p id="footer-text"></p>
<p class="sub">Feed me more transcripts to grow the library. Every call you do is content for this hub.</p>
</div>
<script>
const CATEGORIES={strategy:{label:"Content Strategy",color:"#0D9488",icon:"📐"},hooks:{label:"Hooks & Scripting",color:"#F59E0B",icon:"🎣"},formats:{label:"Content Formats",color:"#8B5CF6",icon:"🎬"},workflow:{label:"Workflow & Production",color:"#3B82F6",icon:"⚙️"},platform:{label:"Platform & Algorithm",color:"#EC4899",icon:"📱"},brand:{label:"Personal Brand",color:"#EF4444",icon:"🔥"},sales:{label:"Sales Through Content",color:"#10B981",icon:"💰"},ai:{label:"AI & Tools",color:"#6366F1",icon:"🤖"},mindset:{label:"Mindset & Consistency",color:"#F97316",icon:"🧠"}};
const CALLS=__CALLS_DATA__;
const ENTRIES=__ENTRIES_DATA__;
CALLS.forEach(c=>{c.entryCount=ENTRIES.filter(e=>e.sourceId===c.id).length});
const stats={entries:ENTRIES.length,calls:CALLS.length,extracted:CALLS.filter(c=>c.entryCount>0).length,pending:CALLS.filter(c=>c.entryCount===0).length};
let currentView="knowledge",catFilter=null,funnelFilter=null,expandedId=null,callTypeFilter=null;
function makeBadge(l,c,s){return`<span class="badge${s?' sm':''}" style="background:${c}18;color:${c}">${l}</span>`}
function switchView(v){currentView=v;document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.view===v));document.getElementById('view-knowledge').classList.toggle('hidden',v!=='knowledge');document.getElementById('view-calls').classList.toggle('hidden',v!=='calls');document.getElementById('view-topics').classList.toggle('hidden',v!=='topics');if(v==='calls')renderCalls();if(v==='topics')renderTopics()}
function renderEntries(){const q=document.getElementById('search').value.toLowerCase();const filtered=ENTRIES.filter(e=>{if(catFilter&&e.category!==catFilter)return false;if(funnelFilter&&!e.funnel.includes(funnelFilter)&&!e.funnel.includes("ALL"))return false;if(q){return e.title.toLowerCase().includes(q)||e.description.toLowerCase().includes(q)||e.tags.some(t=>t.includes(q))||e.context.toLowerCase().includes(q)}return true});document.getElementById('result-count').textContent=`Showing ${filtered.length} of ${ENTRIES.length} entries`;if(!filtered.length){document.getElementById('entries-container').innerHTML='<div class="empty"><div class="empty-icon">🔍</div><p>No entries match your filters. Try broadening your search.</p></div>';return}document.getElementById('entries-container').innerHTML=filtered.map(e=>{const cat=CATEGORIES[e.category];const call=CALLS.find(c=>c.id===e.sourceId);const isExp=expandedId===e.id;return`<div class="entry-card${isExp?' expanded':''}" style="border-left-color:${cat.color}" onclick="toggleEntry('${e.id}')"><div class="entry-top"><div class="entry-content"><div class="entry-badges"><span style="font-size:16px">${cat.icon}</span>${makeBadge(cat.label,cat.color)}${e.funnel.filter(f=>f!=='ALL').map(f=>makeBadge(f,'#64748B',true)).join('')}${makeBadge(e.type,'#94A3B8',true)}</div><h3 class="entry-title">${e.title}</h3><p class="entry-desc${isExp?'':' clamped'}">${e.description}</p></div><span class="entry-arrow">▼</span></div><div class="entry-detail"><div style="margin-bottom:12px"><div class="detail-label">Context</div><p class="detail-text italic">${e.context}</p></div><div class="detail-row"><div class="detail-col"><div class="detail-label">Source</div><p class="detail-text">${call?call.name:'Unknown'} (${call?call.date:''})</p></div><div class="detail-col"><div class="detail-label">Applies To</div><p class="detail-text">${e.businessTypes.join(', ')}</p></div></div><div class="tag-row">${e.tags.map(t=>`<span class="tag">#${t}</span>`).join('')}</div></div></div>`}).join('')}
function toggleEntry(id){expandedId=expandedId===id?null:id;renderEntries()}
function setCat(k){catFilter=catFilter===k?null:k;renderCatChips();renderEntries()}
function setFunnel(k){funnelFilter=funnelFilter===k?null:k;renderFunnelChips();renderEntries()}
function renderCatChips(){let h=`<button class="chip${!catFilter?' active':''}" onclick="setCat(null)">All Categories</button>`;Object.entries(CATEGORIES).forEach(([k,v])=>{const a=catFilter===k;h+=`<button class="chip" style="${a?`border-color:${v.color};background:${v.color}18;color:${v.color}`:''}" onclick="setCat('${k}')">${v.icon} ${v.label}</button>`});document.getElementById('cat-chips').innerHTML=h}
function renderFunnelChips(){const f={TOF:"Top of Funnel",MOF:"Middle of Funnel",BOF:"Bottom of Funnel"};let h=`<button class="chip sm${!funnelFilter?' active':''}" onclick="setFunnel(null)">All Stages</button>`;Object.entries(f).forEach(([k,v])=>{const a=funnelFilter===k;h+=`<button class="chip sm" style="${a?'border-color:#0D9488;background:rgba(13,148,136,.08);color:#0D9488':''}" onclick="setFunnel('${k}')">${v}</button>`});document.getElementById('funnel-chips').innerHTML=h}
function setCallType(t){callTypeFilter=callTypeFilter===t?null:t;renderCalls()}
function renderCalls(){const types=["1:1 Advisory","Group Advisory","BTS Sales","Audit","Podcast","BTS Production"];let ch=`<button class="chip sm${!callTypeFilter?' active':''}" onclick="setCallType(null)">All (${CALLS.length})</button>`;types.forEach(t=>{const n=CALLS.filter(c=>c.type===t).length;if(!n)return;const a=callTypeFilter===t;ch+=`<button class="chip sm" style="${a?'border-color:#0D9488;background:rgba(13,148,136,.08);color:#0D9488':''}" onclick="setCallType('${t}')">${t} (${n})</button>`});document.getElementById('call-type-chips').innerHTML=ch;const tc={"1:1 Advisory":"#6366F1","Group Advisory":"#0D9488","BTS Sales":"#F59E0B",Audit:"#EF4444",Podcast:"#EC4899","BTS Production":"#94A3B8"};const fl=(callTypeFilter?CALLS.filter(c=>c.type===callTypeFilter):CALLS).sort((a,b)=>b.date.localeCompare(a.date));document.getElementById('calls-container').innerHTML=fl.map(c=>`<div class="call-card${c.entryCount>0?' has-entries':''}"><div class="call-info"><div class="call-name-row"><span class="call-name">${c.name}</span>${makeBadge(c.type,tc[c.type]||'#94A3B8',true)}</div><div class="call-meta">${c.date} · ${c.duration?c.duration+'min':'Duration TBD'} · ${c.attendees.join(', ')}</div></div><div class="call-right">${c.entryCount>0?`<span class="call-count">${c.entryCount} entries</span>`:`<span class="call-pending">Awaiting extraction</span>`}${c.link?`<a class="call-link" href="${c.link}" target="_blank" rel="noopener">Fathom ↗</a>`:''}</div></div>`).join('')}
function renderTopics(){document.getElementById('topics-container').innerHTML=Object.entries(CATEGORIES).map(([k,cat])=>{const ce=ENTRIES.filter(e=>e.category===k);const ty={};ce.forEach(e=>{ty[e.type]=(ty[e.type]||0)+1});return`<div class="topic-card" style="border-top-color:${cat.color}" onclick="setCat('${k}');switchView('knowledge')"><div class="topic-icon">${cat.icon}</div><div class="topic-name">${cat.label}</div><div class="topic-count" style="color:${cat.color}">${ce.length}</div><div class="topic-types">${Object.entries(ty).map(([t,n])=>`<span class="topic-type">${n} ${t}${n>1?'s':''}</span>`).join('')}</div></div>`}).join('')}
document.getElementById('stat-entries').textContent=stats.entries;document.getElementById('stat-calls').textContent=stats.calls;document.getElementById('stat-extracted').textContent=stats.extracted;document.getElementById('stat-pending').textContent=stats.pending;document.getElementById('footer-text').textContent=`Sev's Knowledge Hub · V2.0 · ${stats.entries} entries from ${stats.extracted} calls · ${stats.pending} calls awaiting extraction`;
renderCatChips();renderFunnelChips();renderEntries();
</script>
</body>
</html>"""

if __name__ == "__main__":
    build()
