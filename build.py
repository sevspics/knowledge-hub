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
.format-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:12px}
.format-card{background:var(--bg);border-radius:10px;padding:16px;border:1px solid var(--border)}
.format-header{display:flex;align-items:center;gap:8px;margin-bottom:12px}
.format-icon{font-size:20px}.format-name{font-size:14px;font-weight:700;flex:1}
.format-difficulty{font-size:10px;padding:2px 8px;border-radius:100px;font-family:'DM Mono',monospace;letter-spacing:2px}
.format-section{margin-bottom:8px}.format-section:last-child{margin-bottom:0}
.format-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);display:block;margin-bottom:2px}
.format-section p{font-size:13px;color:var(--text-secondary);line-height:1.5;margin:0}
.view-formats-btn{margin-top:12px;padding:8px 18px;border-radius:8px;border:1px solid var(--teal);background:rgba(13,148,136,0.06);color:var(--teal);font-size:13px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .15s}
.view-formats-btn:hover{background:var(--teal);color:#fff}
.format-card{position:relative;transition:opacity .3s ease}
.format-card.created{opacity:0.3}
.format-check{position:absolute;bottom:10px;right:10px;display:flex;align-items:center;gap:6px;cursor:pointer;font-size:11px;color:var(--text-muted);user-select:none}
.format-check input{width:16px;height:16px;cursor:pointer;accent-color:var(--teal)}
.format-check span{font-family:'DM Sans',sans-serif}
.tracker-bar{display:flex;align-items:center;gap:16px;margin-bottom:16px;flex-wrap:wrap}
.tracker-progress{flex:1;min-width:200px}
.tracker-progress-bg{height:8px;background:var(--border);border-radius:100px;overflow:hidden}
.tracker-progress-fill{height:100%;background:var(--teal);border-radius:100px;transition:width .3s}
.tracker-stat{font-size:13px;font-weight:600;color:var(--text-secondary);font-family:'DM Mono',monospace}
.creative-table{width:100%;border-collapse:separate;border-spacing:0}
.creative-table th{position:sticky;top:58px;background:var(--bg);text-align:left;padding:10px 12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);border-bottom:2px solid var(--border);z-index:5}
.creative-table td{padding:10px 12px;font-size:13px;border-bottom:1px solid var(--border);vertical-align:top;background:var(--surface)}
.creative-table tr:hover td{background:var(--tag-bg)}
.creative-table tr.created td{opacity:0.35}
.creative-table td.hook-cell{max-width:300px;color:var(--text-secondary);line-height:1.4}
.creative-table td.title-cell{font-weight:600;white-space:nowrap}
.creative-table td.check-cell{width:40px;text-align:center}
.creative-table td.check-cell input{width:16px;height:16px;cursor:pointer;accent-color:var(--teal)}
.creative-table td.format-cell{white-space:nowrap}
.format-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
@media(max-width:640px){.header h1{font-size:22px}.stats-row{gap:8px}.stat-card{min-width:100px;padding:10px 14px}.stat-num{font-size:20px}.entry-card{padding:16px}.entry-title{font-size:16px}.call-card{flex-direction:column;align-items:flex-start}.call-right{width:100%;justify-content:flex-start}.format-grid{grid-template-columns:1fr}.creative-table{font-size:12px}.creative-table th,.creative-table td{padding:8px 6px}.creative-table td.hook-cell{max-width:160px}}
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
<button class="nav-btn" data-view="creator" onclick="switchView('creator')">🎬 Content Creator</button>
<button class="nav-btn" data-view="tracker" onclick="switchView('tracker')">📋 Creative Tracker</button>
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
<div id="view-creator" class="hidden">
<input class="search-input" id="creator-search" placeholder="Search entries for content briefs..." oninput="renderCreator()">
<div class="chip-row" id="creator-cat-chips"></div>
<div class="chip-row sm" id="creator-funnel-chips"></div>
<div class="result-count" id="creator-result-count"></div>
<div id="creator-container"></div>
</div>
<div id="view-tracker" class="hidden">
<input class="search-input" id="tracker-search" placeholder="Search creatives..." oninput="renderTracker()">
<div class="chip-row" id="tracker-format-chips"></div>
<div class="chip-row" id="tracker-cat-chips"></div>
<div class="chip-row sm" id="tracker-status-chips"></div>
<div class="tracker-bar"><div class="tracker-stat" id="tracker-stat"></div><div class="tracker-progress"><div class="tracker-progress-bg"><div class="tracker-progress-fill" id="tracker-fill"></div></div></div></div>
<div style="overflow-x:auto"><table class="creative-table" id="tracker-table"></table></div>
</div>
</div>
<div class="footer">
<p id="footer-text"></p>
<p class="sub">Feed me more transcripts to grow the library. Every call you do is content for this hub.</p>
</div>
<script>
const CATEGORIES={strategy:{label:"Content Strategy",color:"#0D9488",icon:"📐"},hooks:{label:"Hooks & Scripting",color:"#F59E0B",icon:"🎣"},formats:{label:"Content Formats",color:"#8B5CF6",icon:"🎬"},workflow:{label:"Workflow & Production",color:"#3B82F6",icon:"⚙️"},platform:{label:"Platform & Algorithm",color:"#EC4899",icon:"📱"},brand:{label:"Personal Brand",color:"#EF4444",icon:"🔥"},sales:{label:"Sales Through Content",color:"#10B981",icon:"💰"},ai:{label:"AI & Tools",color:"#6366F1",icon:"🤖"},mindset:{label:"Mindset & Consistency",color:"#F97316",icon:"🧠"}};
const FORMATS={faceless:{label:"Faceless",icon:"\u{1F5A5}\uFE0F",difficulty:1,color:"#10B981"},meme:{label:"Memes",icon:"\u{1F602}",difficulty:2,color:"#84CC16"},candid:{label:"Candid",icon:"\u{1F4F1}",difficulty:3,color:"#F59E0B"},framed:{label:"Framed",icon:"\u{1F3AC}",difficulty:4,color:"#F97316"},"visual-storyteller":{label:"Visual Storyteller",icon:"\u{1F3A5}",difficulty:5,color:"#EF4444"},"talking-head":{label:"Talking Head",icon:"\u{1F5E3}\uFE0F",difficulty:6,color:"#DC2626"}};
const CALLS=__CALLS_DATA__;
const ENTRIES=__ENTRIES_DATA__;
CALLS.forEach(c=>{c.entryCount=ENTRIES.filter(e=>e.sourceId===c.id).length});
const stats={entries:ENTRIES.length,calls:CALLS.length,extracted:CALLS.filter(c=>c.entryCount>0).length,pending:CALLS.filter(c=>c.entryCount===0).length};
let currentView="knowledge",catFilter=null,funnelFilter=null,expandedId=null,callTypeFilter=null,creatorCatFilter=null,creatorFunnelFilter=null,creatorExpandedId=null,trackerFormatFilter=null,trackerCatFilter=null,trackerStatusFilter=null;
function makeBadge(l,c,s){return`<span class="badge${s?' sm':''}" style="background:${c}18;color:${c}">${l}</span>`}
function isCreated(eid,fmt){return localStorage.getItem('created_'+eid+'_'+fmt)==='1'}
function toggleCreated(eid,fmt,el){if(el)el.stopPropagation();if(isCreated(eid,fmt)){localStorage.removeItem('created_'+eid+'_'+fmt)}else{localStorage.setItem('created_'+eid+'_'+fmt,'1')}if(currentView==='creator')renderCreator();if(currentView==='tracker')renderTracker()}
function switchView(v){currentView=v;document.querySelectorAll('.nav-btn').forEach(b=>b.classList.toggle('active',b.dataset.view===v));['knowledge','calls','topics','creator','tracker'].forEach(w=>{document.getElementById('view-'+w).classList.toggle('hidden',v!==w)});if(v==='calls')renderCalls();if(v==='topics')renderTopics();if(v==='creator'){renderCreatorChips();renderCreator()}if(v==='tracker'){renderTrackerChips();renderTracker()}}
function renderEntries(){const q=document.getElementById('search').value.toLowerCase();const filtered=ENTRIES.filter(e=>{if(catFilter&&e.category!==catFilter)return false;if(funnelFilter&&!e.funnel.includes(funnelFilter)&&!e.funnel.includes("ALL"))return false;if(q){return e.title.toLowerCase().includes(q)||e.description.toLowerCase().includes(q)||e.tags.some(t=>t.includes(q))||e.context.toLowerCase().includes(q)}return true});document.getElementById('result-count').textContent=`Showing ${filtered.length} of ${ENTRIES.length} entries`;if(!filtered.length){document.getElementById('entries-container').innerHTML='<div class="empty"><div class="empty-icon">🔍</div><p>No entries match your filters. Try broadening your search.</p></div>';return}document.getElementById('entries-container').innerHTML=filtered.map(e=>{const cat=CATEGORIES[e.category];const call=CALLS.find(c=>c.id===e.sourceId);const isExp=expandedId===e.id;return`<div class="entry-card${isExp?' expanded':''}" style="border-left-color:${cat.color}" onclick="toggleEntry('${e.id}')"><div class="entry-top"><div class="entry-content"><div class="entry-badges"><span style="font-size:16px">${cat.icon}</span>${makeBadge(cat.label,cat.color)}${e.funnel.filter(f=>f!=='ALL').map(f=>makeBadge(f,'#64748B',true)).join('')}${makeBadge(e.type,'#94A3B8',true)}</div><h3 class="entry-title">${e.title}</h3><p class="entry-desc${isExp?'':' clamped'}">${e.description}</p></div><span class="entry-arrow">▼</span></div><div class="entry-detail"><div style="margin-bottom:12px"><div class="detail-label">Context</div><p class="detail-text italic">${e.context}</p></div><div class="detail-row"><div class="detail-col"><div class="detail-label">Source</div><p class="detail-text">${call?call.name:'Unknown'} (${call?call.date:''})</p></div><div class="detail-col"><div class="detail-label">Applies To</div><p class="detail-text">${e.businessTypes.join(', ')}</p></div></div><div class="tag-row">${e.tags.map(t=>`<span class="tag">#${t}</span>`).join('')}</div>${e.formats?`<button class="view-formats-btn" onclick="event.stopPropagation();goToFormats('${e.id}')">🎬 View Content Briefs</button>`:''}</div></div>`}).join('')}
function toggleEntry(id){expandedId=expandedId===id?null:id;renderEntries()}
function setCat(k){catFilter=catFilter===k?null:k;renderCatChips();renderEntries()}
function setFunnel(k){funnelFilter=funnelFilter===k?null:k;renderFunnelChips();renderEntries()}
function renderCatChips(){let h=`<button class="chip${!catFilter?' active':''}" onclick="setCat(null)">All Categories</button>`;Object.entries(CATEGORIES).forEach(([k,v])=>{const a=catFilter===k;h+=`<button class="chip" style="${a?`border-color:${v.color};background:${v.color}18;color:${v.color}`:''}" onclick="setCat('${k}')">${v.icon} ${v.label}</button>`});document.getElementById('cat-chips').innerHTML=h}
function renderFunnelChips(){const f={TOF:"Top of Funnel",MOF:"Middle of Funnel",BOF:"Bottom of Funnel"};let h=`<button class="chip sm${!funnelFilter?' active':''}" onclick="setFunnel(null)">All Stages</button>`;Object.entries(f).forEach(([k,v])=>{const a=funnelFilter===k;h+=`<button class="chip sm" style="${a?'border-color:#0D9488;background:rgba(13,148,136,.08);color:#0D9488':''}" onclick="setFunnel('${k}')">${v}</button>`});document.getElementById('funnel-chips').innerHTML=h}
function setCallType(t){callTypeFilter=callTypeFilter===t?null:t;renderCalls()}
function renderCalls(){const types=["1:1 Advisory","Group Advisory","BTS Sales","Audit","Podcast","BTS Production"];let ch=`<button class="chip sm${!callTypeFilter?' active':''}" onclick="setCallType(null)">All (${CALLS.length})</button>`;types.forEach(t=>{const n=CALLS.filter(c=>c.type===t).length;if(!n)return;const a=callTypeFilter===t;ch+=`<button class="chip sm" style="${a?'border-color:#0D9488;background:rgba(13,148,136,.08);color:#0D9488':''}" onclick="setCallType('${t}')">${t} (${n})</button>`});document.getElementById('call-type-chips').innerHTML=ch;const tc={"1:1 Advisory":"#6366F1","Group Advisory":"#0D9488","BTS Sales":"#F59E0B",Audit:"#EF4444",Podcast:"#EC4899","BTS Production":"#94A3B8"};const fl=(callTypeFilter?CALLS.filter(c=>c.type===callTypeFilter):CALLS).sort((a,b)=>b.date.localeCompare(a.date));document.getElementById('calls-container').innerHTML=fl.map(c=>`<div class="call-card${c.entryCount>0?' has-entries':''}"><div class="call-info"><div class="call-name-row"><span class="call-name">${c.name}</span>${makeBadge(c.type,tc[c.type]||'#94A3B8',true)}</div><div class="call-meta">${c.date} · ${c.duration?c.duration+'min':'Duration TBD'} · ${c.attendees.join(', ')}</div></div><div class="call-right">${c.entryCount>0?`<span class="call-count">${c.entryCount} entries</span>`:`<span class="call-pending">Awaiting extraction</span>`}${c.link?`<a class="call-link" href="${c.link}" target="_blank" rel="noopener">Fathom ↗</a>`:''}</div></div>`).join('')}
function renderTopics(){document.getElementById('topics-container').innerHTML=Object.entries(CATEGORIES).map(([k,cat])=>{const ce=ENTRIES.filter(e=>e.category===k);const ty={};ce.forEach(e=>{ty[e.type]=(ty[e.type]||0)+1});return`<div class="topic-card" style="border-top-color:${cat.color}" onclick="setCat('${k}');switchView('knowledge')"><div class="topic-icon">${cat.icon}</div><div class="topic-name">${cat.label}</div><div class="topic-count" style="color:${cat.color}">${ce.length}</div><div class="topic-types">${Object.entries(ty).map(([t,n])=>`<span class="topic-type">${n} ${t}${n>1?'s':''}</span>`).join('')}</div></div>`}).join('')}
function goToFormats(id){creatorCatFilter=null;creatorFunnelFilter=null;creatorExpandedId=id;switchView('creator');setTimeout(()=>{const el=document.querySelector('#creator-container .expanded');if(el)el.scrollIntoView({behavior:'smooth',block:'start'})},50)}
function toggleCreatorEntry(id){creatorExpandedId=creatorExpandedId===id?null:id;renderCreator()}
function setCreatorCat(k){creatorCatFilter=creatorCatFilter===k?null:k;renderCreatorChips();renderCreator()}
function setCreatorFunnel(k){creatorFunnelFilter=creatorFunnelFilter===k?null:k;renderCreatorChips();renderCreator()}
function renderCreatorChips(){let h=`<button class="chip${!creatorCatFilter?' active':''}" onclick="setCreatorCat(null)">All Categories</button>`;Object.entries(CATEGORIES).forEach(([k,v])=>{const a=creatorCatFilter===k;h+=`<button class="chip" style="${a?`border-color:${v.color};background:${v.color}18;color:${v.color}`:''}" onclick="setCreatorCat('${k}')">${v.icon} ${v.label}</button>`});document.getElementById('creator-cat-chips').innerHTML=h;const f={TOF:"Top of Funnel",MOF:"Middle of Funnel",BOF:"Bottom of Funnel"};let fh=`<button class="chip sm${!creatorFunnelFilter?' active':''}" onclick="setCreatorFunnel(null)">All Stages</button>`;Object.entries(f).forEach(([k,v])=>{const a=creatorFunnelFilter===k;fh+=`<button class="chip sm" style="${a?'border-color:#0D9488;background:rgba(13,148,136,.08);color:#0D9488':''}" onclick="setCreatorFunnel('${k}')">${v}</button>`});document.getElementById('creator-funnel-chips').innerHTML=fh}
function renderCreator(){const q=document.getElementById('creator-search').value.toLowerCase();const withFormats=ENTRIES.filter(e=>e.formats);const filtered=withFormats.filter(e=>{if(creatorCatFilter&&e.category!==creatorCatFilter)return false;if(creatorFunnelFilter&&!e.funnel.includes(creatorFunnelFilter)&&!e.funnel.includes("ALL"))return false;if(q){return e.title.toLowerCase().includes(q)||e.description.toLowerCase().includes(q)||e.tags.some(t=>t.includes(q))}return true});document.getElementById('creator-result-count').textContent=`Showing ${filtered.length} of ${withFormats.length} entries with content briefs`;if(!filtered.length){document.getElementById('creator-container').innerHTML='<div class="empty"><div class="empty-icon">🎬</div><p>No entries with content briefs match your filters.</p></div>';return}document.getElementById('creator-container').innerHTML=filtered.map(e=>{const cat=CATEGORIES[e.category];const isExp=creatorExpandedId===e.id;return`<div class="entry-card${isExp?' expanded':''}" style="border-left-color:${cat.color}" onclick="toggleCreatorEntry('${e.id}')"><div class="entry-top"><div class="entry-content"><div class="entry-badges"><span style="font-size:16px">${cat.icon}</span>${makeBadge(cat.label,cat.color)}${e.funnel.filter(f=>f!=='ALL').map(f=>makeBadge(f,'#64748B',true)).join('')}</div><h3 class="entry-title">${e.title}</h3><p class="entry-desc${isExp?'':' clamped'}">${e.description}</p></div><span class="entry-arrow">▼</span></div><div class="entry-detail"><div class="format-grid">${Object.entries(FORMATS).map(([key,fmt])=>{const b=e.formats[key];if(!b)return'';const done=isCreated(e.id,key);return`<div class="format-card${done?' created':''}" style="border-top:3px solid ${fmt.color}"><div class="format-header"><span class="format-icon">${fmt.icon}</span><span class="format-name">${fmt.label}</span><span class="format-difficulty" style="background:${fmt.color}18;color:${fmt.color}">${'\u25CF'.repeat(fmt.difficulty)}${'\u25CB'.repeat(6-fmt.difficulty)}</span></div><div class="format-section"><span class="format-label">Hook</span><p>${b.hook}</p></div><div class="format-section"><span class="format-label">Body</span><p>${b.body}</p></div><div class="format-section"><span class="format-label">CTA</span><p>${b.cta}</p></div><div class="format-section"><span class="format-label">Notes</span><p>${b.notes}</p></div><label class="format-check" onclick="event.stopPropagation()"><input type="checkbox" ${done?'checked':''} onchange="toggleCreated('${e.id}','${key}',event)"><span>Created</span></label></div>`}).join('')}</div></div></div>`}).join('')}
function setTrackerFormat(k){trackerFormatFilter=trackerFormatFilter===k?null:k;renderTrackerChips();renderTracker()}
function setTrackerCat(k){trackerCatFilter=trackerCatFilter===k?null:k;renderTrackerChips();renderTracker()}
function setTrackerStatus(k){trackerStatusFilter=trackerStatusFilter===k?null:k;renderTrackerChips();renderTracker()}
function renderTrackerChips(){let fh=`<button class="chip${!trackerFormatFilter?' active':''}" onclick="setTrackerFormat(null)">All Formats</button>`;Object.entries(FORMATS).forEach(([k,v])=>{const a=trackerFormatFilter===k;fh+=`<button class="chip" style="${a?`border-color:${v.color};background:${v.color}18;color:${v.color}`:''}" onclick="setTrackerFormat('${k}')">${v.icon} ${v.label}</button>`});document.getElementById('tracker-format-chips').innerHTML=fh;let ch=`<button class="chip${!trackerCatFilter?' active':''}" onclick="setTrackerCat(null)">All Categories</button>`;Object.entries(CATEGORIES).forEach(([k,v])=>{const a=trackerCatFilter===k;ch+=`<button class="chip" style="${a?`border-color:${v.color};background:${v.color}18;color:${v.color}`:''}" onclick="setTrackerCat('${k}')">${v.icon} ${v.label}</button>`});document.getElementById('tracker-cat-chips').innerHTML=ch;let sh=`<button class="chip sm${!trackerStatusFilter?' active':''}" onclick="setTrackerStatus(null)">All Status</button>`;sh+=`<button class="chip sm" style="${trackerStatusFilter==='todo'?'border-color:#EF4444;background:rgba(239,68,68,.08);color:#EF4444':''}" onclick="setTrackerStatus('todo')">To Do</button>`;sh+=`<button class="chip sm" style="${trackerStatusFilter==='done'?'border-color:#10B981;background:rgba(16,185,129,.08);color:#10B981':''}" onclick="setTrackerStatus('done')">Created</button>`;document.getElementById('tracker-status-chips').innerHTML=sh}
function renderTracker(){const q=document.getElementById('tracker-search').value.toLowerCase();const rows=[];ENTRIES.forEach(e=>{if(!e.formats)return;Object.entries(FORMATS).forEach(([fk,fmt])=>{if(!e.formats[fk])return;const done=isCreated(e.id,fk);rows.push({entry:e,formatKey:fk,format:fmt,brief:e.formats[fk],done:done})})});const filtered=rows.filter(r=>{if(trackerFormatFilter&&r.formatKey!==trackerFormatFilter)return false;if(trackerCatFilter&&r.entry.category!==trackerCatFilter)return false;if(trackerStatusFilter==='todo'&&r.done)return false;if(trackerStatusFilter==='done'&&!r.done)return false;if(q){return r.entry.title.toLowerCase().includes(q)||r.brief.hook.toLowerCase().includes(q)||r.formatKey.includes(q)}return true});const totalCreatives=rows.length;const totalDone=rows.filter(r=>r.done).length;const pct=totalCreatives?Math.round(totalDone/totalCreatives*100):0;document.getElementById('tracker-stat').textContent=`${totalDone} / ${totalCreatives} created (${pct}%)`;document.getElementById('tracker-fill').style.width=pct+'%';let h=`<thead><tr><th class="check-cell"></th><th>Entry</th><th>Format</th><th>Category</th><th>Hook</th></tr></thead><tbody>`;filtered.forEach(r=>{const cat=CATEGORIES[r.entry.category];h+=`<tr class="${r.done?'created':''}"><td class="check-cell"><input type="checkbox" ${r.done?'checked':''} onchange="toggleCreated('${r.entry.id}','${r.formatKey}',event)"></td><td class="title-cell">${r.entry.title}</td><td class="format-cell"><span class="format-dot" style="background:${r.format.color}"></span>${r.format.icon} ${r.format.label}</td><td>${cat.icon} ${cat.label}</td><td class="hook-cell">${r.brief.hook}</td></tr>`});h+=`</tbody>`;document.getElementById('tracker-table').innerHTML=h}
document.getElementById('stat-entries').textContent=stats.entries;document.getElementById('stat-calls').textContent=stats.calls;document.getElementById('stat-extracted').textContent=stats.extracted;document.getElementById('stat-pending').textContent=stats.pending;document.getElementById('footer-text').textContent=`Sev's Knowledge Hub · V2.0 · ${stats.entries} entries from ${stats.extracted} calls · ${stats.pending} calls awaiting extraction`;
renderCatChips();renderFunnelChips();renderEntries();
</script>
</body>
</html>"""

if __name__ == "__main__":
    build()
