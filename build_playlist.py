
import re
import urllib.request
from pathlib import Path

# Europe, Arabic countries, USA and Kenya.
COUNTRIES = {
    "USA": "us",
    "Norway": "no",
    "Sweden": "se",
    "Denmark": "dk",
    "Finland": "fi",
    "Iceland": "is",
    "United Kingdom": "uk",
    "Ireland": "ie",
    "Germany": "de",
    "France": "fr",
    "Italy": "it",
    "Spain": "es",
    "Portugal": "pt",
    "Netherlands": "nl",
    "Belgium": "be",
    "Luxembourg": "lu",
    "Switzerland": "ch",
    "Austria": "at",
    "Poland": "pl",
    "Czechia": "cz",
    "Slovakia": "sk",
    "Hungary": "hu",
    "Romania": "ro",
    "Bulgaria": "bg",
    "Greece": "gr",
    "Cyprus": "cy",
    "Malta": "mt",
    "Croatia": "hr",
    "Slovenia": "si",
    "Serbia": "rs",
    "Bosnia and Herzegovina": "ba",
    "Montenegro": "me",
    "North Macedonia": "mk",
    "Albania": "al",
    "Kosovo": "xk",
    "Estonia": "ee",
    "Latvia": "lv",
    "Lithuania": "lt",
    "Ukraine": "ua",
    "Moldova": "md",
    "Belarus": "by",
    "Russia": "ru",
    "Turkey": "tr",
    "Georgia": "ge",
    "Armenia": "am",
    "Azerbaijan": "az",
    "Andorra": "ad",
    "Monaco": "mc",
    "San Marino": "sm",
    "Liechtenstein": "li",
    "Vatican City": "va",
    "Saudi Arabia": "sa",
    "United Arab Emirates": "ae",
    "Qatar": "qa",
    "Kuwait": "kw",
    "Bahrain": "bh",
    "Oman": "om",
    "Yemen": "ye",
    "Iraq": "iq",
    "Jordan": "jo",
    "Lebanon": "lb",
    "Syria": "sy",
    "Palestine": "ps",
    "Egypt": "eg",
    "Libya": "ly",
    "Tunisia": "tn",
    "Algeria": "dz",
    "Morocco": "ma",
    "Sudan": "sd",
    "Somalia": "so",
    "Djibouti": "dj",
    "Mauritania": "mr",
    "Comoros": "km",
    "Kenya": "ke",
}

BASE = "https://iptv-org.github.io/iptv/countries"
output = ["#EXTM3U"]
total = 0

for country, code in COUNTRIES.items():
    url = f"{BASE}/{code}.m3u"
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read().decode("utf-8-sig")

        lines = data.splitlines()
        count = 0
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF:"):
                entry = [line]
                j = i + 1
                while j < len(lines) and not lines[j].startswith("#EXTINF:"):
                    if lines[j].strip() and lines[j].strip() != "#EXTM3U":
                        entry.append(lines[j].strip())
                    j += 1

                if any(x.startswith(("http://", "https://")) for x in entry[1:]):
                    group = country.replace('"', "")
                    meta = re.sub(
                        r'\s+group-title="[^"]*"',
                        "",
                        entry[0]
                    )
                    meta = meta.replace(
                        "#EXTINF:",
                        f'#EXTINF:',
                        1
                    )
                    comma = meta.find(",")
                    if comma >= 0:
                        meta = (
                            meta[:comma]
                            + f' group-title="{group}"'
                            + meta[comma:]
                        )
                    output.append(meta)
                    output.extend(entry[1:])
                    count += 1
                i = j
            else:
                i += 1

        total += count
        print(f"{country}: {count} channels")

    except Exception as error:
        print(f"{country}: skipped ({error})")

if total == 0:
    raise RuntimeError("No channels downloaded; playlist not replaced")

Path("channels.m3u").write_text(
    "\n".join(output) + "\n",
    encoding="utf-8"
)
print(f"Finished: {total} channels")
