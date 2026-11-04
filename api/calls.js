// Private call log: https://www.garlandsewerrepair.com/api/calls?key=YOUR_ADMIN_KEY
// Lists the latest calls to the tracking number with length, outcome and recordings. Useful proof for plumbers.
const { cfg, client, sameSecret, prettyPhone, recordingLink } = require('./_lib');

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

module.exports = async (req, res) => {
    if (!sameSecret(req.query.key, cfg.adminKey)) return res.status(404).send('Not found');
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Robots-Tag', 'noindex');
    let rows = '';
    let total = 0;
    try {
        const c = client();
        const [calls, recordings] = await Promise.all([
            c.calls.list({ to: cfg.number, limit: 100 }),
            c.recordings.list({ limit: 200 }),
        ]);
        const recsByCall = new Map();
        for (const r of recordings) {
            if (!recsByCall.has(r.callSid)) recsByCall.set(r.callSid, []);
            recsByCall.get(r.callSid).push(r);
        }
        total = calls.length;
        rows = calls.map(call => {
            const recs = (recsByCall.get(call.sid) || []).map(r =>
                `<a href="${esc(recordingLink(req, r.sid))}" target="_blank" rel="noopener">▶ ${esc(r.duration)}s</a>`).join(' ');
            const when = call.startTime ? new Date(call.startTime).toLocaleString('en-US', { timeZone: 'America/Chicago' }) : '';
            return `<tr><td>${esc(when)}</td><td>${esc(prettyPhone(call.from))}</td><td>${esc(call.duration)}s</td>`
                + `<td>${esc(call.status)}</td><td>${recs || '-'}</td></tr>`;
        }).join('');
    } catch (err) {
        console.error(err);
        rows = `<tr><td colspan="5">Could not load calls: ${esc(err.message)}</td></tr>`;
    }
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200).send(`<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Call log | ${esc(cfg.siteName)}</title>
<style>body{font:15px/1.5 system-ui,sans-serif;margin:24px;color:#0f1f33}table{border-collapse:collapse;width:100%}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #dce3ea}th{background:#f4f7fa}a{color:#c9520e}</style></head>
<body><h1>${esc(cfg.siteName)}: call log</h1><p>Latest ${total} calls to ${esc(prettyPhone(cfg.number))}. Times are Dallas time.</p>
<table><thead><tr><th>When</th><th>Caller</th><th>Length</th><th>Status</th><th>Recordings</th></tr></thead><tbody>${rows}</tbody></table>
</body></html>`);
};
