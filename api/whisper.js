// Played only to the plumber before the caller is connected. Pressing 1 connects; anything else sends the
// caller to the message line. This proves a real person accepted, and that the lead came from this site.
const { cfg, VOICE, abs, fromTwilio, sendTwiml, forbid, twiml } = require('./_lib');

module.exports = (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const vr = new twiml.VoiceResponse();
    const gather = vr.gather({ numDigits: 1, timeout: 6, action: abs(req, '/api/whisper-check') });
    gather.say(VOICE, `New call from ${cfg.siteName} dot com. Press 1 to accept.`);
    vr.hangup();
    sendTwiml(res, vr);
};
