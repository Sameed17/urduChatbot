#!/usr/bin/env python3
"""
Script to process cleaned Urdu text and create groups of 5 sentences.
Each group represents a sliding window of 5 consecutive sentences.
"""

import re
import os

def read_cleaned_text(file_path):
    """Read the cleaned text file and return all lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def split_into_sentences(text_lines):
    """
    Split text lines into sentences using Urdu full stop (۔) as delimiter.
    Keep the delimiters with the sentences.
    """
    sentences = []
    for line in text_lines:
        # Split by Urdu full stop but keep the delimiter
        parts = re.split(r'(۔)', line)
        current_sentence = ""
        for part in parts:
            if part == '۔':
                # Add the delimiter to the current sentence
                current_sentence += part
                if current_sentence.strip():
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
            else:
                current_sentence += part
        
        # Add any remaining text without delimiter
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
    
    return sentences

def create_sentence_groups(sentences, group_size=5):
    """
    Create groups of sentences using sliding window approach.
    Each group contains 'group_size' consecutive sentences.
    """
    groups = []
    for i in range(len(sentences) - group_size + 1):
        group = sentences[i:i + group_size]
        groups.append(group)
    return groups

def save_groups_to_file(groups, output_file):
    """Save sentence groups to a file, one group per line."""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for group in groups:
                # Join sentences in the group with a space
                line = ' '.join(group)
                file.write(line + '\n')
        print(f"Successfully saved {len(groups)} groups to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    """Main function to process the cleaned text and create sentence groups."""
    input_file = "cleaned_urdu_text.txt"
    output_file = "sentence_groups.txt"
    
    print("Reading cleaned text...")
    text_lines = read_cleaned_text(input_file)
    
    if not text_lines:
        print("No text found to process.")
        return
    
    print(f"Found {len(text_lines)} lines of text.")
    
    print("Splitting into sentences...")
    sentences = split_into_sentences(text_lines)
    print(f"Found {len(sentences)} sentences.")
    
    print("Creating groups of 5 sentences...")
    groups = create_sentence_groups(sentences, group_size=5)
    print(f"Created {len(groups)} groups.")
    
    print("Saving groups to file...")
    save_groups_to_file(groups, output_file)
    
    # Show first few examples
    print("\nFirst 3 groups:")
    for i, group in enumerate(groups[:3]):
        print(f"Group {i+1}: {' '.join(group)}")
    
    print(f"\nProcessing complete! Check {output_file} for results.")

if __name__ == "__main__":
    main()
