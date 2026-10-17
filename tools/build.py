"""Rebuild Who Pay Creators deal lists from deals.json.
Usage: python3 build.py <deals.json> <site folder>
Updates: index.html (free list + counters), Pro page (full list), sitemap lastmod.
"""
import json, re, sys, html, datetime

data_path, site = sys.argv[1], sys.argv[2]
d = json.load(open(data_path))
progs, sponsors, upd, free_n = d["programs"], d["sponsors"], d["updated"], d["free_count"]
total = len(progs) + len(sponsors)
brands = len({x["brand"] for x in progs} | {x["brand"] for x in sponsors})
esc = html.escape
ANY = "Any (YouTube, IG, X, blogs, TikTok)"

# ---- free page ----
# Free picks: "free_brands" (in that order) if set, else the first free_count programs.
by_name = {p["brand"]: p for p in progs}
free_src = [by_name[b] for b in d.get("free_brands", []) if b in by_name][:free_n] or progs[:free_n]
free_n = len(free_src)
free = [{
    "brand": p["brand"], "niche": p["niche"], "platform": ANY, "deal_type": p["deal_type"],
    "pay": p["pay"], "creator_size": "Open to all sizes", "source": p["url"],
    "how_to_apply": p["url"], "date_seen": upd, "kind": "program"} for p in free_src]
idx_path = f"{site}/index.html"
s = open(idx_path).read()
new_script = ("<script>const DEALS=" + json.dumps(free, ensure_ascii=False) +
              f';const UPDATED="{upd}";const LOCKED={total - free_n};</script>')
s, n = re.subn(r"<script>const DEALS=.*?</script>", lambda m: new_script, s, flags=re.S)
assert n == 1, "free DEALS block not found"
for label, val in (("deals tracked", total), ("brands", brands), ("live sponsored posts", len(sponsors))):
    s, n = re.subn(r'<b class="cnt" data-n="\d+">\d+</b><span>' + re.escape(label),
                   f'<b class="cnt" data-n="{val}">{val}</b><span>{label}', s)
    assert n == 1, label
open(idx_path, "w").write(s)

# ---- Pro page ----
CHIP = '<span style="padding:3px 9px;border-radius:99px;background:#1b1b2b">{}</span>'
def card(name, badge_bg, badge_fg, badge, pay, chips, link, link_text, new=False):
    newb = ('<span style="font-size:11px;font-weight:800;padding:3px 8px;border-radius:99px;'
            'background:#3a2a00;color:#ffd166;margin-left:6px">NEW</span>') if new else ''
    return ('<div class="card"><div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap">'
            f'<b style="font-size:18px">{esc(name)}{newb}</b><span style="font-size:11px;font-weight:800;padding:3px 8px;'
            f'border-radius:99px;background:{badge_bg};color:{badge_fg}">{badge}</span></div>'
            f'<div style="color:#3dff9a;font-weight:700;margin:6px 0">{esc(pay)}</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:6px;font-size:12px">' + ''.join(CHIP.format(esc(c)) for c in chips) +
            f'</div><p style="margin-top:8px"><a class="back" href="{esc(link)}" target="_blank" rel="noopener">{link_text}</a></p></div>')

prog_html = ''.join(card(p["brand"], "#123524", "#3dff9a", "Verified program", p["pay"], [p["niche"], ANY],
                         p["url"], "Apply on official page →", p.get("new", False)) for p in progs)
sp_html = ''.join(card(x["brand"], "#3b0f1f", "#ff7aa8", "● SEEN SPONSORING", "Paid sponsor (amount not public)",
                       [x["niche"], "X (sponsored post)"], x["url"], "Visit brand to pitch them →") for x in sponsors)
section = (f'<h2 style="margin:16px 0 4px">💰 Open programs ({len(progs)})</h2><p style="color:#8d8da3;font-size:13px">'
           "Anyone can apply. Figures come from each brand's official page, re-checked " +
           datetime.date.fromisoformat(upd).strftime("%b %-d, %Y") + '.</p><div class="list">' + prog_html + '</div>\n'
           f'<h2 style="margin:20px 0 4px">📣 Brands paying creators for sponsored posts ({len(sponsors)})</h2>'
           '<p style="color:#8d8da3;font-size:13px">These brands paid for sponsored posts on X in October 2026. '
           "Pay wasn't made public, so pitch them directly through their website.</p>"
           '<div class="list">' + sp_html + '</div>\n')
pro_path = f"{site}/pro-kqagrxzgcaxl/index.html"
s = open(pro_path).read()
a = s.find('<h2 style="margin:16px 0 4px">'); b = s.find('<section class="card pro"><h2>Questions')
assert a > 0 and b > a
s = s[:a] + section + s[b:]
nice = datetime.date.fromisoformat(upd).strftime("%b %-d, %Y")
s, n = re.subn(r"✅ Last updated [^<]*", f"✅ Last updated {nice} · {total} deals", s)
assert n == 1
open(pro_path, "w").write(s)

# ---- sitemap: home page date ----
sm = f"{site}/sitemap.xml"
t = open(sm).read()
t = t.replace("<loc>https://whopaycreators.com/</loc><lastmod>", "<loc>https://whopaycreators.com/</loc><lastmod>X", 1)
t = re.sub(r"<lastmod>X\d{4}-\d\d-\d\d", f"<lastmod>{upd}", t)
open(sm, "w").write(t)
print(f"programs={len(progs)} sponsors={len(sponsors)} total={total} brands={brands} free={free_n} locked={total-free_n}")
