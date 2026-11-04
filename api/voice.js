// Incoming call to the tracking number. Point the Twilio number's "A call comes in" webhook here (HTTP POST).
// Flow: recording notice → ring FORWARD_TO with a whisper ("press 1 to accept") → if nobody accepts, take a message.
const { cfg, VOICE, abs, fromTwilio, sendTwiml, forbid, twiml } = require('./_lib');

module.exports = (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const vr = new twiml.VoiceResponse();
    vr.say(VOICE, `Thanks for calling ${cfg.siteName}. This call may be recorded so we can get your request to the right plumber.`);
    if (cfg.forwardTo) {
        const dial = vr.dial({
            timeout: 20,
            answerOnBridge: true,
            record: 'record-from-answer-dual',
            action: abs(req, '/api/after-dial'),
        });
        dial.number({ url: abs(req, '/api/whisper') }, cfg.forwardTo);
    } else {
        vr.redirect(abs(req, '/api/after-dial?nobody=1'));
    }
    sendTwiml(res, vr);
};
