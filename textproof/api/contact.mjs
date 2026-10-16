// textproof.net contact form. Emails the message to hello@textproof.net via Resend.
// RESEND_API_KEY lives in Vercel's environment settings, never in code.
// Optional: CONTACT_TO (defaults to hello@textproof.net) and CONTACT_FROM
// (a Resend-verified sender; defaults to website@textproof.net).
// Spam defence: a hidden honeypot field, a simple per-IP rate limit and input limits.

const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_IP = 6;
const hits = new Map();

function clientIp(req) {
  const fwd = req.headers['x-forwarded-for'];
  if (typeof fwd === 'string' && fwd.length) return fwd.split(',')[0].trim();
  return req.headers['x-real-ip'] || 'unknown';
}

function text(v, max) {
  return typeof v === 'string' ? v.trim().slice(0, max) : '';
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const body = req.body || {};

  // Honeypot: people never see this field, bots fill it in. Pretend it worked.
  if (typeof body.website === 'string' && body.website.trim() !== '') {
    res.status(200).json({ ok: true });
    return;
  }

  const email = text(body.email, 254).toLowerCase();
  const name = text(body.name, 120);
  const company = text(body.company, 160);
  const topic = text(body.topic, 60) || 'General enquiry';
  const message = text(body.message, 4000);

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    res.status(400).json({ error: 'That email address does not look right.' });
    return;
  }

  const now = Date.now();
  const ip = clientIp(req);
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= MAX_PER_IP) {
    res.status(429).json({ error: 'Too many attempts. Please try again later.' });
    return;
  }
  recent.push(now);
  hits.set(ip, recent);

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.error('Contact: RESEND_API_KEY is not set.');
    res.status(503).json({ error: 'The form is not available right now. Please email hello@textproof.net.' });
    return;
  }
  const to = process.env.CONTACT_TO || 'hello@textproof.net';
  const from = process.env.CONTACT_FROM || 'TextProof <website@textproof.net>';

  const rows = [
    ['Topic', topic],
    ['Name', name || '—'],
    ['Company', company || '—'],
    ['Email', email],
    ['Message', message || '—'],
  ];
  const html = `<div style="font:15px/1.6 -apple-system,Segoe UI,sans-serif;color:#111">
    <h2 style="margin:0 0 12px">Website: ${escapeHtml(topic)}</h2>
    <table cellpadding="6" style="border-collapse:collapse">${rows
      .map(([k, v]) => `<tr><td style="color:#667;vertical-align:top;white-space:nowrap">${k}</td><td style="white-space:pre-wrap">${escapeHtml(v)}</td></tr>`)
      .join('')}</table>
    <p style="color:#889;font-size:12px;margin-top:16px">Sent from textproof.net · ${escapeHtml(ip)}</p></div>`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject: `[textproof.net] ${topic}${name ? ` — ${name}` : ''}`,
        html,
        text: rows.map(([k, v]) => `${k}: ${v}`).join('\n'),
      }),
    });
    if (!r.ok) {
      console.error('Contact: Resend returned', r.status, (await r.text()).slice(0, 300));
      res.status(502).json({ error: 'Something went wrong. Please email hello@textproof.net instead.' });
      return;
    }
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Contact: request failed', err && err.message);
    res.status(502).json({ error: 'Something went wrong. Please email hello@textproof.net instead.' });
  }
}
