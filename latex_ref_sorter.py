import collections.abc
import argparse


def is_iterable(arg):
    return isinstance(arg, collections.abc.Iterable) and not isinstance(arg, str)

def find_citations(string, search, dict):
    index = 0
    while True:
        index = string.find(search, index + 1)
        if index == -1:
            return
        entry = string[index:].replace('{', '}').split('}')[1]
        if "," in entry:
            for e in entry.split(','):
                e = e.strip()
                if e not in dict.values():
                    dict[str(len(dict))] = e
        else:
            entry = entry.strip()
            if entry not in dict.values():
                dict[str(len(dict))] = entry

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bib" , type =str)
    parser.add_argument("--tex" , nargs= '*', type =str)
    parser.add_argument("--save" , type =str)

    args = parser.parse_args()

    bib_file = args.bib
    tex_files = args.tex
    output_name = args.save

    if is_iterable(tex_files):
        citations_order = {}
        for tex in tex_files:
            with open(tex, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    find_citations(line, "\\cite", citations_order)
    else:
        quit()
    
    citations_entries = {}
    
    with open(bib_file, "r", encoding='utf-8') as bib:
        lines = bib.readlines()
        citation_name = ""
        entry_bib = ""
        for line in lines:
            if citation_name == "" and '{' in line:
                citation_name = line.split('{')[1].split(',')[0]
                if citation_name not in citations_order.values():
                    print(f"Entry '{citation_name}' is not found in tex files, please check, it will be removed.")
            entry_bib += line
            if line.strip() == '}':
                citations_entries[citation_name] = entry_bib
                citation_name = ""
                entry_bib = ""

    with open(output_name, "w", encoding='utf-8') as f:
        for k, v in citations_order.items():
            if v not in citations_entries.keys():
                print(f"Entry {v} is not found!")
            else:
                f.write(citations_entries[v])
    
    print(f"File '{output_name}' is saved.")

# usage: python latex_ref_sorter.py --bib "ORIGINAL BIB FILE"  --tex "TEX FILES WITH SPACE" --save "SAVENAME"