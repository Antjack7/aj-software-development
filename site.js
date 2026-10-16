/* AJ Software Development — behaviour.
   1. Signal field: a flow-field of particles behind the hero that leans toward the pointer.
   2. Pointer parallax on the device stages.
   3. Each product lends the page its colours as it scrolls into view.
   4. Reveal on scroll, nav state, progress bar, mobile menu.
   5. Forms: post JSON to /api/contact and report back inline. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(pointer: fine)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- 1. Signal field ---------- */
  const canvas = $('#field');
  if (canvas && !reduce) {
    const ctx = canvas.getContext('2d', { alpha: true });
    let w, h, dpr, pts = [], t = 0, raf = 0, visible = true;
    const mouse = { x: -1e4, y: -1e4, tx: -1e4, ty: -1e4 };
    const hero = $('.hero');
    const glowVar = () => getComputedStyle(document.documentElement).getPropertyValue('--glow').trim() || '#5b9dff';

    function size() {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(420, (w * h) / 4200));
      pts = Array.from({ length: n }, () => ({ x: Math.random() * w, y: Math.random() * h, vx: 0, vy: 0, a: .35 + Math.random() * .65, r: .9 + Math.random() * 1.6 }));
    }
    // A cheap, smooth pseudo-noise built from sines; enough for a drifting current.
    const noise = (x, y, t) => Math.sin(x * .0021 + t * .35) * Math.cos(y * .0019 - t * .22) + Math.sin((x + y) * .0012 + t * .17) * .6;
    function frame() {
      if (!visible) { raf = 0; return; }
      t += .008;
      mouse.x += (mouse.tx - mouse.x) * .08; mouse.y += (mouse.ty - mouse.y) * .08;
      // Fade the previous frame instead of clearing it: particles leave glowing trails.
      ctx.globalCompositeOperation = 'destination-out'; ctx.globalAlpha = .16; ctx.fillRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'source-over';
      const col = glowVar();
      ctx.strokeStyle = col; ctx.fillStyle = col;
      for (const p of pts) {
        const ang = noise(p.x, p.y, t) * Math.PI * 1.6;
        p.vx += Math.cos(ang) * .035; p.vy += Math.sin(ang) * .035;
        const dx = mouse.x - p.x, dy = mouse.y - p.y, d2 = dx * dx + dy * dy;
        if (d2 < 260 * 260) { const f = (1 - Math.sqrt(d2) / 260) * .4; p.vx += dx / 220 * f; p.vy += dy / 220 * f; }
        p.vx *= .965; p.vy *= .965;
        const ox = p.x, oy = p.y;
        p.x += p.vx; p.y += p.vy;
        if (p.x < -20) p.x = w + 20; if (p.x > w + 20) p.x = -20; if (p.y < -20) p.y = h + 20; if (p.y > h + 20) p.y = -20;
        ctx.globalAlpha = p.a;
        ctx.lineWidth = p.r;
        ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(p.x, p.y); ctx.stroke();
      }
      // Faint links between near neighbours: the "joined-up" idea.
      ctx.globalAlpha = .26; ctx.lineWidth = .7;
      for (let i = 0; i < pts.length; i += 2) for (let j = i + 2; j < pts.length; j += 3) {
        const a = pts[i], b = pts[j], dx = a.x - b.x, dy = a.y - b.y;
        if (dx * dx + dy * dy < 120 * 120) { ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
      }
      ctx.globalAlpha = 1;
      raf = requestAnimationFrame(frame);
    }
    size(); addEventListener('resize', size, { passive: true });
    hero.addEventListener('pointermove', (e) => { const r = canvas.getBoundingClientRect(); mouse.tx = e.clientX - r.left; mouse.ty = e.clientY - r.top; }, { passive: true });
    hero.addEventListener('pointerleave', () => { mouse.tx = -1e4; mouse.ty = -1e4; });
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible && !raf) raf = requestAnimationFrame(frame); }, { threshold: 0 }).observe(hero);
    raf = requestAnimationFrame(frame);
  }

  /* ---------- 2. Pointer parallax ---------- */
  if (fine && !reduce) {
    $$('.stage, .shots').forEach((stage) => {
      const items = $$('[data-depth]', stage);
      let raf = 0, px = 0, py = 0;
      const apply = () => { raf = 0; items.forEach((el) => { const d = +el.dataset.depth / 100; el.style.setProperty('--px', `${px * d}px`); el.style.setProperty('--py', `${py * d}px`); }); };
      stage.addEventListener('pointermove', (e) => { const r = stage.getBoundingClientRect(); px = (e.clientX - r.left - r.width / 2) * .6; py = (e.clientY - r.top - r.height / 2) * .6; if (!raf) raf = requestAnimationFrame(apply); }, { passive: true });
      stage.addEventListener('pointerleave', () => { px = 0; py = 0; if (!raf) raf = requestAnimationFrame(apply); });
    });
  }

  /* ---------- 3. Product colour takes the page ---------- */
  const root = document.documentElement;
  const defaults = { glow: '#5b9dff', glow2: '#2f6fe0' };
  $$('.product').forEach((p) => {
    p.style.setProperty('--p1', p.dataset.glow); p.style.setProperty('--p2', p.dataset.glow2);
    // Lighten the headline accent so it reads on dark for every product colour.
    p.style.setProperty('--p1-text', `color-mix(in srgb, ${p.dataset.glow} 70%, white)`);
  });
  const prodObs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      e.target.classList.toggle('in', e.isIntersecting);
      if (e.isIntersecting) { root.style.setProperty('--glow', e.target.dataset.glow); root.style.setProperty('--glow2', e.target.dataset.glow2); }
    });
  }, { threshold: .45 });
  $$('.product').forEach((p) => prodObs.observe(p));
  const heroEl = $('.hero');
  new IntersectionObserver(([e]) => { if (e.isIntersecting) { root.style.setProperty('--glow', defaults.glow); root.style.setProperty('--glow2', defaults.glow2); } }, { threshold: .3 }).observe(heroEl);

  /* ---------- 4. Reveal, nav, progress, menu ---------- */
  $$('.sec-head, .product-copy, .product-visual, .flow, .ajai-side, .svc, .about-copy, .timeline, .contact-copy, .cform').forEach((el) => el.classList.add('rv'));
  const rvObs = new IntersectionObserver((entries) => entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); rvObs.unobserve(e.target); } }), { threshold: .12, rootMargin: '0px 0px -5% 0px' });
  $$('.rv').forEach((el) => rvObs.observe(el));
  /* Boot sequence: a short, honest readout, then the page wipes in. Once per session. */
  const boot = $('#boot');
  const countUp = () => $$('[data-count]').forEach((el) => {
    const end = +el.dataset.count, t0 = performance.now(), dur = 1100;
    const step = (now) => { const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(end * e); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
  const revealHero = () => { heroEl.classList.add('in'); if (!reduce) countUp(); };
  let seen = false; try { seen = sessionStorage.getItem('ajboot') === '1'; } catch {}
  if (boot && !reduce && !seen) {
    document.body.classList.add('booting');
    try { sessionStorage.setItem('ajboot', '1'); } catch {}
    const line = $('.boot-line', boot), log = $('.boot-log', boot);
    const lines = [
      ['$ ajsoftware --boot', ''],
      ['apps.live', '6', 'ok'],
      ['data.residency', 'uk-south', 'ok'],
      ['trackers', '0', 'ok'],
      ['render', 'hand-written html · css · js', 'ok'],
    ];
    let done = false;
    const finish = () => {
      if (done) return; done = true;
      boot.classList.add('out'); document.body.classList.remove('booting');
      revealHero();
      setTimeout(() => { boot.hidden = true; }, 1000);
    };
    boot.addEventListener('click', finish);
    const type = (text, cb) => { let i = 0; const tick = () => { line.textContent = text.slice(0, ++i); if (i < text.length) setTimeout(tick, 14 + Math.random() * 22); else cb(); }; tick(); };
    const commit = (l) => {
      const s = document.createElement('span');
      if (l[2]) s.innerHTML = `<span class="ok">✓</span> <span class="k">${l[0].padEnd(16, ' ')}</span><span class="v">${l[1]}</span>
`;
      else s.innerHTML = `<span class="v">${l[0]}</span>
`;
      log.insertBefore(s, line); line.textContent = '';
    };
    const run = (i) => {
      if (done) return;
      if (i >= lines.length) { setTimeout(finish, 420); return; }
      const l = lines[i], shown = l[2] ? `${l[0]} ${l[1]}` : l[0];
      type(shown, () => setTimeout(() => { commit(l); run(i + 1); }, i === 0 ? 260 : 120));
    };
    setTimeout(() => run(0), 350);
    setTimeout(finish, 6000); // never hold the page hostage
  } else {
    if (boot) boot.hidden = true;
    requestAnimationFrame(() => setTimeout(revealHero, 60));
  }

  const progress = $('#progress');
  const onScroll = () => {
    document.body.classList.toggle('scrolled', scrollY > 24);
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${max > 0 ? (scrollY / max) * 100 : 0}%`;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  const menuBtn = $('.menu-btn'), menu = $('#mobile-menu');
  menuBtn.addEventListener('click', () => { const open = menuBtn.getAttribute('aria-expanded') === 'true'; menuBtn.setAttribute('aria-expanded', String(!open)); menu.hidden = open; });
  $$('a', menu).forEach((a) => a.addEventListener('click', () => { menuBtn.setAttribute('aria-expanded', 'false'); menu.hidden = true; }));

  /* ---------- 5. Forms ---------- */
  $$('form[action="/api/contact"]').forEach((form) => {
    const note = $('.form-note', form), btn = $('button[type=submit]', form), original = note.textContent;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email || '')) { note.className = 'form-note err'; note.textContent = 'Please enter a valid email address.'; return; }
      if ('message' in data && !data.message.trim()) { note.className = 'form-note err'; note.textContent = 'Tell us a little about what you need.'; return; }
      btn.disabled = true; note.className = 'form-note'; note.textContent = 'Sending…';
      try {
        const r = await fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        const j = await r.json().catch(() => ({}));
        if (r.ok && j.ok) { note.className = 'form-note ok'; note.textContent = form.id === 'interest' ? 'Thank you. You\'re on the list.' : 'Thank you. Anthony will reply within a working day.'; form.reset(); }
        else { note.className = 'form-note err'; note.textContent = j.error || 'Something went wrong. Please email anthony@ajsoftwaredev.org.'; }
      } catch { note.className = 'form-note err'; note.textContent = 'No connection. Please email anthony@ajsoftwaredev.org.'; }
      btn.disabled = false;
      if (note.classList.contains('ok')) setTimeout(() => { note.className = 'form-note'; note.textContent = original; }, 8000);
    });
  });
})();
