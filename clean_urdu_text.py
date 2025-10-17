import re

def normalize_urdu_text(text):
    """
    Normalize Urdu text by:
    1. Removing diacritics
    2. Standardizing Alef forms
    3. Standardizing Yeh forms
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove Arabic diacritical marks (Harakat)
    # These include: Fatha, Damma, Kasra, Sukun, Shadda, Tanwin, etc.
    diacritics = [
        '\u0610', '\u0611', '\u0612', '\u0613', '\u0614', '\u0615', '\u0616',
        '\u0617', '\u0618', '\u0619', '\u061A', '\u064B', '\u064C', '\u064D',
        '\u064E', '\u064F', '\u0650', '\u0651', '\u0652', '\u0653', '\u0654',
        '\u0655', '\u0656', '\u0657', '\u0658', '\u0659', '\u065A', '\u065B',
        '\u065C', '\u065D', '\u065E', '\u065F', '\u0670', '\u06D6', '\u06D7',
        '\u06D8', '\u06D9', '\u06DA', '\u06DB', '\u06DC', '\u06DF', '\u06E0',
        '\u06E1', '\u06E2', '\u06E3', '\u06E4', '\u06E7', '\u06E8', '\u06EA',
        '\u06EB', '\u06EC', '\u06ED'
    ]
    
    for diacritic in diacritics:
        text = text.replace(diacritic, '')
    
    # Standardize Alef forms to regular Alef (ا)
    # أ (Alef with Hamza above), إ (Alef with Hamza below), آ (Alef with Madda)
    text = re.sub('[أإٱ]', 'ا', text)
    
    # Standardize Yeh forms to Urdu Yeh (ی)
    # ى (Arabic Yeh), ئ (Yeh with Hamza), ي (Arabic Yeh)
    text = re.sub('[يىئ]', 'ی', text)
    
    # Remove Zero-width non-joiner (ZWNJ) and Zero-width joiner (ZWJ)
    text = text.replace('\u200c', '').replace('\u200d', '')
    
    # Normalize fancy/smart quotation marks to ASCII
    text = text.replace('\u2018', "'")  # ' → '
    text = text.replace('\u2019', "'")  # ' → '
    text = text.replace('\u201C', '"')  # " → "
    text = text.replace('\u201D', '"')  # " → "
    text = text.replace('\u201A', "'")  # ‚ → '
    text = text.replace('\u201E', '"')  # „ → "
    
    # Normalize special punctuation
    text = text.replace('\u2026', '...')  # … → ...
    text = text.replace('\u2013', '-')    # – → -
    text = text.replace('\u2014', '-')    # — → -
    text = text.replace('`', "'")         # ` → '
    
    return text.strip()

def process_tsv_file(input_file, output_file):
    """
    Process the TSV file and extract cleaned Urdu sentences
    """
    cleaned_sentences = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Skip header line
            next(f)
            
            for line_num, line in enumerate(f, start=2):
                try:
                    # Split by tab and extract sentence column (index 2)
                    columns = line.strip().split('\t')
                    if len(columns) > 2:
                        sentence = columns[2]
                        if sentence:  # Only process non-empty sentences
                            cleaned_sentence = normalize_urdu_text(sentence)
                            if cleaned_sentence:  # Only add non-empty cleaned sentences
                                cleaned_sentences.append(cleaned_sentence)
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
        
        # Write cleaned sentences to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in cleaned_sentences:
                f.write(sentence + '\n')
        
        print(f"Successfully processed {len(cleaned_sentences)} sentences")
        print(f"Cleaned text saved to: {output_file}")
        
        # Show some examples
        print("\nFirst 5 cleaned sentences:")
        for i, sentence in enumerate(cleaned_sentences[:5], 1):
            print(f"{i}. {sentence}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_file = "final_main_dataset.tsv"
    output_file = "cleaned_urdu_text.txt"
    
    process_tsv_file(input_file, output_file)

