# GarlandSewerRepair.com

Rank-and-rent lead site for sewer line repair in Garland, TX. Plain static HTML, hosted on Vercel.

- Edit words in `tools/content.py`, then run `python3 tools/build_site.py` to rebuild every page, `sitemap.xml` and `robots.txt`.
- Set `PHONE` in `tools/content.py` to the call-tracking number before launch. Until then, call buttons show "Phone line opening soon".
- The site is an honest referral service: it says so in the footer, About page and privacy page.

## Phone system (stage 1)

Vercel functions in `api/` answer calls to the Twilio tracking number:

1. Caller hears a short recording notice.
2. `FORWARD_TO` rings (the plumber, or your cell until a plumber signs on). They hear a private whisper:
   "New call from Garland Sewer Repair dot com. Press 1 to accept." Pressing 1 connects and records the call.
3. Missed or declined calls go to a message line. The voicemail, its transcript and a link to the recording are
   texted to `ALERT_SMS_TO`.
4. `/api/calls?key=ADMIN_KEY` shows the call log with recordings.

Setup: set the environment variables listed at the top of `api/_lib.js` in Vercel, then in the Twilio Console set
the number's "A call comes in" webhook to `https://www.garlandsewerrepair.com/api/voice` (HTTP POST).
Run `npm test` for the offline checks. Stage 2 replaces the message line with an AI voice assistant.
