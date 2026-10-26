// Twilio posts the written transcript of a voicemail here a minute or so after the call. Text it on.
const { cfg, fromTwilio, forbid, alert, prettyPhone } = require('./_lib');

module.exports = async (req, res) => {
    if (!fromTwilio(req)) return forbid(res);
    const body = req.body || {};
    if (body.TranscriptionStatus === 'completed' && body.TranscriptionText) {
        await alert(`${cfg.siteName} message from ${prettyPhone(body.From)}: "${body.TranscriptionText}"`);
    }
    res.status(200).send('ok');
};
