// Explainer engine: a 3D stage with two phones, a drifting mote field, and a step-by-step story.
// Each page defines window.STORY = { app, accent, phones:[leftLabel,rightLabel], steps:[...] } before this runs.
(function () {
  const S = window.STORY;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.style.setProperty('--accent', S.accent);
  document.documentElement.style.setProperty('--accent-rgb', S.accentRgb);

  // ---------- motes ----------
  const cv = document.getElementById('motes'); const cx = cv.getContext('2d');
  let W, H, motes = [], mx = 0, my = 0, scroll = 0;
  function size() { W = cv.width = innerWidth * devicePixelRatio; H = cv.height = innerHeight * devicePixelRatio; cv.style.width = innerWidth + 'px'; cv.style.height = innerHeight + 'px'; }
  function seed() { motes = Array.from({ length: 70 }, (_, i) => { const d = i % 3; return { d, x: Math.random() * W, y: Math.random() * H, r: [1.2, 2.2, 3.6][d] * devicePixelRatio, a: [0.18, 0.32, 0.5][d], vx: ([0.08, 0.16, 0.3][d]) * (Math.random() < 0.5 ? -1 : 1) * devicePixelRatio, ph: Math.random() * 6.28, sp: 0.004 + Math.random() * 0.006 }; }); }
  size(); seed(); addEventListener('resize', () => { size(); seed(); });
  addEventListener('mousemove', (e) => { mx = (e.clientX / innerWidth - 0.5); my = (e.clientY / innerHeight - 0.5); });
  addEventListener('scroll', () => { scroll = scrollY; }, { passive: true });
  function draw(t) {
    cx.clearRect(0, 0, W, H);
    for (const m of motes) {
      if (!reduce) { m.x += m.vx; m.ph += m.sp; }
      if (m.x < -20) m.x = W + 20; if (m.x > W + 20) m.x = -20;
      const depth = [0.3, 0.6, 1][m.d];
      const px = m.x + mx * 40 * depth * devicePixelRatio, py = m.y + Math.sin(m.ph) * 14 * devicePixelRatio * depth - (scroll * 0.15 * depth * devicePixelRatio) % (H + 40) + my * 30 * depth * devicePixelRatio;
      const yy = ((py % (H + 40)) + H + 40) % (H + 40) - 20;
      cx.beginPath(); cx.arc(px, yy, m.r, 0, 6.28);
      cx.fillStyle = `rgba(${S.accentRgb},${m.a})`; cx.shadowColor = `rgba(${S.accentRgb},0.9)`; cx.shadowBlur = m.r * 4; cx.fill();
    }
    if (!reduce) requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);

  // ---------- stage ----------
  const stage = document.getElementById('stage');
  const phoneL = document.getElementById('phoneL'), phoneR = document.getElementById('phoneR');
  const screenL = phoneL.querySelector('.screen'), screenR = phoneR.querySelector('.screen');
  const labelL = phoneL.querySelector('.plabel'), labelR = phoneR.querySelector('.plabel');
  labelL.textContent = S.phones[0]; labelR.textContent = S.phones[1];
  const link = document.getElementById('link'), signal = document.getElementById('signal');
  const caption = document.getElementById('caption'), stepNo = document.getElementById('stepNo'), stepTitle = document.getElementById('stepTitle');
  const dots = document.getElementById('dots'), list = document.getElementById('steps');
  let i = 0, timer = null, playing = true;

  // tilt the whole stage with the mouse (3D)
  addEventListener('mousemove', (e) => {
    if (reduce) return;
    const rx = (0.5 - e.clientY / innerHeight) * 10, ry = (e.clientX / innerWidth - 0.5) * 16;
    stage.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
  });

  S.steps.forEach((st, k) => {
    const d = document.createElement('button'); d.className = 'dot'; d.setAttribute('aria-label', `Step ${k + 1}`); d.onclick = () => { go(k); pause(); }; dots.appendChild(d);
    const li = document.createElement('li'); li.innerHTML = `<b>${k + 1}</b><span><strong>${st.title}</strong><br>${st.caption}</span>`; li.onclick = () => { go(k); pause(); }; list.appendChild(li);
  });

  function flip(el, html) {
    el.classList.add('flipping');
    setTimeout(() => { el.innerHTML = html; el.classList.remove('flipping'); }, reduce ? 0 : 260);
  }
  function go(k) {
    i = (k + S.steps.length) % S.steps.length;
    const st = S.steps[i];
    flip(screenL, st.left || '<div class="idle">·</div>');
    flip(screenR, st.right || '<div class="idle">·</div>');
    phoneL.classList.toggle('lit', !!st.litLeft); phoneR.classList.toggle('lit', !!st.litRight);
    phoneL.classList.toggle('focus', st.focus === 'left'); phoneR.classList.toggle('focus', st.focus === 'right');
    link.classList.toggle('on', !!st.signal); link.classList.toggle('done', !!st.linked);
    signal.classList.toggle('run', !!st.signal && !reduce); signal.classList.toggle('reverse', st.signal === 'back');
    stepNo.textContent = `Step ${i + 1} of ${S.steps.length}`; stepTitle.textContent = st.title; caption.textContent = st.caption;
    [...dots.children].forEach((d, j) => d.classList.toggle('on', j === i));
    [...list.children].forEach((d, j) => d.classList.toggle('on', j === i));
    if (navigator.vibrate && st.buzz) navigator.vibrate(st.buzz);
    document.getElementById('prog').style.animation = 'none'; void document.getElementById('prog').offsetWidth;
    document.getElementById('prog').style.animation = playing && !reduce ? 'prog 5.2s linear forwards' : 'none';
  }
  function next() { go(i + 1); }
  function play() { playing = true; document.getElementById('playBtn').textContent = 'Pause'; clearInterval(timer); timer = setInterval(next, 5200); go(i); }
  function pause() { playing = false; document.getElementById('playBtn').textContent = 'Play'; clearInterval(timer); document.getElementById('prog').style.animation = 'none'; }
  document.getElementById('playBtn').onclick = () => (playing ? pause() : play());
  document.getElementById('prevBtn').onclick = () => { go(i - 1); pause(); };
  document.getElementById('nextBtn').onclick = () => { go(i + 1); pause(); };
  addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') { go(i + 1); pause(); } if (e.key === 'ArrowLeft') { go(i - 1); pause(); } if (e.key === ' ') { e.preventDefault(); playing ? pause() : play(); } });
  if (reduce) { playing = false; document.getElementById('playBtn').textContent = 'Play'; go(0); } else play();
})();
