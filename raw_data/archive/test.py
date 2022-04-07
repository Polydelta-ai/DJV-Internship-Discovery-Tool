import spacy

from collections import Counter
from string import punctuation

nlp = spacy.load("en_core_web_lg")

def get_hotwords(text):
    result = []
    pos_tag = ['VERB','NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5

output = get_hotwords("""
    Intern will primarily work under Parks Naturalist assisting with her duties. During summer months, most attention is focused on the large seabird colony and nesting shorebirds. Huguenot Memorial Park is the only drive-on beach within Jacksonville city limits; the land is a peninsula with the tip closed off to driving seasonally for nesting birds. Intern will also assist with monitoring sea turtle nesting and educating visitors in the nature center. The nature center is open daily Memorial Day - Labor Day and on weekends during the off-season, where more attention is focused on creating new displays and going over collected data from nesting season.

Applicants should have a strong interest in birds and marine life and good communication skills for interacting with park visitors. Interns should expect to gain experience in conducting biological surveys; protecting wildlife through informative interpretation to the public; identifying and removing invasive species; monitoring sea turtle nesting success; and maintaining public lands. If the intern is interested in creating new displays for the nature center, they may also gain some experience in bone processing and introductory taxidermy working under a Scientific Collections permit.


All allowances subject to applicable federal, state, and local taxes.
""")

print(output)