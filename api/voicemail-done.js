// After the caller leaves a message: text the alert numbers right away with the caller's number and a link
// to the recording. The written transcript follows in a second text from /api/transcription.
const { cfg, VOICE, fromTwilio, sendTwiml, forbid, alert, prettyPhone, recordingLink, twiml } = require('./_lib');

module.exports = async (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const body = req.body || {};
    const vr = new twiml.VoiceResponse();
    const secs = Number(body.RecordingDuration) || 0;
    if (body.RecordingSid && secs >= 2) {
        await alert(`${cfg.siteName} NEW LEAD: voicemail from ${prettyPhone(body.From)} (${secs}s). `
            + `Listen: ${recordingLink(req, body.RecordingSid)}  Call them back ASAP.`);
        vr.say(VOICE, 'Thank you. Your message is on its way to a licensed local plumber. Goodbye.');
    } else {
        await alert(`${cfg.siteName}: missed call from ${prettyPhone(body.From)}, no message left. Worth a call back.`);
        vr.say(VOICE, 'Goodbye.');
    }
    vr.hangup();
    sendTwiml(res, vr);
};
