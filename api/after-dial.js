// Runs after the forward attempt (or straight away when FORWARD_TO isn't set).
// Connected calls end here with a summary text; missed calls go to a short message line.
const { cfg, VOICE, abs, fromTwilio, sendTwiml, forbid, alert, prettyPhone, twiml } = require('./_lib');

function wasConnected(body) {
    if (body.DialBridged === 'true') return true;
    // Recording starts only once the plumber accepts, so a recording means the call was bridged.
    return body.DialCallStatus === 'completed' && Boolean(body.RecordingUrl);
}

module.exports = async (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const body = req.body || {};
    const vr = new twiml.VoiceResponse();

    if (!req.query.nobody && wasConnected(body)) {
        const mins = Math.round((Number(body.DialCallDuration) || 0) / 60 * 10) / 10;
        await alert(`${cfg.siteName}: call from ${prettyPhone(body.From)} was answered (${mins} min).`);
        vr.hangup();
        return sendTwiml(res, vr);
    }

    vr.say(VOICE, 'Sorry we missed you. After the beep, please leave your name, your address, and what is happening '
        + 'with your sewer line. A licensed local plumber will call you back.');
    vr.record({
        maxLength: 120,
        playBeep: true,
        timeout: 5,
        transcribe: true,
        transcribeCallback: abs(req, '/api/transcription'),
        action: abs(req, '/api/voicemail-done'),
    });
    vr.say(VOICE, 'We did not get a message. Please call again any time. Goodbye.');
    sendTwiml(res, vr);
};
