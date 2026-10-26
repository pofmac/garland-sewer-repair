// The plumber's key press from the whisper. "1" connects the caller (an empty response ends the whisper and
// bridges the call); anything else hangs up the plumber's leg so the caller can leave a message instead.
const { fromTwilio, sendTwiml, forbid, twiml } = require('./_lib');

module.exports = (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const vr = new twiml.VoiceResponse();
    if ((req.body || {}).Digits !== '1') vr.hangup();
    sendTwiml(res, vr);
};
