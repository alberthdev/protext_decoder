#!/usr/bin/env python3
import html
import string
from bs4 import BeautifulSoup
from ttxconv import ttxconv
from page_decoder import decode_page, dl_fonts, bn_fonts

PRINT_DEBUG_INFO = False

glyph_table = {}
char_to_glyph_table = {}
glyph_to_char_table = {}

def import_font(font_file_name):
    if not font_file_name.lower().endswith(".ttx"):
        font_file_name = ttxconv(font_file_name)
    
    # Read font XML
    fh = open(font_file_name, "r")
    xml = fh.read()
    fh.close()

    # Parse it
    soup = BeautifulSoup(xml, "lxml-xml")

    # Find all TTGlyph components
    res = soup.find_all("TTGlyph")
    
    # Find all map components
    charmaps = soup.find_all("map")

    # Create a table of glyphs
    for font_glyph in res:
        #print(font_glyph['name'])
        contents_strify_arr = [ str(x) if type(x) != str else x for x in font_glyph.contents ]
        contents_strify = "".join(contents_strify_arr).strip().replace("\n", "")
        #print(contents_strify)
        
        glyph_name = font_file_name + "_" + font_glyph['name']
        
        if contents_strify not in glyph_table:
            glyph_table[contents_strify] = [glyph_name]
        else:
            glyph_table[contents_strify].append(glyph_name)
    
    # Create a table of characters to glyphs
    for charmap in charmaps:
        codepoint_num = int(charmap["code"], 16)
        char = chr(codepoint_num)
        glyph_name = font_file_name + "_" + charmap['name']
        
        if char not in char_to_glyph_table:
            char_to_glyph_table[char] = [glyph_name]
        else:
            if glyph_name not in char_to_glyph_table[char]:
                char_to_glyph_table[char].append(glyph_name)
    
    # Invert mapping of glyph
    for char in char_to_glyph_table:
        for glyph_name in char_to_glyph_table[char]:
            glyph_to_char_table[glyph_name] = char

# Input text
#html_text = "&#205;&#204;&#211;&#233;&#212;&#256;&#214;&#215;&#218;&#233;&#247;&#245;&#243;&#234;&#219;&#233;&#258;&#243;&#253;&#233;&#225;&#256;&#263;&#203;&#202;&#233;&#243;&#259;&#211;&#245;&#233;&#226;&#204;&#211;&#233;&#221;&#229;&#239;&#208;&#233;&#249;&#243;&#255;.&#233;&#236;&#233;+&#233;&#210;&#233;=&#233;&#206;."

# Fonts to scan
#font_files = [ "font_a_603a0053444b71ed07873c58ab758484.ttf", "font_b_603a0053444b71ed07873c58ab758484.ttf" ]

html_text, font_files_urls = decode_page(input("Enter HTML file to decode: "))
dl_fonts(font_files_urls)
font_files = bn_fonts(font_files_urls)

# Import fonts into database
for font_file in font_files:
    import_font(font_file)

# Finally, consolidate duplicate information
if PRINT_DEBUG_INFO:
    num_dup_glyphs = 0
    for glyph_sig in glyph_table:
        if len(glyph_table[glyph_sig]) > 1:
            print("Signature [%s] has duplicates: %s" % (glyph_sig, ", ".join(glyph_table[glyph_sig])))
            num_dup_glyphs += len(glyph_table[glyph_sig])

    print("Found %d duplicate glyphs!" % num_dup_glyphs)
    from pprint import pprint
    pprint(char_to_glyph_table)

# Convert html_text to actual text
text = html.unescape(html_text)

# Make a copy to work on
new_text = str(text)

# Replace all of the "fake" spaces with actual spaces
for space_glyph in glyph_table[""]:
    if space_glyph in glyph_to_char_table:
        new_text = new_text.replace(glyph_to_char_table[space_glyph], " ")
        
print(" ** Ciphertext with spaces:\n" + new_text)

# Now create alpha-numeric only text...
# How? We filter out the text for only those that actually show up.
new_text_filtered_alnum = str(new_text)
"""
i = 0

while i < len(new_text_filtered_alnum):
    char = new_text_filtered_alnum[i]
    if char not in char_to_glyph_table:
        new_text_filtered_alnum = new_text_filtered_alnum.replace(char, "")
    i += 1

print(new_text_filtered_alnum)
"""
new_text_without_dups = str(new_text_filtered_alnum)

# Now eliminate duplicates and create an "alphabet"
cipher_alphabet = ""
for glyph_sig in glyph_table:
    if len(glyph_table[glyph_sig]) > 1:
        dup_chars = ""
        for glyph_name in glyph_table[glyph_sig]:
            if glyph_name in glyph_to_char_table:
                dup_chars += glyph_to_char_table[glyph_name]
            else:
                if PRINT_DEBUG_INFO:
                    print("WARNING: %s not found in glyph_to_char_table, even though it is specified in the glyph definition table" % glyph_name)
        
        if len(dup_chars) < 1:
            continue
        
        if PRINT_DEBUG_INFO:
            print("Performing replacement on group: %s" % dup_chars)
        
        # Sort the duplicate chars to prefer the non-unicode one
        dup_chars = "".join(sorted(dup_chars))
        
        # Use the first char, replace the others
        for dup_char in dup_chars[1:]:
            new_text_without_dups = new_text_without_dups.replace(dup_char, dup_chars[0])
        
        # Append first char to "alphabet"
        if dup_chars[0] != " ":
            cipher_alphabet += dup_chars[0]
    else:
        glyph_name = glyph_table[glyph_sig]
        if glyph_to_char_table[glyph_name] != " ":
            cipher_alphabet += glyph_to_char_table[glyph_name]

cipher_alphabet = "".join(sorted(cipher_alphabet))

print(" ** Decoded text:\n" + new_text_without_dups)
print(" ** Decoded alphabet:\n" + cipher_alphabet)
print(" ** Length of alphabet: " + str(len(cipher_alphabet)))

