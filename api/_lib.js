// Shared helpers for the phone system. Files starting with "_" are not served as endpoints by Vercel.
//
// Settings come from Vercel environment variables (Project → Settings → Environment Variables), never from code:
//   TWILIO_ACCOUNT_SID   Twilio account ID (starts with AC)
//   TWILIO_AUTH_TOKEN    Twilio auth token (secret; used to check that requests really come from Twilio)
//   TWILIO_NUMBER        the tracking number shown on the site, e.g. +14695550123
//   FORWARD_TO           phone that rings first (the plumber, or your own cell until a plumber signs on); optional
//   ALERT_SMS_TO         comma-separated numbers that get a text for every missed call / voicemail
//   ADMIN_KEY            long random password for the call log page (/api/calls?key=...)
//   SITE_NAME            spoken name, defaults to "Garland Sewer Repair"
const crypto = require('crypto');
const twilio = require('twilio');

const cfg = {
    sid: process.env.TWILIO_ACCOUNT_SID || '',
    token: process.env.TWILIO_AUTH_TOKEN || '',
    number: process.env.TWILIO_NUMBER || '',
    forwardTo: (process.env.FORWARD_TO || '').trim(),
    alertTo: (process.env.ALERT_SMS_TO || '').split(',').map(s => s.trim()).filter(Boolean),
    adminKey: process.env.ADMIN_KEY || '',
    siteName: process.env.SITE_NAME || 'Garland Sewer Repair',
};

const VOICE = { voice: 'Polly.Joanna' };

function baseUrl(req) {
    const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0].trim();
    return `${proto}://${req.headers.host}`;
}

function abs(req, path) {
    return baseUrl(req) + path;
}

// Reject anything that isn't signed by Twilio with our auth token.
function fromTwilio(req) {
    if (!cfg.token) return false;
    const signature = req.headers['x-twilio-signature'] || '';
    return twilio.validateRequest(cfg.token, signature, abs(req, req.url), req.body || {});
}

function sendTwiml(res, response) {
    res.setHeader('Content-Type', 'text/xml');
    res.status(200).send(response.toString());
}

function forbid(res) {
    res.status(403).send('Forbidden');
}

function client() {
    return twilio(cfg.sid, cfg.token);
}

// Text everyone on ALERT_SMS_TO. Never throws: a failed text must not break the call.
async function alert(body) {
    if (!cfg.alertTo.length || !cfg.number || !cfg.sid) return;
    const c = client();
    await Promise.all(cfg.alertTo.map(to =>
        c.messages.create({ to, from: cfg.number, body: body.slice(0, 1500) })
            .catch(err => console.error('SMS to', to, 'failed:', err.message))));
}

function sameSecret(given, expected) {
    const a = Buffer.from(String(given || ''));
    const b = Buffer.from(String(expected || ''));
    return b.length > 0 && a.length === b.length && crypto.timingSafeEqual(a, b);
}

// Signed link to play one recording through /api/recording, so Twilio passwords never leave the server and a
// link in a text message only opens that one recording.
function recordingSig(sid) {
    return crypto.createHmac('sha256', cfg.adminKey || cfg.token).update(String(sid)).digest('hex').slice(0, 32);
}

function recordingLink(req, sid) {
    return abs(req, `/api/recording?sid=${encodeURIComponent(sid)}&sig=${recordingSig(sid)}`);
}

function prettyPhone(num) {
    const d = String(num || '').replace(/\D/g, '').replace(/^1(?=\d{10}$)/, '');
    return d.length === 10 ? `(${d.slice(0, 3)}) ${d.slice(3, 6)}-${d.slice(6)}` : String(num || 'unknown');
}

module.exports = {
    cfg, VOICE, abs, fromTwilio, sendTwiml, forbid, client, alert, sameSecret, prettyPhone,
    recordingSig, recordingLink, twiml: twilio.twiml,
};
