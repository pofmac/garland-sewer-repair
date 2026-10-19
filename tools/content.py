"""All the words on GarlandSewerRepair.com. Edit here, then run:  python3 tools/build_site.py

Rules for this file:
- Plain language for a homeowner with a sewer problem, not plumbing jargon.
- Only claims we can stand behind. Prices are typical ranges, never quotes.
- The site is a referral service: it connects callers with a licensed local plumber. Never say "we" do the digging.
"""

# Set this to the tracking number (CallRail / CallScaler) before the site goes live, e.g. "(469) 555-0123".
# While it is empty, call buttons are replaced by a "phone line opening soon" note.
PHONE = ""

BRAND = "Garland Sewer Repair"
CITY = "Garland"
STATE = "TX"
ZIPS = ["75040", "75041", "75042", "75043", "75044", "75048"]

HOME = {
    "title": "Sewer Repair in Garland, TX",
    "lede": "Sewage backing up, a soggy yard or a sewer smell? Get connected with a licensed local plumber for "
            "sewer line repair, replacement and trenchless options in Garland.",
    "signs": [
        ("Drains backing up in more than one place", "When the tub gurgles as the toilet flushes, or a floor drain "
         "overflows, the blockage is usually in the main sewer line, not a single drain."),
        ("Soggy, green or sunken patches in the yard", "A broken line leaks wastewater into the soil. Grass over the "
         "line grows greener, or the ground sinks along the pipe's path."),
        ("Sewer smell indoors or outside", "A steady sewage odor can mean a crack or a gap in the pipe, or a dry trap "
         "letting sewer gas in."),
        ("Clogs that keep coming back", "If a main-line clog returns weeks after it was cleared, tree roots or a sagging "
         "section of pipe are often the cause."),
    ],
    "why": [
        ("Garland's clay soil", "Much of the Dallas area sits on expansive clay that swells when wet and shrinks in "
         "drought. That movement bends and cracks buried pipes, and it is worst after a long, hot, dry summer."),
        ("Older pipes", "Many Garland homes were built from the 1950s through the 1980s. Depending on the year, the sewer "
         "line may be cast iron, clay tile or even Orangeburg (tar paper pipe), all of which wear out with age."),
        ("Tree roots", "Roots grow toward the moisture in sewer lines and push in through small joints and cracks, then "
         "grow until they block the pipe."),
    ],
}

SERVICES = [
    {
        "slug": "sewer-line-replacement",
        "title": "Sewer Line Replacement",
        "nav": "Replacement",
        "short": "When a sewer line is collapsed, badly cracked or full of roots, replacing it ends the repeat clogs.",
        "what": "Replacement means taking out the old pipe from the house to the city connection and putting in new "
                "PVC pipe, which does not rust and resists roots far better than cast iron or clay. It can be done by "
                "digging a trench, or with trenchless methods if the yard, driveway or trees are in the way.",
        "when": [
            "A camera inspection shows a collapsed, crushed or badly offset pipe",
            "Cast iron that is scaling, rusted through or flattened",
            "Orangeburg or clay pipe with many root intrusions",
            "Repeated backups even after the line has been cleaned",
        ],
        "cost": "Full replacement commonly runs from about $3,000 to $25,000. Length of the line, depth, what is above "
                "it (driveway, patio, mature trees) and the method all change the price.",
        "faq": [
            ("How long does sewer line replacement take?", "Most home sewer lines are replaced in one to three days. "
             "Trenchless jobs are often finished in a single day."),
            ("Do I need a permit in Garland?", "Sewer line work generally needs a permit and an inspection, and in Texas "
             "the work must be done by a plumber licensed by the Texas State Board of Plumbing Examiners. Your plumber "
             "normally pulls the permit."),
            ("Who is responsible for the sewer line?", "In most cities, including Garland, the homeowner is responsible "
             "for the private line from the house to the city's connection, and the city maintains the public main. "
             "Ask your plumber or the City of Garland if you are unsure where your part ends."),
        ],
    },
    {
        "slug": "trenchless-sewer-repair",
        "title": "Trenchless Sewer Repair",
        "nav": "Trenchless",
        "short": "Fix or replace a sewer line with one or two small access holes instead of a trench across the yard.",
        "what": "There are two main trenchless methods. Pipe lining slides a resin-soaked liner into the old pipe and "
                "hardens it in place, forming a new pipe inside the old one. Pipe bursting pulls a new pipe through the "
                "old one, breaking the old pipe apart as it goes. Both leave lawns, driveways and trees mostly untouched.",
        "when": [
            "The line runs under a driveway, patio, slab or mature trees",
            "Cracks, root intrusion or leaking joints along much of the pipe",
            "You want the job done quickly with little cleanup",
        ],
        "not": "Trenchless is not always possible. A fully collapsed pipe, a badly sagging line (a 'belly') or very sharp "
               "bends may still need digging. A camera inspection tells you which option fits.",
        "cost": "Trenchless work often costs from about $6,000 to $30,000. It can cost more per foot than digging, but "
                "you avoid the expense of replacing landscaping, concrete or flooring.",
        "faq": [
            ("Is trenchless as good as digging?", "When the pipe is a good fit for it, yes. Lined and burst pipes are "
             "commonly expected to last for decades. Ask the plumber about the warranty on the liner or pipe."),
            ("Will trenchless work under my house slab?", "Often, yes. Lining can repair pipes under a slab without "
             "breaking up the floor, which is one of its biggest advantages."),
        ],
    },
    {
        "slug": "sewer-camera-inspection",
        "title": "Sewer Camera Inspection",
        "nav": "Camera Inspection",
        "short": "A small waterproof camera goes down the line so you can see the problem before paying to fix it.",
        "what": "The plumber feeds a camera on a flexible cable through a cleanout or drain. You see the inside of the "
                "pipe on a screen: roots, cracks, sags, grease or a collapse, and how far along the line each problem is. "
                "Many plumbers also locate the problem spot from above so any digging is in exactly the right place.",
        "when": [
            "Before buying an older home (a 'sewer scope' is a common add-on to a home inspection)",
            "After a backup, to find out why it happened",
            "Before agreeing to an expensive replacement, for a second opinion",
            "Clogs keep coming back",
        ],
        "cost": "A camera inspection usually costs about $250 to $900, and is sometimes included if you go ahead with "
                "the repair.",
        "faq": [
            ("Can I get a copy of the video?", "Ask for it. Many plumbers will send the video or screenshots, which is "
             "useful for a second opinion or for a home sale."),
            ("Should I get a sewer scope before buying a house?", "For homes built before about 1980, it is widely "
             "recommended. Repairing a failed line can cost thousands, and a standard home inspection does not look "
             "inside the sewer line."),
        ],
    },
    {
        "slug": "hydro-jetting",
        "title": "Hydro Jetting & Main Line Clogs",
        "nav": "Hydro Jetting",
        "short": "High-pressure water scours grease, sludge and roots out of the main sewer line.",
        "what": "Hydro jetting sends water at very high pressure through a special nozzle that cleans the full width of "
                "the pipe, not just a hole through the clog like a cable snake. It is the usual fix for grease buildup "
                "and for clearing roots before a repair or lining.",
        "when": [
            "Slow drains throughout the house",
            "Grease buildup in kitchen and main lines",
            "Roots that keep coming back after snaking",
            "Cleaning the line before a camera inspection or lining",
        ],
        "not": "Jetting is not safe for every pipe. Very old, cracked or collapsed pipes can be damaged further, so a good "
               "plumber inspects with a camera first.",
        "cost": "Hydro jetting a main line typically costs about $350 to $1,000.",
        "faq": [
            ("Is hydro jetting better than snaking?", "For grease and roots, usually yes, because it cleans the whole pipe "
             "wall. Snaking is cheaper and fine for a simple blockage."),
        ],
    },
    {
        "slug": "emergency-sewer-backup",
        "title": "Emergency Sewer Backup",
        "nav": "Sewer Backup",
        "short": "Sewage coming up through floor drains, tubs or toilets needs fast attention.",
        "what": "A backup means wastewater can't get out to the city sewer. The cause is usually a blocked or broken main "
                "line on your property, but sometimes it's the city main. A plumber can clear the line and find the "
                "cause so it doesn't happen again.",
        "steps": [
            "Stop using water: no flushing, showers, laundry or dishwasher",
            "Keep children and pets away from the water; sewage carries germs",
            "If water is near outlets or appliances, stay out and switch off power only if you can do so safely",
            "Call a plumber to clear the line",
            "If neighbors are backing up too, call the City of Garland, since the public main may be blocked",
            "Take photos for your insurance company",
        ],
        "cost": "Clearing a main-line clog often costs a few hundred dollars. If a camera shows broken pipe, repair or "
                "replacement is priced separately.",
        "faq": [
            ("Does homeowners insurance cover a sewer backup?", "Many standard policies don't cover sewer backup unless "
             "you added a 'water backup' endorsement. Check your policy or call your agent."),
            ("Can I clean up sewage myself?", "Small, clean-water spills are one thing. Sewage carries bacteria; for "
             "anything more than a little, consider a professional water damage and cleanup company."),
        ],
    },
]

COST_GUIDE = {
    "slug": "sewer-repair-cost",
    "title": "Sewer Repair Cost in Garland",
    "short": "Typical price ranges for common sewer jobs, and what makes the price go up or down.",
    "rows": [
        ("Main line clog cleared (snake)", "$150 - $500"),
        ("Hydro jetting", "$350 - $1,000"),
        ("Camera inspection", "$250 - $900"),
        ("Spot repair of one section", "$1,000 - $4,000"),
        ("Full sewer line replacement (dig)", "$3,000 - $25,000"),
        ("Trenchless lining or pipe bursting", "$6,000 - $30,000"),
    ],
    "factors": [
        ("Length and depth", "Longer, deeper lines cost more to dig and replace."),
        ("What's on top", "Driveways, patios, slabs and big trees add cost to digging, which is where trenchless can "
         "save money overall."),
        ("Pipe material and condition", "A collapsed line limits the options; a line that can be lined may cost less."),
        ("Permits and the city tie-in", "Permits, inspections and connecting at the city side add to the total."),
    ],
    "note": "These are typical ranges gathered from national cost guides and plumber price lists, not quotes. Always "
            "get a written estimate, and for big jobs, a second opinion with the camera video.",
}

AREAS = [
    {
        "slug": "rowlett",
        "name": "Rowlett",
        "text": "Rowlett sits just east of Garland on Lake Ray Hubbard. It has a mix of older neighborhoods near the "
                "original town and newer subdivisions to the north and east. Older homes face the same clay-soil and "
                "root problems as Garland, and lakeside lots can have high moisture that speeds up root growth.",
    },
    {
        "slug": "sachse",
        "name": "Sachse",
        "text": "Sachse, north of Garland, grew mostly from the 1980s on, so many homes have PVC sewer lines. Even plastic "
                "pipe can shift and separate at the joints in expansive clay, and roots still find their way into older "
                "connections.",
    },
]

HOW_IT_WORKS = [
    ("You call", "Call the number on this page any time. Calls are answered by our team or a virtual assistant."),
    ("We connect you", "We pass your details to a licensed, insured local plumber who handles sewer work in Garland."),
    ("The plumber calls you back", "They confirm the problem, schedule a visit and give you a written estimate. You "
     "decide whether to go ahead."),
]
