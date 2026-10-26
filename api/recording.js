// Plays one call recording: /api/recording?sid=RE...&sig=...  (links come from texts and the call log).
// The signature only unlocks that single recording; Twilio credentials stay on the server.
const crypto = require('crypto');
const { cfg, recordingSig } = require('./_lib');

module.exports = async (req, res) => {
    const sid = String(req.query.sid || '');
    const sig = String(req.query.sig || '');
    const expected = recordingSig(sid);
    const ok = /^RE[0-9a-f]{32}$/i.test(sid) && sig.length === expected.length
        && crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected));
    if (!ok) return res.status(404).send('Not found');

    const url = `https://api.twilio.com/2010-04-01/Accounts/${cfg.sid}/Recordings/${sid}.mp3`;
    const auth = Buffer.from(`${cfg.sid}:${cfg.token}`).toString('base64');
    const upstream = await fetch(url, { headers: { Authorization: `Basic ${auth}` } });
    if (!upstream.ok) return res.status(upstream.status === 404 ? 404 : 502).send('Recording unavailable');

    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'private, no-store');
    res.setHeader('X-Robots-Tag', 'noindex');
    res.status(200).send(Buffer.from(await upstream.arrayBuffer()));
};
