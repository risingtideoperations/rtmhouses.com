#!/usr/bin/env python3
"""Builds the static pages for rtmhouses.com into ./site. Header/footer are shared here so every page matches."""
import os, re
OUT = os.path.join(os.path.dirname(__file__), "site")
SITE = "https://rtmhouses.com"

ICON = {
 "pay": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
 "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
 "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
 "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.78 7.78 5.5 5.5 0 0 1 7.78-7.78zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
 "house": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/><path d="M10 20v-6h4v6"/></svg>',
 "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m9.5 15.5 1.8 1.8 3.7-3.8"/></svg>',
 "wrench2": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
 "phone2": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg>',
}

def head(title, desc, path, extra=""):
    full = f"{title} | Rising Tide Homes" if title != "Rising Tide Homes" else "Rising Tide Homes — Houses for rent in Birmingham, AL"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path=='index.html' else path}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{'' if path=='index.html' else path}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta name="theme-color" content="#0B2545">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://app.tenantturner.com"><link rel="preconnect" href="https://ttimages.blob.core.windows.net">
<link rel="stylesheet" href="css/site.css">
{extra}
</head>
<body>
<a class="sr" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Rising Tide Homes home"><img src="assets/logo-navy.png" srcset="assets/logo-navy@2x.png 2x" alt="Rising Tide" width="108" height="40"></a>
    <nav class="nav" aria-label="Main">
      <a href="homes.html">Available houses</a>
      <a href="apply.html">How to apply</a>
      <a href="residents.html">Residents</a>
      <a href="https://occupi.app/" rel="noopener" data-track="click_pay">Pay rent</a>
      <a href="contact.html">Contact</a>
      <a class="btn btn-outline btn-sm" href="https://leasepg.twa.rentmanager.com/" rel="noopener" data-track="click_portal">Resident portal</a>
      <a class="btn btn-primary btn-sm" href="homes.html">Find a house</a>
    </nav>
    <button class="menu-btn" aria-expanded="false" aria-controls="mnav">Menu <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
  <div class="mobile-nav" id="mnav" data-open="false">
    <a href="homes.html">Available houses</a>
    <a href="apply.html">How to apply</a>
    <a href="https://occupi.app/" rel="noopener" data-track="click_pay">Pay rent here</a>
    <a href="https://leasepg.twa.rentmanager.com/" rel="noopener" data-track="click_portal">Resident portal</a>
    <a href="residents.html">Residents: repairs, forms, FAQ</a>
    <a href="contact.html">Contact us</a>
    <a href="careers.html">Jobs &amp; vendors</a>
    <a class="btn btn-primary" href="homes.html">Find a house</a>
  </div>
</header>
<main id="main">
'''

def foot():
    return '''
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <img src="assets/logo-white.png" srcset="assets/logo-white@2x.png 2x" alt="Rising Tide" width="135" height="50" style="margin-bottom:.75rem">
        <p style="color:rgba(255,255,255,.75);max-width:34ch">Single-family rental homes in the Birmingham and Montgomery, Alabama areas. Locally owned and managed.</p>
        <p style="color:rgba(255,255,255,.75)">790 Montclair Rd, Ste 215<br>Birmingham, AL 35213<br>Mon–Fri 8:00 am – 5:00 pm</p>
      </div>
      <div><h4>Renters</h4><a href="homes.html">Available houses</a><a href="apply.html">How to apply</a><a href="apply.html#criteria">Qualification criteria</a><a href="https://app.tenantturner.com/listings/risingtidemanagement" rel="noopener">Book a showing</a></div>
      <div><h4>Residents</h4><a href="https://occupi.app/" rel="noopener" data-track="click_pay">Pay rent</a><a href="https://leasepg.twa.rentmanager.com/" rel="noopener" data-track="click_portal">Resident portal</a><a href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener" data-track="click_maintenance">Request a repair</a><a href="residents.html#forms">Forms</a><a href="residents.html#faq">FAQ</a></div>
      <div><h4>Company</h4><a href="contact.html">Contact</a><a href="careers.html">Jobs</a><a href="careers.html#vendors">Vendors</a><a href="tel:+12052089793" data-track="click_call">(205) 208-9793</a><a href="mailto:info@rtmhouses.com">info@rtmhouses.com</a></div>
    </div>
    <div class="legal">
      <img src="assets/eho.png" alt="Equal Housing Opportunity">
      <span>Equal Housing Opportunity. &copy; <span id="yr"></span> Rising Tide Management, LLC. All rights reserved.</span>
    </div>
  </div>
</footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear()</script>
<script src="js/site.js" defer></script>
</body>
</html>
'''

pages = {}

# ---------------- index ----------------
pages["index.html"] = head("Rising Tide Homes", "Houses for rent in Birmingham, AL. See every available house, book a self-guided showing in minutes, and apply online. Locally owned and managed.", "index.html") + f'''
<section class="hero">
  <div class="wrap">
    <div>
      <div class="count" data-count><span class="dot" aria-hidden="true"></span><b>…</b> <span class="lbl">houses available now</span></div>
      <h1>Houses for rent, ready when you are.</h1>
      <p class="sub">Single-family homes across greater Birmingham. See one today — no appointment, no office visit — and apply from your phone.</p>
      <form class="searchbar" action="homes.html" method="get" role="search">
        <label class="sr" for="s-q">Search by street, city or zip</label>
        <input id="s-q" name="q" type="search" placeholder="City, zip code or street" autocomplete="off">
        <button type="submit"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>Search</button>
      </form>
      <div class="hero-chips" id="chips"><a href="homes.html">All houses</a><a href="homes.html?beds=3">3+ bedrooms</a><a href="homes.html?max=1100">Under $1,100</a></div>
    </div>
    <div class="mosaic" aria-hidden="true"><a href="homes.html" tabindex="-1"><img src="assets/hero-1.jpg" alt="" width="1000" height="667"></a><a href="homes.html" tabindex="-1"><img src="assets/hero-2.jpg" alt="" loading="lazy"></a><a href="homes.html" tabindex="-1"><img src="assets/hero-3.jpg" alt="" loading="lazy"></a><a href="homes.html" tabindex="-1"><img src="assets/hero-4.jpg" alt="" loading="lazy"></a><a href="homes.html" tabindex="-1"><img src="assets/hero-5.jpg" alt="" loading="lazy"></a></div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-grid">
      <div>
        <h2>Renting from us, in plain terms.</h2>
        <p>Every house on this site is managed by our Birmingham office. No outside agent in the middle and no office visit required — you deal with the people who actually schedule the repairs.</p>
      </div>
      <ul class="plain">
        <li><b>See it today.</b> Self-guided showings seven days a week, including evenings — exact times are shown when you schedule. You get the lockbox code by text.</li>
        <li><b>Know before you apply.</b> Every house page shows the income you need and what's due at move-in. No surprises after the $50 fee.</li>
        <li><b>Repairs by our own crew.</b> In-house technicians, requests tracked online, a 24/7 line for emergencies.</li>
        <li><b>A Birmingham office that picks up.</b> Call or text a person Monday through Friday. Our address is on every page.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head left"><div><h2>Newest houses</h2><p>Listed automatically the day they're ready.</p></div><a class="btn btn-outline" href="homes.html">See all available houses</a></div>
    <div class="grid" id="featured" aria-live="polite"></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="path">
      <div>
        <h2>Showing to keys in days, not weeks.</h2>
        <p class="lede" style="margin-bottom:.5rem">Most applicants have an answer within 3 to 5 business days.</p>
        <div class="steps">
          <div class="step"><div><h3>Walk through on your own</h3><p>Pick a house and a time. You'll get a lockbox code by text and walk through on your own — evenings and weekends included.</p></div></div>
          <div class="step"><div><h3>Apply from your phone</h3><p>$50 per adult. Have your ID and two recent pay stubs ready. Applications are typically reviewed within 3 to 5 business days.</p></div></div>
          <div class="step"><div><h3>E-sign, pay the deposit, get keys</h3><p>Sign the lease electronically, pay your deposit, pick up keys. Turn on autopay and rent takes care of itself.</p></div></div>
        </div>
        <a class="btn btn-primary" href="apply.html">See what you need to qualify</a>
      </div>
      <div class="pic"><img src="assets/porch-1141-15th-pl.jpg" alt="Front porch of a Rising Tide house on 15th Place SW, Birmingham" width="800" height="450" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="wrap">
    <div class="section-head left"><div><h2>Current residents</h2><p>The four things people call about, handled online.</p></div></div>
    <div class="tiles">
      <a class="tile" href="https://occupi.app/" rel="noopener" data-track="click_pay"><div class="ic">{ICON["pay"]}</div><h3>Pay rent here</h3><p>Pay on Occupi by bank account or card, or set up autopay once and never pay a late fee.</p></a>
      <a class="tile" href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener" data-track="click_maintenance"><div class="ic">{ICON["wrench"]}</div><h3>Request a repair</h3><p>Send photos, track the work order until it's done.</p></a>
      <a class="tile" href="residents.html#forms"><div class="ic">{ICON["doc"]}</div><h3>Forms</h3><p>Move-in inspection, notice to vacate, payment arrangement, move-out.</p></a>
      <a class="tile" href="residents.html#faq"><div class="ic">{ICON["chat"]}</div><h3>Questions</h3><p>Rent dates, late fees, pets, lockouts, emergencies — answered.</p></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head left"><div><h2>In their words</h2></div></div>
    <div class="quotes">
      <div class="quote"><p>“Great landlords, friendly and responsive!”</p><cite>Katy Pena, resident</cite></div>
      <div class="quote"><p>“I have rented from Rising Tide for 3 years and I feel like I have a great relationship with my landlord.”</p><cite>Janae Wilson, resident</cite></div>
      <div class="quote"><p>“I do projects for Rising Tide and I know that they're reasonable and take care of their homes and tenants.”</p><cite>Michael Hacklow, vendor</cite></div>
    </div>
  </div>
</section>
<script>
document.addEventListener('DOMContentLoaded', async () => {{
  RT.renderGrid(document.getElementById('featured'), {{ limit: 6 }});
  try {{
    const all = await RT.listings();
    const cities = [...new Set(all.map(l => l.city).filter(Boolean))].sort();
    const chips = document.getElementById('chips');
    cities.slice(0, 3).forEach(c => {{ const a = document.createElement('a'); a.href = 'homes.html?city=' + encodeURIComponent(c); a.textContent = c; chips.appendChild(a); }});
  }} catch (e) {{}}
  document.querySelector('.searchbar').addEventListener('submit', () => RT.track('search'));
}});
</script>
''' + foot()

# ---------------- homes ----------------
pages["homes.html"] = head("Available houses for rent", "Every Rising Tide house available right now in Birmingham, Center Point, Trussville, Pelham, Gardendale and more. Filter by city, bedrooms and rent; book a showing in minutes.", "homes.html", '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>') + '''
<div class="page-head"><div class="wrap"><h1>Available houses</h1><p>Live list — updated automatically as houses are listed and leased. Tap any house to see details and book a showing.</p></div></div>
<div class="filters">
  <div class="wrap">
    <label class="sr" for="f-city">City</label><select id="f-city"><option value="">All cities</option></select>
    <label class="sr" for="f-beds">Bedrooms</label><select id="f-beds"><option value="">Any beds</option><option value="2">2+ beds</option><option value="3">3+ beds</option><option value="4">4+ beds</option></select>
    <label class="sr" for="f-max">Max rent</label><select id="f-max"><option value="">Any rent</option><option value="900">Up to $900</option><option value="1100">Up to $1,100</option><option value="1300">Up to $1,300</option><option value="1500">Up to $1,500</option><option value="2000">Up to $2,000</option></select>
    <label class="sr" for="f-sort">Sort</label><select id="f-sort"><option value="new">Newest first</option><option value="rent-asc">Rent: low to high</option><option value="rent-desc">Rent: high to low</option><option value="beds">Most bedrooms</option></select>
    <button class="clear" id="f-clear" type="button" hidden>Clear</button>
    <span class="result" id="f-result"></span>
  </div>
</div>
<section class="section-tight">
  <div class="wrap">
    <div class="map-wrap">
      <div id="map" class="map" aria-label="Map of available houses"></div>
      <div class="legend"><span><i class="pin now"></i>Available now</span><span><i class="pin soon"></i>Coming soon</span><button class="clear" id="map-toggle" type="button" aria-expanded="true">Hide map</button></div>
    </div>
    <div class="grid" id="grid" aria-live="polite"></div>
    <p class="small muted" style="margin-top:1.5rem">Rent shown is the monthly rent. A $50 application fee applies per adult applicant. Your security deposit amount is set when your application is approved. Pets vary by house — see each listing. We do not currently have homes that accept Section 8 / Housing Choice Vouchers. <a href="apply.html">Full criteria</a>.</p>
  </div>
</section>
<script>
document.addEventListener('DOMContentLoaded', async () => {
  const q = new URLSearchParams(location.search);
  const sel = { city: document.getElementById('f-city'), beds: document.getElementById('f-beds'), max: document.getElementById('f-max'), sort: document.getElementById('f-sort') };
  const grid = document.getElementById('grid'), res = document.getElementById('f-result'), clear = document.getElementById('f-clear');
  let all = []; try { all = await RT.listings(); } catch (e) {}
  [...new Set(all.map(l => l.city).filter(Boolean))].sort().forEach(c => { const o = document.createElement('option'); o.value = c; o.textContent = c; sel.city.appendChild(o); });
  // Map (Leaflet + OpenStreetMap). Green = available now, amber = coming soon.
  let map = null, layer = null;
  const soon = l => !!(l.available && !/now/i.test(l.available));
  function drawMap(items) {
    if (!window.L || !document.getElementById('map')) return;
    if (!map) {
      map = L.map('map', { scrollWheelZoom: false }).setView([33.52, -86.8], 10);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>', maxZoom: 18 }).addTo(map);
      layer = L.layerGroup().addTo(map);
    }
    layer.clearLayers();
    const pts = [];
    items.forEach(l => {
      if (typeof l.lat !== 'number' || typeof l.lng !== 'number') return;
      const color = soon(l) ? '#D9822B' : '#1E9E63';
      const m = L.circleMarker([l.lat, l.lng], { radius: 9, color: '#fff', weight: 2, fillColor: color, fillOpacity: 1 });
      m.bindPopup('<div class="pop">' + (l.photo ? '<img src="' + RT.esc(l.photo) + '" alt="">' : '') + '<b>' + RT.money(l.rent) + '/mo</b> · ' + (l.beds != null ? l.beds + ' bd' : '') + (l.baths != null ? ' / ' + l.baths + ' ba' : '') + '<br>' + RT.esc(l.address) + ', ' + RT.esc(l.city) + '<br><span class="' + (soon(l) ? 'soon' : 'now') + '">' + (soon(l) ? 'Coming ' + RT.esc(l.available) : 'Available now') + '</span><br><a href="' + RT.detailUrl(l) + '">Details</a> · <a href="' + RT.esc(l.schedule) + '" target="_blank" rel="noopener" data-track="click_schedule" data-listing="' + RT.esc(l.id) + '" data-addr="' + RT.esc(l.address) + '">Book a showing</a></div>', { maxWidth: 260 });
      m.addTo(layer); pts.push([l.lat, l.lng]);
    });
    if (pts.length) map.fitBounds(pts, { padding: [30, 30], maxZoom: 13 });
  }
  const tog = document.getElementById('map-toggle');
  tog.addEventListener('click', () => { const w = document.querySelector('.map-wrap'); const open = !w.classList.contains('collapsed'); w.classList.toggle('collapsed', open); tog.textContent = open ? 'Show map' : 'Hide map'; tog.setAttribute('aria-expanded', String(!open)); if (!open && map) setTimeout(() => map.invalidateSize(), 50); });
  ['city','beds','max'].forEach(k => { if (q.get(k)) sel[k].value = q.get(k); });
  const qtext = q.get('q') || '';
  function sortList(items) {
    const v = sel.sort.value;
    if (v === 'rent-asc') items.sort((a,b)=>(a.rent||9e9)-(b.rent||9e9));
    else if (v === 'rent-desc') items.sort((a,b)=>(b.rent||0)-(a.rent||0));
    else if (v === 'beds') items.sort((a,b)=>(b.beds||0)-(a.beds||0));
    return items;
  }
  async function run() {
    const f = { city: sel.city.value, beds: sel.beds.value, max: sel.max.value, q: qtext };
    const active = !!(f.city || f.beds || f.max || f.q);
    clear.hidden = !active;
    const umap = await RT.unitMap();
    let items = sortList(RT.filter(all, f));
    if (!all.length) { grid.innerHTML = '<div class="empty" style="grid-column:1/-1"><p><strong>The listing feed didn\\'t load.</strong></p><p>Refresh the page, or see the live list at <a href="https://app.tenantturner.com/listings/risingtidemanagement" rel="noopener">our showing page</a>.</p></div>'; res.textContent=''; return; }
    if (!items.length) grid.innerHTML = '<div class="empty" style="grid-column:1/-1"><p><strong>No houses match that search.</strong></p><p>Try fewer filters. New houses are listed most weeks.</p></div>';
    else grid.innerHTML = items.map(l => RT.card(l, umap)).join('');
    drawMap(items);
    res.textContent = items.length + ' of ' + all.length + (qtext ? ' · “' + qtext + '”' : '');
    const p = new URLSearchParams(); ['city','beds','max'].forEach(k => { if (f[k]) p.set(k, f[k]); }); if (qtext) p.set('q', qtext);
    history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
  }
  Object.values(sel).forEach(s => s.addEventListener('change', () => { RT.track('search'); run(); }));
  clear.addEventListener('click', () => { sel.city.value=''; sel.beds.value=''; sel.max.value=''; history.replaceState(null,'',location.pathname); location.reload(); });
  run();
});
</script>
''' + foot()

# ---------------- home detail ----------------
pages["home.html"] = head("House details", "House for rent from Rising Tide Homes — photos, rent, bedrooms, bathrooms, and a link to book a self-guided showing.", "home.html") + '''
<div class="page-head"><div class="wrap"><div class="breadcrumb"><a href="homes.html">Available houses</a> / <span id="bc">House</span></div><h1 id="h-addr">Loading…</h1><p id="h-city"></p></div></div>
<section class="section-tight">
  <div class="wrap">
    <div class="detail">
      <div class="d-photo">
        <div class="gallery" id="gal">
          <div class="photo main"><img id="g-main" alt=""><button class="gnav prev" id="g-prev" type="button" aria-label="Previous photo">&#8249;</button><button class="gnav next" id="g-next" type="button" aria-label="Next photo">&#8250;</button><span class="gcount" id="g-count"></span></div>
          <div class="thumbs" id="g-thumbs"></div>
        </div>
      </div>
      <aside class="d-side">
        <div class="panel sticky">
          <div class="rent" id="h-rent"></div>
          <div class="facts" id="h-facts"></div>
          <div class="actions">
            <a class="btn btn-primary btn-block" id="h-sched" href="#" target="_blank" rel="noopener" data-track="click_schedule">Book a self-guided showing</a>
            <a class="btn btn-primary btn-block" id="h-apply" href="#" target="_blank" rel="noopener" data-track="click_apply">Apply for this house</a>
            <a class="btn btn-outline btn-block" href="tel:+12052089793" data-track="click_call">Call (205) 208-9793</a>
          </div>
          <p class="fine">Showings are self-guided: pick a time, verify your phone, and you'll get a lockbox code.</p>
        </div>
        <div class="panel" style="margin-top:1rem;box-shadow:none">
          <h3 style="font-size:1.2rem;margin-bottom:.75rem">What it takes to rent this house</h3>
          <dl class="kv" id="h-qual"></dl>
          <p class="fine">Your security deposit amount is set when your application is approved. <a href="apply.html#criteria">Full criteria</a>.</p>
        </div>
      </aside>
      <div class="d-text">
        <h2>About this house</h2>
        <p class="desc" id="h-desc"></p>
        <h3 style="margin-top:1.5rem">Details</h3>
        <dl class="kv" id="h-kv"></dl>
        <p style="margin-top:1.5rem"><a id="h-map" class="btn btn-outline" href="#" target="_blank" rel="noopener">Open in Google Maps</a></p>
      </div>
    </div>
  </div>
</section>
<div class="mobile-cta" id="mcta" hidden>
  <a class="btn btn-primary" id="m-sched" href="#" target="_blank" rel="noopener" data-track="click_schedule">Book a showing</a>
  <a class="btn btn-primary" id="m-apply" href="#" target="_blank" rel="noopener" data-track="click_apply">Apply</a>
</div>
<section class="section section-sand" style="margin-top:2rem">
  <div class="wrap"><div class="section-head left"><div><h2>More houses nearby</h2></div><a class="btn btn-outline" href="homes.html">See all</a></div><div class="grid" id="more"></div></div>
</section>
<script>
document.addEventListener('DOMContentLoaded', async () => {
  const id = new URLSearchParams(location.search).get('id');
  const $ = s => document.querySelector(s), $$ = s => Array.from(document.querySelectorAll(s));
  let list = [], map = {};
  try { [list, map] = await Promise.all([RT.listings(), RT.unitMap()]); } catch (e) {}
  const l = list.find(x => x.id === String(id));
  if (!l) {
    $('#h-addr').textContent = 'This house is no longer available';
    $('#h-city').innerHTML = 'It was probably just leased. <a href="homes.html">See every house available right now</a>.';
    $('.detail').hidden = true; RT.renderGrid($('#more'), { limit: 6 }); return;
  }
  document.title = l.address + ', ' + l.city + ' — ' + RT.money(l.rent) + '/mo | Rising Tide Homes';
  $('#bc').textContent = l.address; $('#h-addr').textContent = l.address; $('#h-city').textContent = l.city + ', ' + l.state + ' ' + l.zip;
  // Gallery: every Rent Manager photo for this unit (from site_listing_photos), falling back to the Tenant Turner photo
  let photos = [];
  try {
    const unitId = (RT.applyUrl(l, map).match(/unitId=(\d+)/) || [])[1];
    if (unitId) {
      const r = await fetch(RT.SB_URL + '/rest/v1/site_listing_photos?select=url,caption,kind,sort_order,width,height&unit_id=eq.' + unitId + '&order=kind.desc,sort_order.asc,id.asc', { headers: { apikey: RT.SB_KEY, Authorization: 'Bearer ' + RT.SB_KEY } });
      if (r.ok) photos = await r.json();
    }
  } catch (e) {}
  // prefer enhanced over original when both exist for the same shot; staged go last
  const enhanced = photos.filter(p => p.kind === 'enhanced'), originals = photos.filter(p => p.kind === 'original'), staged = photos.filter(p => p.kind === 'staged');
  photos = (enhanced.length ? enhanced : originals).concat(staged);
  if (!photos.length && l.photo) photos = [{ url: l.photo, caption: null, kind: 'original' }];
  let gi = 0;
  const gMain = $('#g-main'), gThumbs = $('#g-thumbs'), gCount = $('#g-count');
  function show(i) {
    if (!photos.length) return; gi = (i + photos.length) % photos.length; const ph = photos[gi];
    gMain.src = ph.url; gMain.alt = (ph.caption ? ph.caption + ' — ' : '') + l.address + (ph.kind === 'staged' ? ' (virtually staged)' : '');
    gCount.textContent = (gi + 1) + ' / ' + photos.length + (ph.kind === 'staged' ? ' · Virtually staged' : '');
    $$('#g-thumbs button').forEach((b, k) => b.setAttribute('aria-current', k === gi ? 'true' : 'false'));
    const cur = gThumbs.children[gi]; if (cur) gThumbs.scrollTo({ left: cur.offsetLeft - gThumbs.clientWidth / 2 + cur.offsetWidth / 2, behavior: 'smooth' });
  }
  gThumbs.innerHTML = photos.map((ph, k) => '<button type="button" aria-label="Photo ' + (k + 1) + '"><img src="' + RT.esc(ph.url) + '" alt="" loading="lazy"></button>').join('');
  $$('#g-thumbs button').forEach((b, k) => b.addEventListener('click', () => show(k)));
  $('#g-prev').addEventListener('click', () => show(gi - 1)); $('#g-next').addEventListener('click', () => show(gi + 1));
  document.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') show(gi - 1); if (e.key === 'ArrowRight') show(gi + 1); });
  let tx = null; gMain.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true }); gMain.addEventListener('touchend', e => { if (tx == null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 40) show(gi + (dx < 0 ? 1 : -1)); tx = null; }, { passive: true });
  if (photos.length < 2) { $('#g-prev').hidden = true; $('#g-next').hidden = true; gThumbs.hidden = true; }
  show(0);
  $('#h-desc').textContent = l.description || '';
  $('#h-rent').innerHTML = RT.money(l.rent) + ' <span>/ month</span>';
  const b = l.baths == null ? '' : (l.baths % 1 === 0 ? l.baths.toFixed(0) : l.baths.toFixed(1));
  $('#h-facts').innerHTML = (l.beds != null ? '<div><b>' + l.beds + '</b>beds</div>' : '') + (b ? '<div><b>' + b + '</b>baths</div>' : '') + '<div><b>' + RT.esc(l.available || 'Now') + '</b>available</div>';
  const kv = [['Type', l.type], ['Rent', RT.money(l.rent) + ' / month'], ['Fees', l.fees], ['Pets', l.pets], ['Special offer', l.offer], ['Listed', l.activated]].filter(x => x[1]);
  $('#h-kv').innerHTML = kv.map(x => '<dt>' + RT.esc(x[0]) + '</dt><dd>' + RT.esc(x[1]) + '</dd>').join('');
  const apply = RT.applyUrl(l, map);
  ['#h-sched', '#m-sched'].forEach(s => { const a = $(s); a.href = l.schedule; a.dataset.listing = l.id; a.dataset.addr = l.address; });
  ['#h-apply', '#m-apply'].forEach(s => { const a = $(s); a.href = apply; a.dataset.listing = l.id; a.dataset.addr = l.address; });
  $('#h-map').href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(l.address + ', ' + l.city + ', ' + l.state + ' ' + l.zip);
  if (l.rent) {
    const q = [['Take-home income', 'at least ' + RT.money(l.rent * 3) + ' / month (3× rent)'], ['Application fee', '$50 per adult, non-refundable'], ['Security deposit', 'set when your application is approved'], ['Due at move-in', 'first month + security deposit'], ['Credit', 'FICO under 600 is reviewed case by case'], ['Pets', 'with approval: $250 fee + $25/mo per pet']];
    $('#h-qual').innerHTML = q.map(x => '<dt>' + RT.esc(x[0]) + '</dt><dd>' + RT.esc(x[1]) + '</dd>').join('');
  }
  $('#mcta').hidden = false; document.body.classList.add('has-mobile-cta');
  // nearby: same city first, then others
  const others = list.filter(x => x.id !== l.id).sort((a, b) => (b.city === l.city) - (a.city === l.city)).slice(0, 3);
  $('#more').innerHTML = others.map(x => RT.card(x, map)).join('') || '<div class="empty" style="grid-column:1/-1">No other houses right now.</div>';
});
</script>
''' + foot()

# ---------------- apply / criteria ----------------
pages["apply.html"] = head("How to apply", "How to rent a Rising Tide house: what you need, the $50 application fee, income and credit requirements, pets, deposits, and what disqualifies an application.", "apply.html") + '''
<div class="page-head"><div class="wrap"><h1>How to apply</h1><p>Read this before you apply. It tells you exactly what we check, so you don't pay a fee for an application that can't be approved.</p></div></div>
<section class="section-tight">
  <div class="wrap">
    <div class="quick">
      <div><b>$50</b><span>application fee, per adult 19+. Non-refundable.</span></div>
      <div><b>3×</b><span>take-home monthly income vs. rent (or equivalent assets)</span></div>
      <div><b>600</b><span>FICO. Applicants with a score under 600 are reviewed on a case-by-case basis.</span></div>
      <div><b>Deposit</b><span>Your security deposit amount is set when your application is approved.</span></div>
    </div>
    <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:2rem">
      <a class="btn btn-primary" href="homes.html">Pick a house to apply for</a>
      <a class="btn btn-outline" href="https://leasepg.twa.rentmanager.com/applynow" target="_blank" rel="noopener" data-track="click_apply">Open the application</a>
    </div>

    <div class="prose">
      <h2>What to have ready</h2>
      <ul>
        <li>A government-issued photo ID for every applicant (driver's license, state ID, or passport). Non-U.S. citizens: proof of immigration status.</li>
        <li>Social Security number or ITIN.</li>
        <li>Proof of income: your two most recent pay stubs, or a new-hire letter on company letterhead, last year's tax return, or the last three months of bank statements. Self-employed: last year's tax return or a bank verification plus your DBA registration.</li>
        <li>Rental history with landlord contact info, or mortgage history if you've owned.</li>
        <li>A checking or savings account. Every applicant must have one.</li>
      </ul>

      <h2 id="criteria">Qualification criteria</h2>
      <p>"Applicant" means anyone who will sign the lease. "Occupant" means anyone else who will live in the home. Each adult applicant pays the $50 application fee; applications aren't processed until every fee is paid and a copy of each applicant's ID is on file. Fees are used to cover screening costs and are not refunded. A house stays available until we accept a security deposit and both sides sign a lease.</p>

      <h3>Who can apply</h3>
      <ul>
        <li>The primary applicant must be 19 or older.</li>
        <li>Maximum occupancy is two people per bedroom plus one per home.</li>
      </ul>

      <h3>Income</h3>
      <p>Net (take-home) monthly income must be at least three times the monthly rent, or you must hold liquid assets equal to at least three times the total value of the lease. We verify it with the documents above. Cash income doesn't count. Housing allowances, government-backed disability, Social Security, and retirement income count. Child support and alimony count if the order is current and you can show six months of consistent payments. If your credit is thin or you have no rental history, time on the job helps.</p>

      <h3>Credit</h3>
      <p>We pull a credit report, landlord-tenant court records, and a criminal background check on every adult applicant. Applicants with a FICO score under 600 are reviewed on a case-by-case basis. Chapter 13 bankruptcy is acceptable if you have been in repayment for 12 months and the payment shows on your pay stubs.</p>

      <h3>Rental history</h3>
      <p>An eviction in the past year is a denial. A rental-related judgment with a balance over $3,400 is a denial. Homeowners: we look for no more than three late mortgage payments per year. No rental history at all isn't held against you.</p>

      <h3>Co-signers</h3>
      <p>A co-signer or guarantor can cover a shortfall in income, credit, or rental history, but not a criminal record. Co-signers file their own application, pay the fee, and must show monthly income of at least five times the rent. Accepted at our discretion.</p>

      <h3>Criminal history</h3>
      <p>Every applicant and every occupant 18 or older is screened. We may decline any application based on criminal history. These are automatic denials: a felony (or equivalent) involving property damage, violence, or a sexual offense; any offense requiring sex-offender registration; a felony for manufacturing or distributing controlled substances within the past seven years.</p>

      <h3>Security deposit</h3>
      <p>Due when the lease is signed. Your security deposit amount is set when your application is approved. It's refundable at move-out less damage and any unpaid balance, and can't be applied to rent.</p>

      <h3 id="pets">Pets</h3>
      <p>Pets need written approval before they move in (and before you get one later). Up to four pets per home. Each approved pet carries a non-refundable $250 pet fee and $25 a month in pet rent. An unapproved pet found in the home is a $250 fee, and pet rent is added through the end of the lease. Verified assistance animals are always allowed with no fee. We may decline any animal we consider unsuitable for the home, and no chained animals. Weight and breed limits are in the lease pet addendum; these breeds and their mixes may be declined: Akita, American Bulldog, Pit Bull / American Pit Bull Terrier, Bull Mastiff, Chow, Doberman, German Shepherd, Great Dane, Husky, Rottweiler, wolf hybrids, and similar.</p>

      <h3>Housing vouchers</h3>
      <p>We do not currently have homes that accept Section 8 / Housing Choice Vouchers.</p>

      <h3>Honesty</h3>
      <p>Anything false on an application is an automatic denial, forfeits any fees and deposits paid, and you can't reapply.</p>

      <div class="callout warn"><strong>We no longer accept Rhino deposit insurance.</strong> If you have an existing Rhino policy from a prior Rising Tide lease, see the <a href="residents.html#faq">resident FAQ</a>.</div>
    </div>
  </div>
</section>
''' + foot()

# ---------------- residents ----------------
pages["residents.html"] = head("Residents", "Rising Tide residents: pay rent and set up autopay in the resident portal, submit a maintenance request, download forms, and get answers to common questions.", "residents.html") + f'''
<div class="page-head"><div class="wrap"><h1>Residents</h1><p>Pay rent, request a repair, send a form, or find an answer — without calling the office.</p></div></div>
<section class="section-tight">
  <div class="wrap">
    <div class="tiles">
      <a class="tile" href="https://occupi.app/" rel="noopener" data-track="click_pay"><div class="ic">{ICON["pay"]}</div><h3>Pay rent here</h3><p>Pay on Occupi by bank account or card. Turn on autopay so you never pay a late fee.</p></a>
      <a class="tile" href="https://leasepg.twa.rentmanager.com/" rel="noopener" data-track="click_portal"><div class="ic">{ICON["key"]}</div><h3>Resident portal</h3><p>Your lease, ledger and documents in the Rent Manager tenant portal.</p></a>
      <a class="tile" href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener" data-track="click_maintenance"><div class="ic">{ICON["wrench"]}</div><h3>Request a repair</h3><p>Describe the problem, add photos, and track the work order. Non-emergency visits are scheduled within 2–3 business days.</p></a>
      <a class="tile" href="tel:+12054193148" data-track="click_call"><div class="ic">{ICON["phone"]}</div><h3>After-hours emergency</h3><p>No heat, no water, flooding, gas smell, or you're locked out: call 205-419-3148 any time.</p></a>
      <a class="tile" href="sms:+12055021552" data-track="click_text"><div class="ic">{ICON["chat"]}</div><h3>Text the office</h3><p>Quick questions, Mon–Fri 8–5: text 205-502-1552 or 205-962-7771, or email rtm@rtmhouses.com.</p></a>
    </div>
  </div>
</section>

<section class="section" id="forms">
  <div class="wrap">
    <div class="section-head left"><div><h2>Forms</h2><p>Each one takes a couple of minutes on your phone.</p></div></div>
    <div class="tiles">
      <a class="tile" href="https://forms.zohopublic.com/risingtidemanagement1/form/TenantMoveinInspection/formperma/VfWzRyuTWtx16A4LAmLuuXj6qz51ujF1UZHJr__UoI0" rel="noopener"><div class="ic">{ICON["key"]}</div><h3>Move-in inspection</h3><p>Note the condition of the house in your first days so you're not charged for it later.</p></a>
      <a class="tile" href="https://forms.zohopublic.com/risingtidemanagement1/form/RentPaymentArrangement/formperma/Jw0SogobEHr3btvV2RyFOkNXlsybFZEsFYZEQiVx5W4" rel="noopener"><div class="ic">{ICON["doc"]}</div><h3>Payment arrangement</h3><p>Going to be late? Tell us the date you'll pay before rent is due, not after.</p></a>
      <a class="tile" href="https://forms.zohopublic.com/risingtidemanagement1/form/NoticetoVacate/formperma/9OGfj5Au0p0801kc9J-EpsSRTkSEjTpL5FdxwwbXY4k" rel="noopener"><div class="ic">{ICON["doc"]}</div><h3>Notice to vacate</h3><p>Moving out? Give written notice here — check your lease for how many days are required.</p></a>
      <a class="tile" href="https://forms.zohopublic.com/risingtidemanagement1/form/MoveOutConfirmation/formperma/dcaAHsJx06ttOk2wsmWmN-tPwSF71u7xsZg0TZ7OdLc" rel="noopener"><div class="ic">{ICON["doc"]}</div><h3>Move-out confirmation</h3><p>Confirm your move-out date and forwarding address for your deposit.</p></a>
    </div>
  </div>
</section>

<section class="section section-sand" id="faq">
  <div class="wrap">
    <div class="section-head left"><div><h2>Questions residents ask</h2></div></div>
    <div style="max-width:72ch">
      <details><summary>Where do I pay rent?</summary><p>At <a href="https://occupi.app/" rel="noopener" data-track="click_pay">occupi.app</a> — bank account or card. Payments post to your account automatically. The Rent Manager resident portal is for your lease, ledger and documents, not payments.</p></details>
      <details><summary>When is rent due, and when is it late?</summary><p>Rent is due on the 1st. Check your lease for the exact grace period and late fee. The surest way to never pay a late fee is autopay on Occupi.</p></details>
      <details><summary>How do I set up autopay?</summary><p>Log in at <a href="https://occupi.app/" rel="noopener" data-track="click_pay">occupi.app</a>, open Payments, and turn on autopay. Pick a bank account (lowest fees) or a card and the date you want it to run. You can change or cancel it any time.</p></details>
      <details><summary>Something broke. What do I do?</summary><p>Submit a request at <a href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener">our maintenance portal</a> with photos. Non-emergency visits are scheduled within 2–3 business days. True emergencies — no heat, no water, flooding, gas smell, lockout — call 205-419-3148 any time.</p></details>
      <details><summary>Will I be charged for a repair?</summary><p>Normal wear is on us. You're billed for the repair plus any trip charge when the damage was caused by you, your household, or guests; for clogged disposals and toilets (other than human waste); misused appliances; dirty air filters; items your lease assigns to you; smoke-detector batteries, tripped breakers, and light bulbs; or if you refuse or block access to the home, including unrestrained pets.</p></details>
      <details><summary>Can I get a pet?</summary><p>Ask first, in writing. Each approved pet is a non-refundable $250 fee plus $25 a month pet rent; up to four pets. An unapproved pet is a $250 fee plus pet rent through the end of the lease. Assistance animals are always allowed with no fee. Details under <a href="apply.html#pets">pets</a>.</p></details>
      <details><summary>I'm locked out.</summary><p>During office hours call (205) 208-9793. After hours call 205-419-3148. A lockout service charge may apply.</p></details>
      <details><summary>How do I give notice that I'm moving?</summary><p>Use the <a href="https://forms.zohopublic.com/risingtidemanagement1/form/NoticetoVacate/formperma/9OGfj5Au0p0801kc9J-EpsSRTkSEjTpL5FdxwwbXY4k" rel="noopener">notice to vacate form</a>. Your lease says how many days' notice are required. Leave the house clean and empty, return all keys, and send the <a href="https://forms.zohopublic.com/risingtidemanagement1/form/MoveOutConfirmation/formperma/dcaAHsJx06ttOk2wsmWmN-tPwSF71u7xsZg0TZ7OdLc" rel="noopener">move-out confirmation</a> with a forwarding address for your deposit.</p></details>
      <details><summary>I have a Rhino policy from an older lease. What happens to it?</summary><p>We no longer take new Rhino policies. If you still have one, it renews automatically each lease year unless you replace it by paying the full security deposit — we have to hold one or the other. Rhino premiums aren't refundable like a deposit. If we file a Rhino claim for unpaid rent or damage, the payment goes to your account here and you settle with Rhino directly. Questions about your policy: support@sayrhino.com.</p></details>
      <details><summary>Do I need renter's insurance?</summary><p>Yes — it covers your belongings and living expenses if something happens to the house. Rising Tide's insurance does not cover your things.</p></details>
      <details><summary>Pest control</summary><p>Ask the office about our pest control program (PestShare). It covers routine treatment for enrolled homes.</p></details>
    </div>
  </div>
</section>
''' + foot()

# ---------------- contact ----------------
pages["contact.html"] = head("Contact us", "Call, text, or message Rising Tide Homes in Birmingham, AL. Office hours Mon–Fri 8–5. After-hours emergency line for residents.", "contact.html") + '''
<div class="page-head"><div class="wrap"><h1>Contact us</h1><p>Residents: repairs go through the maintenance portal so they get scheduled — not through this form. Everything else, we're here.</p></div></div>
<section class="section-tight">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <div class="contact-list">
          <div><a href="tel:+12052089793" data-track="click_call">(205) 208-9793</a><small>Office, Mon–Fri 8:00 am – 5:00 pm</small></div>
          <div><a href="sms:+12055021552" data-track="click_text">Text 205-502-1552</a><small>Residents: quick questions during office hours (or 205-962-7771)</small></div>
          <div><a href="tel:+12054193148" data-track="click_call">205-419-3148</a><small>After-hours emergencies only</small></div>
          <div><a href="mailto:info@rtmhouses.com">info@rtmhouses.com</a><small>Leasing and general questions</small></div>
          <div><a href="mailto:rtm@rtmhouses.com">rtm@rtmhouses.com</a><small>Current residents</small></div>
          <div><a href="https://www.google.com/maps/search/?api=1&query=790+Montclair+Rd+Ste+215+Birmingham+AL+35213" target="_blank" rel="noopener">790 Montclair Rd, Ste 215, Birmingham, AL 35213</a><small>Office</small></div>
        </div>
        <div class="callout" style="margin-top:1.5rem"><strong>Need a repair?</strong> Use the <a href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener" data-track="click_maintenance">maintenance portal</a>. Requests sent by email or this form can't be scheduled.</div>
      </div>
      <div>
        <form class="form" id="cf" novalidate>
          <div><label for="c-name">Your name</label><input id="c-name" name="name" required maxlength="120" autocomplete="name"></div>
          <div><label for="c-email">Email</label><input id="c-email" name="email" type="email" maxlength="200" autocomplete="email"></div>
          <div><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" maxlength="40" autocomplete="tel"></div>
          <div><label for="c-topic">What's this about?</label><select id="c-topic" name="topic"><option>Renting a house</option><option>My application</option><option>My lease or account</option><option>Section 8 / housing authority</option><option>Vendor or job inquiry</option><option>Owner / investor</option><option>Something else</option></select></div>
          <div><label for="c-msg">Message</label><textarea id="c-msg" name="message" required maxlength="4000"></textarea></div>
          <div class="note">We reply within one business day. Please don't include account numbers.</div>
          <div id="c-out"></div>
          <button class="btn btn-primary" type="submit" id="c-btn">Send message</button>
        </form>
      </div>
    </div>
  </div>
</section>
<script>
document.getElementById('cf').addEventListener('submit', async e => {
  e.preventDefault();
  const f = e.target, out = document.getElementById('c-out'), btn = document.getElementById('c-btn');
  const data = { name: f.name.value.trim(), email: f.email.value.trim() || null, phone: f.phone.value.trim() || null, topic: f.topic.value, message: f.message.value.trim(), page: location.pathname };
  if (!data.name || !data.message) { out.innerHTML = '<div class="err">Add your name and a message.</div>'; return; }
  if (!data.email && !data.phone) { out.innerHTML = '<div class="err">Add an email or phone number so we can reply.</div>'; return; }
  btn.disabled = true; btn.textContent = 'Sending…';
  try {
    const r = await fetch(RT.SB_URL + '/rest/v1/site_messages', { method: 'POST', headers: { 'Content-Type': 'application/json', apikey: RT.SB_KEY, Authorization: 'Bearer ' + RT.SB_KEY, Prefer: 'return=minimal' }, body: JSON.stringify(data) });
    if (!r.ok) throw new Error(r.status);
    f.reset(); out.innerHTML = '<div class="ok"><strong>Sent.</strong> We\\'ll get back to you within one business day.</div>'; btn.textContent = 'Send message'; btn.disabled = false;
  } catch (err) {
    out.innerHTML = '<div class="err">That didn\\'t go through. Call (205) 208-9793 or email <a href="mailto:info@rtmhouses.com">info@rtmhouses.com</a>.</div>'; btn.textContent = 'Send message'; btn.disabled = false;
  }
});
</script>
''' + foot()

# ---------------- careers / vendors ----------------
pages["careers.html"] = head("Jobs and vendors", "Work with Rising Tide Homes: maintenance technician jobs in Birmingham, AL, and how to become a preferred vendor for maintenance and construction.", "careers.html") + '''
<div class="page-head"><div class="wrap"><h1>Jobs and vendors</h1><p>We manage about 750 houses with an in-house team. We're usually hiring technicians and always taking vendor applications.</p></div></div>
<section class="section-tight">
  <div class="wrap">
    <div class="contact-grid">
      <div class="prose">
        <h2>Maintenance technician</h2>
        <p>Technicians complete work orders submitted by residents every day — everything from a sticking door to a water heater. We hire at three levels:</p>
        <ul>
          <li><strong>Level I</strong> — general labor: drywall repair, doors and windows, paint, cabinets.</li>
          <li><strong>Level II</strong> — broader home repair: routine electrical and plumbing, diagnostics around the house.</li>
          <li><strong>Level III</strong> — plumbing, HVAC, or electrical specialists.</li>
        </ul>
        <p>Pay depends on experience. After a 90-day probation, benefits include health, dental, and vision insurance, a gas allowance, 401(k), and paid vacation.</p>
        <p><a class="btn btn-primary" href="https://zfrmz.com/9aTxSbLh1swArGINVMto" rel="noopener">Apply for a technician job</a></p>
      </div>
      <div class="prose" id="vendors">
        <h2>Preferred vendors</h2>
        <p>Preferred vendors are outside contractors we hire job by job for maintenance and construction — plumbing, HVAC, electrical, roofing, flooring, turns, and more. Tell us what you do and where you work, include your license and insurance if you have them, and we'll be in touch when a job fits.</p>
        <p><a class="btn btn-primary" href="https://zfrmz.com/HpCEIFAjch2kQr6ilsBu" rel="noopener">Sign up as a vendor</a></p>
      </div>
    </div>
  </div>
</section>
''' + foot()

# ---------------- 404 ----------------
pages["404.html"] = head("Page not found", "That page doesn't exist. See available houses or go to the resident portal.", "404.html") + '''
<div class="page-head"><div class="wrap"><h1>That page isn't here</h1><p>The link may be old. Here's where most people are headed.</p></div></div>
<section class="section-tight"><div class="wrap" style="display:flex;gap:.75rem;flex-wrap:wrap">
  <a class="btn btn-primary" href="homes.html">Available houses</a>
  <a class="btn btn-primary" href="https://occupi.app/" rel="noopener" data-track="click_pay">Pay rent</a>
  <a class="btn btn-outline" href="https://leasepg.twa.rentmanager.com/" rel="noopener" data-track="click_portal">Resident portal</a>
  <a class="btn btn-outline" href="https://app.propertymeld.com/tenant/rising-tide-management" rel="noopener">Request a repair</a>
  <a class="btn btn-outline" href="contact.html">Contact us</a>
</div></section>
''' + foot()

os.makedirs(OUT, exist_ok=True)
for name, html in pages.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)
    print("wrote", name, len(html))

# robots + sitemap
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = ["", "homes.html", "apply.html", "residents.html", "contact.html", "careers.html"]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
