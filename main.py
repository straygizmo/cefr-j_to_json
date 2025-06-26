#!/usr/bin/env python3
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

IRREGULAR_VERBS = {
    'be': {
        'base': 'be',
        'past': ['was', 'were'],
        'past_participle': ['been'],
        'present_participle': ['being'],
        'third_person': ['is'],
        'other_forms': ['am', 'are']
    },
    'have': {
        'base': 'have',
        'past': ['had'],
        'past_participle': ['had'],
        'present_participle': ['having'],
        'third_person': ['has']
    },
    'do': {
        'base': 'do',
        'past': ['did'],
        'past_participle': ['done'],
        'present_participle': ['doing'],
        'third_person': ['does']
    },
    'go': {
        'base': 'go',
        'past': ['went'],
        'past_participle': ['gone'],
        'present_participle': ['going'],
        'third_person': ['goes']
    },
    'get': {
        'base': 'get',
        'past': ['got'],
        'past_participle': ['got', 'gotten'],
        'present_participle': ['getting'],
        'third_person': ['gets']
    },
    'make': {
        'base': 'make',
        'past': ['made'],
        'past_participle': ['made'],
        'present_participle': ['making'],
        'third_person': ['makes']
    },
    'take': {
        'base': 'take',
        'past': ['took'],
        'past_participle': ['taken'],
        'present_participle': ['taking'],
        'third_person': ['takes']
    },
    'come': {
        'base': 'come',
        'past': ['came'],
        'past_participle': ['come'],
        'present_participle': ['coming'],
        'third_person': ['comes']
    },
    'see': {
        'base': 'see',
        'past': ['saw'],
        'past_participle': ['seen'],
        'present_participle': ['seeing'],
        'third_person': ['sees']
    },
    'know': {
        'base': 'know',
        'past': ['knew'],
        'past_participle': ['known'],
        'present_participle': ['knowing'],
        'third_person': ['knows']
    },
    'think': {
        'base': 'think',
        'past': ['thought'],
        'past_participle': ['thought'],
        'present_participle': ['thinking'],
        'third_person': ['thinks']
    },
    'give': {
        'base': 'give',
        'past': ['gave'],
        'past_participle': ['given'],
        'present_participle': ['giving'],
        'third_person': ['gives']
    },
    'find': {
        'base': 'find',
        'past': ['found'],
        'past_participle': ['found'],
        'present_participle': ['finding'],
        'third_person': ['finds']
    },
    'tell': {
        'base': 'tell',
        'past': ['told'],
        'past_participle': ['told'],
        'present_participle': ['telling'],
        'third_person': ['tells']
    },
    'become': {
        'base': 'become',
        'past': ['became'],
        'past_participle': ['become'],
        'present_participle': ['becoming'],
        'third_person': ['becomes']
    },
    'leave': {
        'base': 'leave',
        'past': ['left'],
        'past_participle': ['left'],
        'present_participle': ['leaving'],
        'third_person': ['leaves']
    },
    'feel': {
        'base': 'feel',
        'past': ['felt'],
        'past_participle': ['felt'],
        'present_participle': ['feeling'],
        'third_person': ['feels']
    },
    'bring': {
        'base': 'bring',
        'past': ['brought'],
        'past_participle': ['brought'],
        'present_participle': ['bringing'],
        'third_person': ['brings']
    },
    'begin': {
        'base': 'begin',
        'past': ['began'],
        'past_participle': ['begun'],
        'present_participle': ['beginning'],
        'third_person': ['begins']
    },
    'keep': {
        'base': 'keep',
        'past': ['kept'],
        'past_participle': ['kept'],
        'present_participle': ['keeping'],
        'third_person': ['keeps']
    },
    'hold': {
        'base': 'hold',
        'past': ['held'],
        'past_participle': ['held'],
        'present_participle': ['holding'],
        'third_person': ['holds']
    },
    'write': {
        'base': 'write',
        'past': ['wrote'],
        'past_participle': ['written'],
        'present_participle': ['writing'],
        'third_person': ['writes']
    },
    'stand': {
        'base': 'stand',
        'past': ['stood'],
        'past_participle': ['stood'],
        'present_participle': ['standing'],
        'third_person': ['stands']
    },
    'hear': {
        'base': 'hear',
        'past': ['heard'],
        'past_participle': ['heard'],
        'present_participle': ['hearing'],
        'third_person': ['hears']
    },
    'let': {
        'base': 'let',
        'past': ['let'],
        'past_participle': ['let'],
        'present_participle': ['letting'],
        'third_person': ['lets']
    },
    'mean': {
        'base': 'mean',
        'past': ['meant'],
        'past_participle': ['meant'],
        'present_participle': ['meaning'],
        'third_person': ['means']
    },
    'set': {
        'base': 'set',
        'past': ['set'],
        'past_participle': ['set'],
        'present_participle': ['setting'],
        'third_person': ['sets']
    },
    'meet': {
        'base': 'meet',
        'past': ['met'],
        'past_participle': ['met'],
        'present_participle': ['meeting'],
        'third_person': ['meets']
    },
    'run': {
        'base': 'run',
        'past': ['ran'],
        'past_participle': ['run'],
        'present_participle': ['running'],
        'third_person': ['runs']
    },
    'pay': {
        'base': 'pay',
        'past': ['paid'],
        'past_participle': ['paid'],
        'present_participle': ['paying'],
        'third_person': ['pays']
    },
    'sit': {
        'base': 'sit',
        'past': ['sat'],
        'past_participle': ['sat'],
        'present_participle': ['sitting'],
        'third_person': ['sits']
    },
    'speak': {
        'base': 'speak',
        'past': ['spoke'],
        'past_participle': ['spoken'],
        'present_participle': ['speaking'],
        'third_person': ['speaks']
    },
    'lie': {
        'base': 'lie',
        'past': ['lay', 'lied'],
        'past_participle': ['lain', 'lied'],
        'present_participle': ['lying'],
        'third_person': ['lies']
    },
    'lead': {
        'base': 'lead',
        'past': ['led'],
        'past_participle': ['led'],
        'present_participle': ['leading'],
        'third_person': ['leads']
    },
    'read': {
        'base': 'read',
        'past': ['read'],
        'past_participle': ['read'],
        'present_participle': ['reading'],
        'third_person': ['reads']
    },
    'grow': {
        'base': 'grow',
        'past': ['grew'],
        'past_participle': ['grown'],
        'present_participle': ['growing'],
        'third_person': ['grows']
    },
    'lose': {
        'base': 'lose',
        'past': ['lost'],
        'past_participle': ['lost'],
        'present_participle': ['losing'],
        'third_person': ['loses']
    },
    'fall': {
        'base': 'fall',
        'past': ['fell'],
        'past_participle': ['fallen'],
        'present_participle': ['falling'],
        'third_person': ['falls']
    },
    'send': {
        'base': 'send',
        'past': ['sent'],
        'past_participle': ['sent'],
        'present_participle': ['sending'],
        'third_person': ['sends']
    },
    'build': {
        'base': 'build',
        'past': ['built'],
        'past_participle': ['built'],
        'present_participle': ['building'],
        'third_person': ['builds']
    },
    'understand': {
        'base': 'understand',
        'past': ['understood'],
        'past_participle': ['understood'],
        'present_participle': ['understanding'],
        'third_person': ['understands']
    },
    'draw': {
        'base': 'draw',
        'past': ['drew'],
        'past_participle': ['drawn'],
        'present_participle': ['drawing'],
        'third_person': ['draws']
    },
    'break': {
        'base': 'break',
        'past': ['broke'],
        'past_participle': ['broken'],
        'present_participle': ['breaking'],
        'third_person': ['breaks']
    },
    'spend': {
        'base': 'spend',
        'past': ['spent'],
        'past_participle': ['spent'],
        'present_participle': ['spending'],
        'third_person': ['spends']
    },
    'cut': {
        'base': 'cut',
        'past': ['cut'],
        'past_participle': ['cut'],
        'present_participle': ['cutting'],
        'third_person': ['cuts']
    },
    'rise': {
        'base': 'rise',
        'past': ['rose'],
        'past_participle': ['risen'],
        'present_participle': ['rising'],
        'third_person': ['rises']
    },
    'drive': {
        'base': 'drive',
        'past': ['drove'],
        'past_participle': ['driven'],
        'present_participle': ['driving'],
        'third_person': ['drives']
    },
    'buy': {
        'base': 'buy',
        'past': ['bought'],
        'past_participle': ['bought'],
        'present_participle': ['buying'],
        'third_person': ['buys']
    },
    'wear': {
        'base': 'wear',
        'past': ['wore'],
        'past_participle': ['worn'],
        'present_participle': ['wearing'],
        'third_person': ['wears']
    },
    'choose': {
        'base': 'choose',
        'past': ['chose'],
        'past_participle': ['chosen'],
        'present_participle': ['choosing'],
        'third_person': ['chooses']
    },
    'sing': {
        'base': 'sing',
        'past': ['sang'],
        'past_participle': ['sung'],
        'present_participle': ['singing'],
        'third_person': ['sings']
    },
    'teach': {
        'base': 'teach',
        'past': ['taught'],
        'past_participle': ['taught'],
        'present_participle': ['teaching'],
        'third_person': ['teaches']
    },
    'catch': {
        'base': 'catch',
        'past': ['caught'],
        'past_participle': ['caught'],
        'present_participle': ['catching'],
        'third_person': ['catches']
    },
    'throw': {
        'base': 'throw',
        'past': ['threw'],
        'past_participle': ['thrown'],
        'present_participle': ['throwing'],
        'third_person': ['throws']
    },
    'forget': {
        'base': 'forget',
        'past': ['forgot'],
        'past_participle': ['forgotten'],
        'present_participle': ['forgetting'],
        'third_person': ['forgets']
    },
    'swim': {
        'base': 'swim',
        'past': ['swam'],
        'past_participle': ['swum'],
        'present_participle': ['swimming'],
        'third_person': ['swims']
    },
    'sell': {
        'base': 'sell',
        'past': ['sold'],
        'past_participle': ['sold'],
        'present_participle': ['selling'],
        'third_person': ['sells']
    },
    'drink': {
        'base': 'drink',
        'past': ['drank'],
        'past_participle': ['drunk'],
        'present_participle': ['drinking'],
        'third_person': ['drinks']
    },
    'sleep': {
        'base': 'sleep',
        'past': ['slept'],
        'past_participle': ['slept'],
        'present_participle': ['sleeping'],
        'third_person': ['sleeps']
    },
    'eat': {
        'base': 'eat',
        'past': ['ate'],
        'past_participle': ['eaten'],
        'present_participle': ['eating'],
        'third_person': ['eats']
    },
    'win': {
        'base': 'win',
        'past': ['won'],
        'past_participle': ['won'],
        'present_participle': ['winning'],
        'third_person': ['wins']
    },
    'fight': {
        'base': 'fight',
        'past': ['fought'],
        'past_participle': ['fought'],
        'present_participle': ['fighting'],
        'third_person': ['fights']
    },
    'fly': {
        'base': 'fly',
        'past': ['flew'],
        'past_participle': ['flown'],
        'present_participle': ['flying'],
        'third_person': ['flies']
    },
    'put': {
        'base': 'put',
        'past': ['put'],
        'past_participle': ['put'],
        'present_participle': ['putting'],
        'third_person': ['puts']
    },
    'cost': {
        'base': 'cost',
        'past': ['cost'],
        'past_participle': ['cost'],
        'present_participle': ['costing'],
        'third_person': ['costs']
    },
    'hit': {
        'base': 'hit',
        'past': ['hit'],
        'past_participle': ['hit'],
        'present_participle': ['hitting'],
        'third_person': ['hits']
    },
    'hurt': {
        'base': 'hurt',
        'past': ['hurt'],
        'past_participle': ['hurt'],
        'present_participle': ['hurting'],
        'third_person': ['hurts']
    },
    'shut': {
        'base': 'shut',
        'past': ['shut'],
        'past_participle': ['shut'],
        'present_participle': ['shutting'],
        'third_person': ['shuts']
    },
    'quit': {
        'base': 'quit',
        'past': ['quit'],
        'past_participle': ['quit'],
        'present_participle': ['quitting'],
        'third_person': ['quits']
    },
    'spread': {
        'base': 'spread',
        'past': ['spread'],
        'past_participle': ['spread'],
        'present_participle': ['spreading'],
        'third_person': ['spreads']
    },
    'deal': {
        'base': 'deal',
        'past': ['dealt'],
        'past_participle': ['dealt'],
        'present_participle': ['dealing'],
        'third_person': ['deals']
    },
    'steal': {
        'base': 'steal',
        'past': ['stole'],
        'past_participle': ['stolen'],
        'present_participle': ['stealing'],
        'third_person': ['steals']
    },
    'shoot': {
        'base': 'shoot',
        'past': ['shot'],
        'past_participle': ['shot'],
        'present_participle': ['shooting'],
        'third_person': ['shoots']
    },
    'hide': {
        'base': 'hide',
        'past': ['hid'],
        'past_participle': ['hidden'],
        'present_participle': ['hiding'],
        'third_person': ['hides']
    },
    'bite': {
        'base': 'bite',
        'past': ['bit'],
        'past_participle': ['bitten'],
        'present_participle': ['biting'],
        'third_person': ['bites']
    },
    'ring': {
        'base': 'ring',
        'past': ['rang'],
        'past_participle': ['rung'],
        'present_participle': ['ringing'],
        'third_person': ['rings']
    },
    'blow': {
        'base': 'blow',
        'past': ['blew'],
        'past_participle': ['blown'],
        'present_participle': ['blowing'],
        'third_person': ['blows']
    },
    'shake': {
        'base': 'shake',
        'past': ['shook'],
        'past_participle': ['shaken'],
        'present_participle': ['shaking'],
        'third_person': ['shakes']
    },
    'freeze': {
        'base': 'freeze',
        'past': ['froze'],
        'past_participle': ['frozen'],
        'present_participle': ['freezing'],
        'third_person': ['freezes']
    },
    'light': {
        'base': 'light',
        'past': ['lit', 'lighted'],
        'past_participle': ['lit', 'lighted'],
        'present_participle': ['lighting'],
        'third_person': ['lights']
    }
}

AMERICAN_BRITISH_VARIANTS = {
    'color': 'colour',
    'analyze': 'analyse',
    'realize': 'realise',
    'organize': 'organise',
    'recognize': 'recognise',
    'apologize': 'apologise',
    'emphasize': 'emphasise',
    'criticize': 'criticise',
    'memorize': 'memorise',
    'minimize': 'minimise',
    'maximize': 'maximise',
    'optimize': 'optimise',
    'utilize': 'utilise',
    'center': 'centre',
    'meter': 'metre',
    'theater': 'theatre',
    'fiber': 'fibre',
    'neighbor': 'neighbour',
    'favor': 'favour',
    'labor': 'labour',
    'honor': 'honour',
    'humor': 'humour',
    'behavior': 'behaviour',
    'flavor': 'flavour',
    'endeavor': 'endeavour',
    'defense': 'defence',
    'offense': 'offence',
    'license': 'licence',
    'practice': 'practise',
    'traveled': 'travelled',
    'traveling': 'travelling',
    'traveler': 'traveller',
    'canceled': 'cancelled',
    'canceling': 'cancelling',
    'modeled': 'modelled',
    'modeling': 'modelling',
    'fueled': 'fuelled',
    'fueling': 'fuelling',
    'labeled': 'labelled',
    'labeling': 'labelling'
}

def create_reverse_irregular_verb_mapping() -> Dict[str, str]:
    """Create a mapping from all verb forms to their base form."""
    mapping = {}
    for base_verb, forms in IRREGULAR_VERBS.items():
        mapping[base_verb] = base_verb
        for form_list in [forms.get('past', []), forms.get('past_participle', []), 
                         forms.get('present_participle', []), forms.get('third_person', []),
                         forms.get('other_forms', [])]:
            for form in form_list:
                mapping[form.lower()] = base_verb
    return mapping

def generate_regular_verb_forms(verb: str) -> Set[str]:
    """Generate regular verb forms (present, past, participle, -ing)."""
    forms = {verb}
    
    if verb.endswith('e'):
        forms.add(verb + 'd')
        forms.add(verb[:-1] + 'ing')
    elif verb.endswith('y') and len(verb) > 2 and verb[-2] not in 'aeiou':
        forms.add(verb[:-1] + 'ied')
        forms.add(verb[:-1] + 'ies')
        forms.add(verb + 'ing')
    elif verb.endswith(('s', 'x', 'z', 'ch', 'sh')):
        forms.add(verb + 'ed')
        forms.add(verb + 'es')
        forms.add(verb + 'ing')
    else:
        if len(verb) >= 3 and verb[-1] in 'bdgklmnprt' and verb[-2] in 'aeiou' and verb[-3] not in 'aeiou':
            forms.add(verb + verb[-1] + 'ed')
            forms.add(verb + verb[-1] + 'ing')
        else:
            forms.add(verb + 'ed')
            forms.add(verb + 'ing')
        forms.add(verb + 's')
    
    return forms

def get_american_british_variants(word: str) -> Tuple[List[str], List[str]]:
    """Get American and British spelling variants."""
    american = []
    british = []
    
    if word in AMERICAN_BRITISH_VARIANTS:
        american.append(word)
        british.append(AMERICAN_BRITISH_VARIANTS[word])
    elif word in AMERICAN_BRITISH_VARIANTS.values():
        british.append(word)
        for am, br in AMERICAN_BRITISH_VARIANTS.items():
            if br == word:
                american.append(am)
                break
    
    for suffix in ['s', 'ed', 'ing', 'er', 'est', 'ly', 'ness', 'ment', 'tion', 'sion']:
        if word.endswith(suffix):
            base = word[:-len(suffix)]
            if base in AMERICAN_BRITISH_VARIANTS:
                american.append(word)
                british.append(AMERICAN_BRITISH_VARIANTS[base] + suffix)
            elif base in AMERICAN_BRITISH_VARIANTS.values():
                british.append(word)
                for am, br in AMERICAN_BRITISH_VARIANTS.items():
                    if br == base:
                        american.append(am + suffix)
                        break
    
    return american, british

def process_slash_variants(headword: str) -> List[str]:
    """Process headwords with slashes to extract all variants."""
    return [v.strip() for v in headword.split('/')]

def read_csv_with_bom(filepath: Path) -> List[Dict[str, str]]:
    """Read CSV file handling UTF-8 BOM if present."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def get_word_family(word: str, pos: str) -> Set[str]:
    """Generate word family based on word and part of speech."""
    family = {word.lower()}
    irregular_mapping = create_reverse_irregular_verb_mapping()
    
    if pos == 'verb':
        if word.lower() in IRREGULAR_VERBS:
            verb_info = IRREGULAR_VERBS[word.lower()]
            family.update(verb_info.get('past', []))
            family.update(verb_info.get('past_participle', []))
            family.update(verb_info.get('present_participle', []))
            family.update(verb_info.get('third_person', []))
            family.update(verb_info.get('other_forms', []))
        elif word.lower() in irregular_mapping:
            base_verb = irregular_mapping[word.lower()]
            verb_info = IRREGULAR_VERBS[base_verb]
            family.add(base_verb)
            family.update(verb_info.get('past', []))
            family.update(verb_info.get('past_participle', []))
            family.update(verb_info.get('present_participle', []))
            family.update(verb_info.get('third_person', []))
            family.update(verb_info.get('other_forms', []))
        else:
            family.update(generate_regular_verb_forms(word.lower()))
    
    elif pos == 'noun':
        if word.endswith('y') and len(word) > 2 and word[-2] not in 'aeiou':
            family.add(word[:-1] + 'ies')
        elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
            family.add(word + 'es')
        else:
            family.add(word + 's')
    
    elif pos == 'adjective':
        if word.endswith('y'):
            family.add(word[:-1] + 'ier')
            family.add(word[:-1] + 'iest')
        elif word.endswith('e'):
            family.add(word + 'r')
            family.add(word + 'st')
        else:
            family.add(word + 'er')
            family.add(word + 'est')
    
    temp_family = set()
    for w in family:
        american, british = get_american_british_variants(w)
        temp_family.update(american)
        temp_family.update(british)
    family.update(temp_family)
    
    return {w.lower() for w in family if w}

def compare_cefr_levels(level1: str, level2: str) -> int:
    """Compare CEFR levels. Returns -1 if level1 < level2, 0 if equal, 1 if level1 > level2."""
    order = {'A1': 0, 'A2': 1, 'B1': 2, 'B2': 3, 'C1': 4, 'C2': 5}
    return order.get(level1, 6) - order.get(level2, 6)

def main():
    vocabulary_data = []
    word_entries = defaultdict(list)
    
    # Process all CSV files in the assets folder
    assets_dir = Path('assets')
    if not assets_dir.exists():
        print("Error: assets directory not found")
        return
    
    csv_files = list(assets_dir.glob('*.csv'))
    
    for csv_file in csv_files:
        print(f"Checking {csv_file}...")
        
        # Read the CSV file to check headers
        rows = read_csv_with_bom(csv_file)
        if not rows:
            print(f"  Skipping {csv_file}: empty file")
            continue
        
        # Get the headers (field names)
        headers = list(rows[0].keys())
        
        # Check if the first 3 headers are headword, pos, CEFR
        if len(headers) < 3 or headers[0:3] != ['headword', 'pos', 'CEFR']:
            print(f"  Skipping {csv_file}: headers do not match required format")
            print(f"    Expected: ['headword', 'pos', 'CEFR', ...]")
            print(f"    Found: {headers}")
            continue
        
        print(f"  Processing {csv_file}...")
        
        for row in rows:
            headword = row.get('headword', '').strip()
            if not headword:
                continue
            
            variants = process_slash_variants(headword)
            
            for variant in variants:
                entry = {
                    'word': variant,
                    'pos': row.get('pos', '').strip(),
                    'CEFR': row.get('CEFR', '').strip(),
                    'CoreInventory 1': row.get('CoreInventory 1', '').strip(),
                    'CoreInventory 2': row.get('CoreInventory 2', '').strip(),
                    'Threshold': row.get('Threshold', '').strip(),
                    'notes': row.get('notes', '').strip()
                }
                
                base_word = variant.lower()
                if entry['pos'] == 'verb':
                    irregular_mapping = create_reverse_irregular_verb_mapping()
                    if base_word in irregular_mapping:
                        base_word = irregular_mapping[base_word]
                
                entry['base_form'] = base_word
                
                word_entries[f"{base_word}|{entry['pos']}"].append(entry)
    
    for key, entries in word_entries.items():
        base_word, pos = key.split('|')
        
        lowest_cefr = entries[0]['CEFR']
        for entry in entries[1:]:
            if compare_cefr_levels(entry['CEFR'], lowest_cefr) < 0:
                lowest_cefr = entry['CEFR']
        
        all_word_forms = set()
        for entry in entries:
            all_word_forms.add(entry['word'].lower())
            all_word_forms.update(get_word_family(entry['word'], pos))
        
        american_forms = []
        british_forms = []
        for form in all_word_forms:
            am_variants, br_variants = get_american_british_variants(form)
            american_forms.extend(am_variants)
            british_forms.extend(br_variants)
        
        american_forms = list(set(american_forms))
        british_forms = list(set(british_forms))
        
        main_entry = entries[0].copy()
        main_entry['CEFR'] = lowest_cefr
        main_entry['base_form'] = base_word
        main_entry['word_family'] = sorted(list(all_word_forms))
        
        if american_forms or british_forms:
            main_entry['variants'] = {}
            if american_forms:
                main_entry['variants']['american'] = sorted(american_forms)
            if british_forms:
                main_entry['variants']['british'] = sorted(british_forms)
        
        for key in ['CoreInventory 1', 'CoreInventory 2', 'Threshold', 'notes']:
            values = [e.get(key, '') for e in entries if e.get(key, '')]
            main_entry[key] = ', '.join(set(values))
        
        vocabulary_data.append(main_entry)
    
    vocabulary_json = {'vocabulary': vocabulary_data}
    with open('vocabulary.json', 'w', encoding='utf-8') as f:
        json.dump(vocabulary_json, f, ensure_ascii=False, indent=2)
    
    word_lookup = {}
    for entry in vocabulary_data:
        lookup_info = {
            'base_form': entry['base_form'],
            'pos': entry['pos'],
            'CEFR': entry['CEFR']
        }
        
        for word in entry['word_family']:
            word_lower = word.lower()
            if word_lower not in word_lookup or compare_cefr_levels(lookup_info['CEFR'], word_lookup[word_lower]['CEFR']) < 0:
                word_lookup[word_lower] = lookup_info
    
    with open('word_lookup.json', 'w', encoding='utf-8') as f:
        json.dump(word_lookup, f, ensure_ascii=False, indent=2)
    
    print(f"Conversion complete!")
    print(f"Total vocabulary entries: {len(vocabulary_data)}")
    print(f"Total lookup entries: {len(word_lookup)}")

if __name__ == '__main__':
    main()