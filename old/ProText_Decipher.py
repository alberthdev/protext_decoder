#!/usr/bin/env python3
# Albert Huang
# ENEE459E HW 1
# Problem 1
# Vigenere Cipher Cracking Tool
# 
# Resulting output:
# ------------------
# $ python3 HW1.py 
# 1.0
# Threshold met for key length 9: found 0.069, reference 0.065, diff 0.004, threshold 0.010
# Found key: SECRETKEY
# GMAILPHISHINGLATESTCYBERATTACKINFECTSUSERSBYMIMICKINGPASTEMAILSTHEINCREDIBLYCLEVERTECHNIQUEINVOLVESAFAKEBUTCONVINCINGANDFUNCTIONALGMAILSIGNINPAGEASOPHISTICATEDNEWPHISHINGTECHNIQUETHATCOMPOSESCONVINCINGEMAILSBYANALYSINGANDMIMICKINGPASTMESSAGESANDATTACHMENTSHASBEENDISCOVEREDBYSECURITYEXPERTSDISCOVEREDBYMARKMAUNDERTHECEOOFWORDPRESSSECURITYPLUGINWORDFENCETHEATTACKFIRSTSEESTHEHACKERSENDANEMAILAPPEARINGTOCONTAINAPDFWITHAFAMILIARFILENAMETHATPDFHOWEVERISACTUALLYACLEVERLYDISGUISEDIMAGETHATWHENCLICKEDLAUNCHESANEWTABTHATLOOKSLIKETHISITSTHEGMAILSIGNINPAGERIGHTNOTQUITEACLOSERLOOKATTHEADDRESSBARWILLSHOWYOUTHATALLISNOTQUITEASITSEEMSUNFORTUNATELYTHEATTACKSIMITATIONOFTHEGMAILSIGNINPAGEISSOCONVINCINGTHATMANYUSERSWILLAUTOMATICALLYENTERTHEIRLOGINDETAILSSIMULTANEOUSLYSURRENDERINGTHEMTOTHEHACKERSWHOCANPROCEEDTOSTEALYOURDATAANDUSEONEOFYOURPASTMESSAGESTOCOMPROMISEANOTHERROUNDOFGMAILUSERSINANEXAMPLEDESCRIBEDBYACOMMENTERONHACKERNEWSTHEHACKERSEMAILEDALINKDISGUISEDASANATHLETICSPRACTICESCHEDULEFROMONEMEMBEROFTHETEAMTOTHEOTHERSTHEATTACKERSLOGINTOYOURACCOUNTIMMEDIATELYONCETHEYGETTHECREDENTIALSANDTHEYUSEONEOFYOURACTUALATTACHMENTSALONGWITHONEOFYOURACTUALSUBJECTLINESANDSENDITTOPEOPLEINYOURCONTACTLISTADDEDTHECOMMENTERIMPRESSIVEASTHEATTACKISTHEREAREWAYSTOPROTECTYOURSELFTHEMOSTOBVIOUSGIVEAWAYISTHATTHELEGITIMATEGMAILSIGNINPAGESURLBEGINSWITHALOCKSYMBOLANDHTTPSHIGHLIGHTEDINGREENNOTDATATEXTHTMLHTTPSHOWEVERIFYOUHITTHEADDRESSBARYOULLALSOSEETHATTHEFAKEPAGESURLISACTUALLYINCREDIBLYLONGWITHAWHITESPACESNEAKILYHIDINGTHEMAJORITYOFTHETEXTFROMVIEWMAUNDERALSORECOMMENDSENABLINGTWOFACTORAUTHORISATIONONGMAILWHICHYOUCANDOHERE
# 

import sys
from char_frequency import freq_table_probs
import string

PLAINTEXT_AVAIL = string.ascii_uppercase + string.ascii_lowercase + string.ascii_uppercase + string.digits

CIPHERTEXT = "FELMuOPSbrowTfoxZumDCovLraELVdzIdog1KG"

# Frequency value
english_plaintext_sqsum = 0.065
sqsum_threshold = 0.01

# p = english_plaintext_probs
english_plaintext_probs = dict(freq_table_probs)

def find_key_length(ciphertext):
    # q = (total) occurence_dict
    est_sqsum = 0
    for letter in PLAINTEXT_AVAIL:
        est_sqsum += ciphertext.upper().count(letter) / len(ciphertext)
    
    print(est_sqsum)
    
    for key_len in range(1, len(ciphertext) + 1):
        cipher_part = "".join([ciphertext[char_index] for char_index in range(0, len(ciphertext), key_len)])
        
        occurence_dict = {}
        for letter in PLAINTEXT_AVAIL:
            occurence_dict[letter] = cipher_part.upper().count(letter)
        
        # q = occurence_dict / len(cipher)
        q_dict = {}
        for letter in PLAINTEXT_AVAIL:
            q_dict[letter] = occurence_dict[letter] / len(cipher_part)
        
        lang_fingerprint_sqsum = 0
        for letter in PLAINTEXT_AVAIL:
            lang_fingerprint_sqsum += q_dict[letter] * q_dict[letter]
        
        if abs(lang_fingerprint_sqsum - english_plaintext_sqsum) < sqsum_threshold:
            print("Threshold met for key length %d: found %.3f, reference %.3f, diff %.3f, threshold %.3f" % (
                key_len,
                lang_fingerprint_sqsum, english_plaintext_sqsum,
                abs(lang_fingerprint_sqsum - english_plaintext_sqsum),
                sqsum_threshold))
            return key_len
    return -1

def find_key(ciphertext, key_length):
    decoded_key = ""
    for kl in range(0, key_length):
        cipher_part = "".join([ciphertext[char_index] for char_index in range(kl, len(ciphertext), key_length)])
        
        # Compute letter probabilities
        cipher_letter_probs = {}
        for letter_i in PLAINTEXT_AVAIL:
            cipher_letter_probs[letter_i] = cipher_part.upper().count(letter_i) / len(cipher_part)
        
        shift_sqsums = []
        
        for letter_j in PLAINTEXT_AVAIL:
            shift_sqsums.append(
                sum(
                    [
                        (
                            english_plaintext_probs[letter_i] * 
                            cipher_letter_probs[
                                PLAINTEXT_AVAIL[(PLAINTEXT_AVAIL.index(letter_i) + PLAINTEXT_AVAIL.index(letter_j)) % 26]
                            ]
                        ) for letter_i in PLAINTEXT_AVAIL
                    ]
                )
            )
        
        english_plaintext_sqsum_arr = [english_plaintext_sqsum] * len(shift_sqsums)
        diff_sqsum = [abs(i - j) for i, j in zip(shift_sqsums, english_plaintext_sqsum_arr)]
        lowest_diff_sqsum = min(diff_sqsum)
        lowest_diff_sqsum_idx = diff_sqsum.index(lowest_diff_sqsum)
        key_letter = PLAINTEXT_AVAIL[lowest_diff_sqsum_idx]
        
        decoded_key += key_letter
    return decoded_key

def decrypt_vigenere(ciphertext, key):
    key_idx = 0
    plaintext = ""
    for cipher_char in ciphertext:
        cipher_char_idx = PLAINTEXT_AVAIL.index(cipher_char.upper())
        shift = key[key_idx]
        shift_char_idx = PLAINTEXT_AVAIL.index(shift.upper())
        final_char_idx = (cipher_char_idx - shift_char_idx) % 26
        plaintext += PLAINTEXT_AVAIL[final_char_idx]
        
        if key_idx < len(key) - 1:
            key_idx += 1
        else:
            key_idx = 0
    return plaintext

key_length = find_key_length(CIPHERTEXT)

if key_length == -1:
    print("Could not determine key length!")
    sys.exit(1)

key_decrypt = find_key(CIPHERTEXT, key_length)

print("Found key: %s" % key_decrypt)
plaintext = decrypt_vigenere(CIPHERTEXT, key_decrypt)
print(plaintext)
