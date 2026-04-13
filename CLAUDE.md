# Sev's Knowledge Hub - Claude Code Instructions

## What This Project Is

A searchable knowledge library built from Sev's advisory calls, sales conversations, coaching sessions, audits, and podcast episodes. Every distinct teaching point, framework, tactic, case study, and mindset lesson gets extracted and tagged.

## Project Structure

```
knowledge-hub/
├── CLAUDE.md           ← You're reading this
├── data/
│   ├── calls.json      ← Every call indexed (metadata only)
│   └── entries.json    ← Every knowledge entry extracted
├── transcripts/        ← Drop raw transcripts here for processing
├── build.py            ← Generates the HTML hub from JSON data
└── docs/
    └── knowledge-hub.html  ← The final interactive HTML (served by GitHub Pages)
```

## Hosting

This project is hosted on GitHub Pages serving from the `docs/` folder.
After any update to the HTML, push to GitHub and the live site updates within 60 seconds.

## The Workflow

When Sev says **"process this call"**, **"extract from this transcript"**, or **"process and push"**:

### Step 1: Identify the Call Metadata
Extract from the transcript or ask Sev:
- **Call name** (e.g., "Group Advisory #2", "BTS Sales - ClientName")
- **Date** (YYYY-MM-DD)
- **Type**: One of: `1:1 Advisory`, `Group Advisory`, `BTS Sales`, `Audit`, `Podcast`, `BTS Production`
- **Attendees**: List of names
- **Fathom link**: If available (format: `https://fathom.video/calls/XXXXXXXXX`)
- **Duration**: In minutes

Create a unique `id` using the pattern:
- Group advisory: `group-apr13`, `group-apr20`
- 1:1 advisory: `daecian-s9`, `abbey-s2`
- BTS sales: `bts-clientname`
- Other: `audit-name`, `podcast-name`

### Step 2: Extract Knowledge Entries
Read the entire transcript. Extract every distinct teaching point that meets these criteria:

**INCLUDE:**
- Frameworks with a name or structure (e.g., "The 5 Content Pillars")
- Tactical advice that can be applied by others (e.g., "scrape competitor questions")
- Case studies with specific numbers or outcomes (e.g., "$10K from 1,100 views")
- Mindset shifts or reframes (e.g., "searchable beats viral")
- Tool recommendations with workflow details (e.g., "DJI Osmo Pocket 3 setup")
- AI/tech workflows (e.g., "voice memo to AI transcription")
- Sales techniques (e.g., "qualify the decision maker in first 5 minutes")
- Resource recommendations (e.g., "Rick Rubin's Creative Act")

**EXCLUDE:**
- Operational logistics (scheduling, payment processing, onboarding steps)
- Small talk or pleasantries
- Repetitions of advice already in entries.json (check first!)
- Client-specific details that aren't universally applicable
- Standard BTS workshop pitch details (already captured in entry `rezz-06`)

### Step 3: Write Each Entry
Every entry follows this exact schema:

```json
{
  "id": "prefix-XX",
  "title": "Short, Memorable Title",
  "category": "one of the 9 categories",
  "funnel": ["TOF", "MOF", "BOF", or "ALL"],
  "sourceId": "matching call id",
  "type": "framework | tactic | case-study | mindset | tool | resource",
  "description": "2-4 sentences. Written in Sev's voice. Direct, assertive, no filler. Include the specific advice, not just a summary. Someone reading this should be able to ACT on it without watching the original call.",
  "context": "1-2 sentences. Who was this given to, what was their business, why did this come up. This is the backstory that makes the advice concrete.",
  "businessTypes": ["All"] or specific types like ["Personal Trainer", "Agency"],
  "tags": ["lowercase", "hyphenated", "reuse-existing-tags"]
}
```

**Entry ID format:** Use the call id prefix + sequential number.
- Group advisory entries: `ga2-01`, `ga2-02`
- Daecian sessions: `d9-01`, `d9-02`
- BTS sales: `bts-16`, `bts-17`
- Other: `kb-07`, `ab-06`, etc.

### Step 4: Check for Duplicates
Before adding any entry, search `entries.json` for similar concepts. If an existing entry covers the same ground:
- **Same advice, different context**: Skip it (don't duplicate)
- **Same concept, meaningfully expanded**: Update the existing entry's description
- **Related but distinct**: Add it and cross-reference via tags

### Step 5: Update the JSON Files and Build
1. Add the new call object to `data/calls.json`
2. Add all new entries to `data/entries.json`
3. Run `python build.py` to regenerate the HTML in `docs/`

### Step 6: Push Live (if Sev says "push" or "push live")
```bash
git add -A
git commit -m "Add [X] entries from [call name] ([date])"
git push
```
The live GitHub Pages site updates within ~60 seconds.

### Step 7: Report Back
Tell Sev:
- How many entries were extracted
- List each entry title and category
- Flag any entries that were close to duplicates
- Note anything from the call that was interesting but didn't qualify as an entry

---

## The 9 Categories

| Key | Label | What Goes Here |
|-----|-------|----------------|
| `strategy` | Content Strategy | Frameworks for what to create, content planning, pillars, funnels |
| `hooks` | Hooks & Scripting | First 2 seconds, curiosity gaps, hook formulas, script structure |
| `formats` | Content Formats | Video types, memes, carousels, static, long-form vs short |
| `workflow` | Workflow & Production | Recording setups, editing tools, batch processes, SOPs |
| `platform` | Platform & Algorithm | Instagram, YouTube, TikTok, algorithm behavior, search vs discovery |
| `brand` | Personal Brand | USPersonality, educator vs journeyman, WIIFM, positioning |
| `sales` | Sales Through Content | ROI closes, testimonials, assignment selling, pricing |
| `ai` | AI & Tools | Claude workflows, ManyChat, NotebookLM, GEO, quiz builders |
| `mindset` | Mindset & Consistency | Consistency, creative blocks, volume philosophy, reframes |

---

## Entry Types

| Type | When to Use |
|------|-------------|
| `framework` | Named system with structure (e.g., "The 5 Content Pillars", "80/20 Rule") |
| `tactic` | Specific actionable technique (e.g., "scrape competitor questions") |
| `case-study` | Real example with numbers/outcomes (e.g., "Wayne got 500K views") |
| `mindset` | Mental model or reframe (e.g., "searchable beats viral") |
| `tool` | Equipment or software recommendation with usage details |
| `resource` | Book, course, person, or reference recommendation |

---

## Funnel Stages

| Stage | Meaning |
|-------|---------|
| `TOF` | Top of Funnel: Awareness, reach, memes, relatable pain points |
| `MOF` | Middle of Funnel: Education, trust-building, answering questions |
| `BOF` | Bottom of Funnel: Proof, testimonials, sales conversion, pricing |
| `ALL` | Applies across all stages |

---

## Existing Tags (reuse these before creating new ones)

### Core Concepts
`they-ask-you-answer`, `organic`, `compound`, `volume`, `testing`, `data-driven`, `consistency`, `searchability`

### Content
`hooks`, `first-2-seconds`, `memes`, `relatable`, `repurposing`, `content-library`, `content-pillars`, `content-matrix`

### Formats
`talking-head`, `static-content`, `voiceover`, `green-screen`, `behind-the-scenes`, `commentary`, `podcast`

### Sales & Business
`roi-close`, `social-proof`, `testimonials`, `pricing-transparency`, `retainer-model`, `scope-creep`, `client-management`

### AI & Tools
`ai-workflow`, `claude`, `gemini`, `notebooklm`, `manychat`, `capcut`, `notion`, `geo-thesis`, `ai-search`

### Brand & Positioning
`personal-brand`, `personality`, `differentiation`, `audience-first`, `storybrand`

### Mindset
`patience`, `creative-block`, `no-rules`, `fatherhood`, `long-game`

---

## Writing Style for Descriptions

- Write in Sev's voice: assertive, direct, conversational
- No em-dashes
- No cliche AI phrases ("it's important to note", "game-changer", "dive into")
- Include the specific actionable detail, not a vague summary
- Someone should be able to read the description and DO the thing
- Use concrete numbers where available
- Keep it 2-4 sentences max

---

## Build Command

After updating the JSON files:

```bash
python build.py
```

This regenerates `docs/knowledge-hub.html` from the JSON data. The HTML is a self-contained file that opens in any browser and is served by GitHub Pages.
