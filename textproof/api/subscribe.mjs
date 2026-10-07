// Website email signup. Adds the address to the "TextProof" segment in Resend.
// RESEND_API_KEY and RESEND_SEGMENT_ID live in Vercel's environment settings, never in code.
// Spam defence: a hidden honeypot field, a simple per-IP rate limit and an email format check.

const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_IP = 5;
const hits = new Map();

function clientIp(req) {
  const fwd = req.headers['x-forwarded-for'];
  if (typeof fwd === 'string' && fwd.length) return fwd.split(',')[0].trim();
  return req.headers['x-real-ip'] || 'unknown';
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { email, website } = req.body || {};

  // Honeypot: people never see this field, bots fill it in. Pretend it worked.
  if (typeof website === 'string' && website.trim() !== '') {
    res.status(200).json({ ok: true });
    return;
  }

  const clean = typeof email === 'string' ? email.trim().toLowerCase() : '';
  if (!clean || clean.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(clean)) {
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
  const segment = process.env.RESEND_SEGMENT_ID;
  if (!key || !segment) {
    console.error('Signup: RESEND_API_KEY or RESEND_SEGMENT_ID is not set.');
    res.status(503).json({ error: 'Sign-up is not available right now.' });
    return;
  }

  try {
    const r = await fetch('https://api.resend.com/contacts', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: clean, unsubscribed: false, segments: [{ id: segment }] }),
    });
    if (!r.ok) {
      const body = await r.text();
      // Someone signing up twice is not an error from their point of view.
      if (r.status === 409 || /already exists/i.test(body)) {
        res.status(200).json({ ok: true });
        return;
      }
      console.error('Signup: Resend returned', r.status, body.slice(0, 300));
      res.status(502).json({ error: 'Something went wrong. Please try again.' });
      return;
    }
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Signup: request failed', err && err.message);
    res.status(502).json({ error: 'Something went wrong. Please try again.' });
  }
}
