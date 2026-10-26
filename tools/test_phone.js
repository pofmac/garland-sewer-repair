// Offline checks for the phone system: run with `npm test`. Simulates Twilio's signed webhook requests against
// each handler and checks the TwiML that comes back. No network calls (SMS alerts are disabled here).
process.env.TWILIO_AUTH_TOKEN = 'test-token';
process.env.TWILIO_ACCOUNT_SID = 'ACtest';
process.env.TWILIO_NUMBER = '+14695550100';
process.env.ADMIN_KEY = 'admin-test-key';
const assert = require('assert');
const twilio = require('twilio');

const HOST = 'www.garlandsewerrepair.com';

function load(name, env = {}) {
    for (const k of Object.keys(require.cache)) if (k.includes('/api/')) delete require.cache[k];
    const saved = {};
    for (const [k, v] of Object.entries(env)) { saved[k] = process.env[k]; process.env[k] = v; }
    const mod = require(`../api/${name}`);
    return { mod, restore: () => { for (const [k, v] of Object.entries(saved)) { if (v === undefined) delete process.env[k]; else process.env[k] = v; } } };
}

async function call(handler, path, body = {}, { signed = true } = {}) {
    const url = `https://${HOST}${path}`;
    const headers = { host: HOST, 'x-forwarded-proto': 'https' };
    if (signed) headers['x-twilio-signature'] = twilio.getExpectedTwilioSignature('test-token', url, body);
    const query = Object.fromEntries(new URL(url).searchParams);
    const res = { code: 0, headers: {}, body: '', setHeader(k, v) { this.headers[k] = v; }, status(c) { this.code = c; return this; }, send(b) { this.body = String(b); return this; } };
    await handler({ method: 'POST', url: path, headers, body, query }, res);
    return res;
}

(async () => {
    let r;
    // Unsigned requests are refused.
    let { mod, restore } = load('voice', { FORWARD_TO: '+12145550199' });
    r = await call(mod, '/api/voice', { From: '+19725551234' }, { signed: false });
    assert.strictEqual(r.code, 403);

    // Incoming call with a forward number: notice, then dial with whisper, recording and after-dial action.
    r = await call(mod, '/api/voice', { From: '+19725551234' });
    assert.strictEqual(r.code, 200);
    assert.match(r.body, /may be recorded/);
    assert.match(r.body, /<Dial[^>]*record="record-from-answer-dual"/);
    assert.match(r.body, /action="https:\/\/www\.garlandsewerrepair\.com\/api\/after-dial"/);
    assert.match(r.body, /<Number url="https:\/\/www\.garlandsewerrepair\.com\/api\/whisper">\+12145550199<\/Number>/);
    restore();

    // No forward number yet: straight to the message line.
    ({ mod, restore } = load('voice', { FORWARD_TO: '' }));
    r = await call(mod, '/api/voice', { From: '+19725551234' });
    assert.match(r.body, /<Redirect>https:\/\/www\.garlandsewerrepair\.com\/api\/after-dial\?nobody=1<\/Redirect>/);
    restore();

    // Whisper asks the plumber to press 1; pressing 1 bridges, anything else hangs up their leg.
    ({ mod } = load('whisper'));
    r = await call(mod, '/api/whisper', {});
    assert.match(r.body, /<Gather numDigits="1"[^>]*>.*Press 1 to accept/);
    ({ mod } = load('whisper-check'));
    r = await call(mod, '/api/whisper-check', { Digits: '1' });
    assert.doesNotMatch(r.body, /Hangup/);
    r = await call(mod, '/api/whisper-check', { Digits: '9' });
    assert.match(r.body, /<Hangup\/>/);

    // After dial: connected calls hang up; missed calls record a message.
    ({ mod } = load('after-dial'));
    r = await call(mod, '/api/after-dial', { From: '+19725551234', DialCallStatus: 'completed', DialBridged: 'true', DialCallDuration: '95' });
    assert.match(r.body, /<Hangup\/>/);
    assert.doesNotMatch(r.body, /<Record/);
    r = await call(mod, '/api/after-dial', { From: '+19725551234', DialCallStatus: 'no-answer' });
    assert.match(r.body, /<Record[^>]*transcribe="true"/);
    assert.match(r.body, /action="https:\/\/www\.garlandsewerrepair\.com\/api\/voicemail-done"/);
    r = await call(mod, '/api/after-dial?nobody=1', { From: '+19725551234' });
    assert.match(r.body, /<Record/);

    // Voicemail done thanks the caller.
    ({ mod } = load('voicemail-done'));
    r = await call(mod, '/api/voicemail-done', { From: '+19725551234', RecordingSid: 'RE' + 'a'.repeat(32), RecordingDuration: '30' });
    assert.match(r.body, /on its way to a licensed local plumber/);

    // Recording links: a wrong signature is refused before anything is fetched.
    ({ mod } = load('recording'));
    r = await call(mod, `/api/recording?sid=RE${'a'.repeat(32)}&sig=bad`, {}, { signed: false });
    assert.strictEqual(r.code, 404);

    // Call log needs the admin key.
    ({ mod } = load('calls'));
    r = await call(mod, '/api/calls?key=wrong', {}, { signed: false });
    assert.strictEqual(r.code, 404);

    console.log('All phone system checks passed.');
})().catch(err => { console.error(err); process.exit(1); });
