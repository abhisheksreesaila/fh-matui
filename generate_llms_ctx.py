"""
Generate LLM context file from llms.txt documentation links.

This script reads llms.txt, extracts all markdown file links,
reads each referenced documentation file, and concatenates them
into a single llms-ctx.txt file for LLM context integration.

Usage:
    python generate_llms_ctx.py
"""

import re
from pathlib import Path


def generate_local_ctx(llms_file='llms.txt', output_file='llms-ctx.txt'):
    """
    Generate LLM context file from llms.txt documentation links.
    
    Args:
        llms_file: Path to llms.txt file containing project overview and doc links
        output_file: Path to output context file (llms-ctx.txt)
    """
    llms_path = Path(llms_file)
    if not llms_path.exists():
        print(f"Error: {llms_file} not found.")
        return False

    print(f"Reading {llms_file}...")
    content = llms_path.read_text(encoding='utf-8')
    
    # Find all links in the format [title](url)
    links = re.findall(r'\[.*?\]\((.*?)\)', content)
    
    if not links:
        print(f"Warning: No documentation links found in {llms_file}")
        return False
    
    print(f"Found {len(links)} documentation file(s) to process\n")
    
    ctx_output = []
    processed_count = 0
    skipped_count = 0
    
    for link in links:
        # Convert web-style path to local path
        local_path = Path(link)
        
        if local_path.exists():
            print(f"  ✓ Processing: {local_path}")
            try:
                file_text = local_path.read_text(encoding='utf-8')
                # Format follows the llms-ctx standard:
                # File path as header, then content, then separator
                ctx_output.append(f"FILE: {link}\n")
                ctx_output.append(file_text)
                ctx_output.append("\n" + "="*80 + "\n")
                processed_count += 1
            except Exception as e:
                print(f"  ✗ Error reading {local_path}: {e}")
                skipped_count += 1
        else:
            print(f"  ✗ Skipping: {local_path} (File not found)")
            skipped_count += 1

    if processed_count == 0:
        print("\nError: No files were successfully processed")
        return False
    
    # Write output file
    output_path = Path(output_file)
    output_path.write_text("\n".join(ctx_output), encoding='utf-8')
    
    # Calculate file size
    file_size = output_path.stat().st_size
    size_mb = file_size / (1024 * 1024)
    size_kb = file_size / 1024
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully generated {output_file}")
    print(f"  - Processed: {processed_count} file(s)")
    if skipped_count > 0:
        print(f"  - Skipped: {skipped_count} file(s)")
    print(f"  - Output size: {size_mb:.2f} MB ({size_kb:.1f} KB)")
    print(f"{'='*60}")
    
    return True


if __name__ == "__main__":
    success = generate_local_ctx()
    exit(0 if success else 1)
