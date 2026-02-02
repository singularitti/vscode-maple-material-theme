import re
import json
import pandas as pd


__all__ = [
    "extract_key_doc_from_md",
    "merge_colors_with_docs",
    "export_colors_with_meaning",
    "merged_json_to_dataframe",
]


def extract_key_doc_from_md(md_text):
    # Match - `key`: doc (multiline allowed)
    pat = re.compile(
        r"^\s*-\s*`([a-zA-Z0-9\.\_\-]+)`:?\s+(.*?)(?=\n\s*-\s*`|$)",
        re.MULTILINE | re.DOTALL,
    )
    out = {}
    for m in pat.finditer(md_text):
        key, doc = m.group(1).strip(), m.group(2).strip()
        doc = re.sub(r"\s+", " ", doc)
        out[key] = doc
    return out


def merge_colors_with_docs(json_colors, docs):
    merged = {}
    for key, color in json_colors.items():
        merged[key] = {"color": color, "meaning": docs.get(key, None)}
    return merged


def export_colors_with_meaning(md_path, json_path, out_path):
    # Read Markdown
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    # Read JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Extract 'colors' sub-dict if present
    colors = data.get("colors", data)
    docs = extract_key_doc_from_md(md_text)
    merged = merge_colors_with_docs(colors, docs)
    # Write output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    return merged


def merged_json_to_dataframe(merged_dict):
    # Turn dict of dicts into DataFrame
    df = pd.DataFrame.from_dict(merged_dict, orient="index")
    df.index.name = "key"
    return df


if __name__ == "__main__":
    md_file = "docs/doc.md"
    json_file = "themes/maple-material-light-color-theme.json"
    out_file = "colors_with_docs.json"

    # Merge docs and write output
    merged = export_colors_with_meaning(md_file, json_file, out_file)

    # Convert merged JSON to DataFrame
    df = merged_json_to_dataframe(merged)

    # Show or use the DataFrame
    print(df.head())
