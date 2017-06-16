ProText Decoder
===============
This is a GitHub repo for the HackerRank challenge submitted to
Hackathon Hackers.

Requirements
------------
This script requires Python 3.x to run. It also needs BeautifulSoup4
and the fonttools library to download and process the fonts,
respectively.

To run this:

 * Clone this repo.
 * Go to http://protext.herokuapp.com/ and view source.
 * Copy the source into an HTML file within the repo.
 * Run `decode.py`. Enter the HTML file name when prompted.

Approach
--------
At the very start, I looked at the rendered page, and then the source
of the page. I noticed that custom fonts were being used to render this
page. I then realized that the custom fonts had some sort of mapping
from the unicode custom character to render a valid, alphanumeric
character.

Knowing that I would need to analyze a font, I looked for a suitable
font library to download and use. I quickly found a font library for my
language of choice: fonttools, a font manipulation library for Python.
It had a really nice feature for decoding a TTF to a so-called TTX file,
which is an XML representation of the TTF's contents.

From the original encrypted text, I noticed that there wasn't a direct
mapping of English characters to encrypted text, and suspected that
there were multiple characters that mapped to the same rendered letter.

Parsing through the TTX file with BeautifulSoup, I then attempted to
find same shapes throughout the TTFs, for both file A and file B.
Duplicates were indeed found, and I created a dictionary to keep track
of all of this.

At first, I thought that there was some sort of cipher encryption on the
entire text, where the characters were shifted by a certain amount.
After some experimentation, I realized that the fonts also have the
regular characters defined, and that I simply needed to match up the
encrypted text shapes with the regular text shapes to get the decoded
text.

Therefore, I replaced all of the encrypted text with their regular
English counterparts, and I was able to successfully decode the message.
