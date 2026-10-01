/* Rising Tide Homes — shared site script
   Listings come live from Tenant Turner's public feed (no key, no rebuilds).
   Apply links use Rent Manager unit ids from a read-only Supabase view.
   Analytics: page views + CTA clicks go to Supabase site_events (insert-only). */
(function () {
  'use strict';
  const RT = window.RT = {
    TT_FEED: 'https://app.tenantturner.com/listings-json/2342',
    SB_URL: 'https://csdsendpbnwycwhqwgbe.supabase.co',
    SB_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNzZHNlbmRwYm53eWN3aHF3Z2JlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5ODkxMTMsImV4cCI6MjA5MDU2NTExM30.-4ba13ihXjJiQapWhnuydTbXspw7-AqRdMA7AqRnGD4',
    APPLY_BASE: 'https://leasepg.twa.rentmanager.com/applynow',
    PORTAL: 'https://leasepg.twa.rentmanager.com/',
    PAY: 'https://occupi.app/',
    MELD: 'https://app.propertymeld.com/tenant/rising-tide-management',
    PHONE: '2052089793', PHONE_FMT: '(205) 208-9793',
    TEXT: '2055021552', TEXT_FMT: '205-502-1552',
    EMERGENCY: '2054193148', EMERGENCY_FMT: '205-419-3148'
  };

  /* ---------- helpers ---------- */
  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money = n => { const v = Number(String(n).replace(/[^0-9.]/g,'')); return isFinite(v) && v > 0 ? '$' + v.toLocaleString('en-US', {maximumFractionDigits:0}) : ''; };
  const addrKey = a => String(a || '').toLowerCase().replace(/[^a-z0-9]+/g, '');
  const num = v => { const n = parseFloat(v); return isFinite(n) ? n : null; };
  const fmtBath = v => { const n = num(v); if (n == null) return ''; return (n % 1 === 0 ? n.toFixed(0) : n.toFixed(1)); };
  RT.esc = esc; RT.money = money;

  /* ---------- analytics (fire-and-forget, never blocks) ---------- */
  const sid = (() => { try { let s = sessionStorage.getItem('rt_sid'); if (!s) { s = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem('rt_sid', s); } return s; } catch (e) { return 'na'; } })();
  const utm = (() => { try { const p = new URLSearchParams(location.search); const o = {}; ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','ref'].forEach(k => { if (p.get(k)) o[k] = p.get(k).slice(0,100); }); return Object.keys(o).length ? o : null; } catch (e) { return null; } })();
  RT.track = function (event, extra) {
    try {
      const body = Object.assign({
        event, path: location.pathname + (location.search ? location.search.slice(0, 120) : ''),
        referrer: (document.referrer || '').slice(0, 300) || null, utm, session_id: sid,
        device: matchMedia('(max-width: 760px)').matches ? 'mobile' : 'desktop', ua: navigator.userAgent.slice(0, 300)
      }, extra || {});
      const url = RT.SB_URL + '/rest/v1/site_events';
      const headers = { 'Content-Type': 'application/json', apikey: RT.SB_KEY, Authorization: 'Bearer ' + RT.SB_KEY, Prefer: 'return=minimal' };
      if (navigator.sendBeacon && !extra) { // page views can beacon; clicks need headers so use fetch keepalive
        fetch(url, { method: 'POST', headers, body: JSON.stringify(body), keepalive: true }).catch(() => {});
      } else {
        fetch(url, { method: 'POST', headers, body: JSON.stringify(body), keepalive: true }).catch(() => {});
      }
    } catch (e) {}
  };
  // click tracking via data-track="click_apply" (+ optional data-listing / data-addr)
  document.addEventListener('click', e => {
    const a = e.target.closest('[data-track]'); if (!a) return;
    RT.track(a.getAttribute('data-track'), { listing_id: a.getAttribute('data-listing') || null, listing_address: a.getAttribute('data-addr') || null });
  }, true);

  /* ---------- listings ---------- */
  let feedCache = null, mapCache = null;
  RT.listings = async function () {
    if (feedCache) return feedCache;
    try { const c = sessionStorage.getItem('rt_feed'); if (c) { const o = JSON.parse(c); if (Date.now() - o.t < 5 * 60 * 1000) { feedCache = o.d; return feedCache; } } } catch (e) {}
    const r = await fetch(RT.TT_FEED, { cache: 'no-store' });
    if (!r.ok) throw new Error('feed ' + r.status);
    const raw = await r.json();
    const list = (Array.isArray(raw) ? raw : []).map(x => ({
      id: String(x.id), address: x.address || x.title || '', city: x.city || '', state: x.state || 'AL', zip: x.zip || '',
      photo: x.photo || '', description: x.description || '', beds: num(x.beds), baths: num(x.baths),
      rent: num(x.rentAmount), available: x.dateAvailable || 'Now', schedule: (x.btnUrl || '').trim(),
      offer: x.specialOffer || null, fees: x.fees || '', pets: x.acceptPets || '', type: x.propertyType || '',
      lat: x.latitude, lng: x.longitude, activated: x.dateActivated || '', waitlist: !!x.enableWaitlist
    })).filter(x => x.address);
    // newest first
    list.sort((a, b) => (Date.parse(b.activated) || 0) - (Date.parse(a.activated) || 0));
    feedCache = list;
    try { sessionStorage.setItem('rt_feed', JSON.stringify({ t: Date.now(), d: list })); } catch (e) {}
    return list;
  };
  RT.unitMap = async function () {
    if (mapCache) return mapCache;
    try {
      const h = { apikey: RT.SB_KEY, Authorization: 'Bearer ' + RT.SB_KEY };
      let rows = [], off = 0; // PostgREST caps at 1000 rows per request; we have ~1,050 units
      for (let i = 0; i < 5; i++) {
        const r = await fetch(RT.SB_URL + '/rest/v1/site_unit_map?select=address_key,address,unit_id&order=unit_id&limit=1000&offset=' + off, { headers: h });
        const page = r.ok ? await r.json() : []; rows = rows.concat(page); if (page.length < 1000) break; off += 1000;
      }
      const shortKey = a => { const t = String(a || '').toLowerCase().split(/\s+/).filter(Boolean); return t.length >= 2 ? (t[0] + t[1]).replace(/[^a-z0-9]/g, '') : ''; };
      RT._shortKey = shortKey;
      mapCache = {}; const short = {};
      rows.forEach(row => { if (!row.address_key) return; if (!(row.address_key in mapCache)) mapCache[row.address_key] = row.unit_id; const sk = shortKey(row.address); if (sk) (short[sk] = short[sk] || []).push(row.unit_id); });
      mapCache.__short = short;
    } catch (e) { mapCache = {}; }
    return mapCache;
  };
  RT.applyUrl = function (l, map) {
    const k = addrKey(l.address);
    let id = map && map[k];
    if (!id && map && map.__short) { // e.g. TT "1024 43rd St Ensley" vs RM "1024 43rd St": match on house number + street name
      const sk = RT._shortKey(l.address); const c = sk && map.__short[sk]; if (c && c.length === 1) id = c[0];
    }
    return id ? RT.APPLY_BASE + '?unitId=' + encodeURIComponent(id) : RT.APPLY_BASE;
  };
  RT.detailUrl = l => 'home.html?id=' + encodeURIComponent(l.id);

  RT.card = function (l, map) {
    const facts = [];
    if (l.beds != null) facts.push('<span>' + l.beds + ' bed' + (l.beds === 1 ? '' : 's') + '</span>');
    if (l.baths != null) facts.push('<span>' + fmtBath(l.baths) + ' bath' + (l.baths === 1 ? '' : 's') + '</span>');
    if (l.type) facts.push('<span>' + esc(l.type) + '</span>');
    const tag = l.offer ? '<span class="tag offer">Special offer</span>' : (l.available && /now/i.test(l.available) ? '<span class="tag">Available now</span>' : (l.available ? '<span class="tag">Available ' + esc(l.available) + '</span>' : ''));
    return '<article class="card">' +
      '<a class="photo" href="' + RT.detailUrl(l) + '" data-track="click_listing" data-listing="' + esc(l.id) + '" data-addr="' + esc(l.address) + '" aria-label="' + esc(l.address) + '">' +
        (l.photo ? '<img src="' + esc(l.photo) + '" alt="' + esc(l.address) + '" loading="lazy">' : '') + tag + '</a>' +
      '<div class="body">' +
        '<div class="rent">' + money(l.rent) + '<span>/mo</span></div>' +
        '<div class="facts">' + facts.join('') + '</div>' +
        '<a class="addr" href="' + RT.detailUrl(l) + '">' + esc(l.address) + '</a>' +
        '<div class="city">' + esc(l.city) + ', ' + esc(l.state) + ' ' + esc(l.zip) + '</div>' +
        '<div class="cta">' +
          '<a class="btn btn-primary" href="' + esc(l.schedule) + '" target="_blank" rel="noopener" data-track="click_schedule" data-listing="' + esc(l.id) + '" data-addr="' + esc(l.address) + '">Book a showing</a>' +
          '<a class="btn btn-outline" href="' + esc(RT.applyUrl(l, map)) + '" target="_blank" rel="noopener" data-track="click_apply" data-listing="' + esc(l.id) + '" data-addr="' + esc(l.address) + '">Apply</a>' +
        '</div>' +
      '</div></article>';
  };

  RT.filter = function (list, f) {
    return list.filter(l => {
      if (f.city && l.city.toLowerCase() !== f.city.toLowerCase()) return false;
      if (f.beds && (l.beds == null || l.beds < Number(f.beds))) return false;
      if (f.max && (l.rent == null || l.rent > Number(f.max))) return false;
      if (f.q) { const q = f.q.toLowerCase(); if (!(l.address + ' ' + l.city + ' ' + l.zip).toLowerCase().includes(q)) return false; }
      return true;
    });
  };

  RT.renderGrid = async function (el, opts) {
    opts = opts || {};
    el.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';
    try {
      const [list, map] = await Promise.all([RT.listings(), RT.unitMap()]);
      let items = RT.filter(list, opts.filter || {});
      if (opts.limit) items = items.slice(0, opts.limit);
      if (!items.length) {
        el.innerHTML = '<div class="empty" style="grid-column:1/-1"><p><strong>No houses match that search.</strong></p><p>Try fewer filters, or <a href="homes.html">see every available house</a>. New homes are listed most weeks.</p></div>';
      } else {
        el.innerHTML = items.map(l => RT.card(l, map)).join('');
      }
      if (opts.onDone) opts.onDone(items, list);
      return items;
    } catch (e) {
      el.innerHTML = '<div class="empty" style="grid-column:1/-1"><p><strong>The listing feed didn\'t load.</strong></p><p>Refresh the page, or see the live list at <a href="https://app.tenantturner.com/listings/risingtidemanagement" rel="noopener">our showing page</a>.</p></div>';
      if (opts.onDone) opts.onDone([], []);
      return [];
    }
  };

  /* ---------- header / nav ---------- */
  function initNav() {
    const btn = $('.menu-btn'), nav = $('.mobile-nav'); if (!btn || !nav) return;
    btn.addEventListener('click', () => { const open = nav.getAttribute('data-open') === 'true'; nav.setAttribute('data-open', String(!open)); btn.setAttribute('aria-expanded', String(!open)); });
    const here = location.pathname.split('/').pop() || 'index.html';
    $$('.nav a, .mobile-nav a').forEach(a => { const h = (a.getAttribute('href') || '').split('#')[0]; if (h && h === here) a.setAttribute('aria-current', 'page'); });
  }

  /* ---------- hero count ---------- */
  async function initCount() {
    const el = $('[data-count]'); if (!el) return;
    try { const list = await RT.listings(); el.querySelector('b').textContent = list.length; el.querySelector('span.lbl').textContent = list.length === 1 ? 'house available now' : 'houses available now'; } catch (e) { el.hidden = true; }
  }

  document.addEventListener('DOMContentLoaded', () => { initNav(); initCount(); RT.track('page_view'); });
})();
