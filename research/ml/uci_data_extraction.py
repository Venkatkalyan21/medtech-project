import arff
import pandas as pd
import re
from pathlib import Path
import sys

# ...existing code...
def parse_attributes(header: str):
    attrs = []
    for m in re.finditer(r'(?im)^\s*@attribute\s+(".*?"|\'.*?\'|\S+)\s+(.+)$', header):
        name = m.group(1).strip()
        typ = m.group(2).strip()
        if name[0] in "\"'": name = name[1:-1]
        nominals = None
        nominal_map_lower = {}
        if typ.startswith("{") and typ.endswith("}"):
            vals = [v.strip().strip("'\"") for v in typ[1:-1].split(",")]
            nominals = vals
            nominal_map_lower = {v.lower(): v for v in vals}
        attrs.append({"name": name, "type": typ, "nominals": nominals, "nominal_map_lower": nominal_map_lower})
    return attrs

def load_arff_fix(path: str, out_clean_path: str | None = None):
    p = Path(path)
    text = p.read_text(encoding="utf-8")

    m = re.search(r'(?i)(\n@data\s*\n)', text)
    if not m:
        return arff.loads(text)

    header = text[: m.end()]
    data = text[m.end():]
    attr_defs = parse_attributes(header)
    attr_count = len(attr_defs)

    fixed_lines = []
    modified = False
    replaced_nominals = 0

    for lineno, line in enumerate(data.splitlines(), start=1):
        s = line.strip()
        if not s or s.startswith('%'):
            fixed_lines.append(line)
            continue

        # Normalize missing/malformed fields:
        s = re.sub(r'^\s*,', '?,', s)         # leading comma
        s = re.sub(r',\s*$', ',?', s)        # trailing comma
        while ',,' in s or re.search(r',\s*,', s):
            s = re.sub(r',\s*,', ',?,', s)   # consecutive commas -> ?,

        fields = [f.strip() for f in s.split(',')]
        if attr_count and len(fields) != attr_count:
            modified = True
            if len(fields) < attr_count:
                fields += ['?'] * (attr_count - len(fields))
            else:
                fields = fields[:attr_count]

        # Validate/normalize nominal values
        for i, val in enumerate(fields):
            if i >= len(attr_defs):
                continue
            attr = attr_defs[i]
            nominals = attr["nominals"]
            if not nominals or val == '?':
                continue
            low = val.lower()
            # exact case-insensitive match
            if low in attr["nominal_map_lower"]:
                canonical = attr["nominal_map_lower"][low]
                if canonical != val:
                    fields[i] = canonical
                    replaced_nominals += 1
                    modified = True
                continue
            # common yes/no -> present/notpresent or ckd/notckd or yes/no if declared
            if low in ("yes", "no"):
                if "present" in nominals and "notpresent" in nominals:
                    fields[i] = "present" if low == "yes" else "notpresent"
                    replaced_nominals += 1
                    modified = True
                    continue
                if "yes" in nominals and "no" in nominals:
                    fields[i] = "yes" if low == "yes" else "no"
                    replaced_nominals += 1
                    modified = True
                    continue
                if "ckd" in nominals and "notckd" in nominals:
                    fields[i] = "ckd" if low == "yes" else "notckd"
                    replaced_nominals += 1
                    modified = True
                    continue
            # try partial match (substring) as fallback
            found = None
            for nom in nominals:
                if low in nom.lower() or nom.lower() in low:
                    found = nom
                    break
            if found:
                fields[i] = found
                replaced_nominals += 1
                modified = True
                continue
            # unknown nominal -> replace with missing marker
            fields[i] = "?"
            replaced_nominals += 1
            modified = True

        fixed_lines.append(','.join(fields))

    fixed_text = header + "\n".join(fixed_lines)
    if out_clean_path:
        Path(out_clean_path).write_text(fixed_text, encoding="utf-8")
    if modified:
        print(f"Fixed malformed rows; replaced {replaced_nominals} invalid nominal values.", file=sys.stderr)

    try:
        return arff.loads(fixed_text)
    except arff.BadDataFormat as e:
        badfile = p.with_suffix('.bad.cleaned.arff')
        badfile.write_text(fixed_text, encoding="utf-8")
        print(f"arff.BadDataFormat: wrote cleaned file to {badfile!s} for inspection", file=sys.stderr)
        raise
# ...existing code...
if __name__ == "__main__":
    arff_path = "chronic_kidney_disease_full.arff"
    cleaned_path = "cleaned_chronic_kidney_disease_full.arff"
    arff_data = load_arff_fix(arff_path, out_clean_path=cleaned_path)

    uci_df = pd.DataFrame(arff_data["data"], columns=[a[0] for a in arff_data["attributes"]])
    print("Loaded:", uci_df.shape)
    print("Columns:", list(uci_df.columns))
    uci_df.to_csv("uci_ckd.csv", index=False)

    print("Saved ckd_synthetic.csv")
