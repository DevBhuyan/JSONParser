# JSONParser

`JSONParser` is a lightweight Python utility that enables easy flattening and inflating of complex/nested JSON data. Additionally, it provides a flexible search mechanism over JSON structures.

## Features
- 🔽 Flatten deeply nested JSON into a flat dictionary.
- 🔼 Inflate flat JSON into the original structure.
- 🔍 Search functionality includes:
  - Keyword search with options for:
    - Case sensitivity
    - Fuzzy matching (via `difflib`)
    - Filtering by keys or values
  - Multi-word query search:
    - Ranks results based on how many words match
    - Customisable number of top results (`n_results`)

---

## Installation
Clone the repository and ensure you have Python 3.x installed.

```bash
git clone https://github.com/DevBhuyan/JSONParser.git
cd JSONParser
```

Or download the source code using:

1. `wget`
```bash
wget https://github.com/DevBhuyan/JSONParser/archive/refs/tags/linux-binary.zip
```

2. `curl`
```bash
curl -LO https://github.com/DevBhuyan/JSONParser/archive/refs/tags/linux-binary.zip
```


## Usage
Ensure you have a `complex_json.json` file in the same directory.

Run the script:
```bash
python main.py
```

### Programmatic Usage
```python
from main import (
    flatten_data,
    inflate_data,
    search_by_keyword,
    search_by_query
)

flat = flatten_data(nested_dict)
nested = inflate_data(flat)

# Basic keyword search
search_results = search_by_keyword(flat, "source", close_matches=True)

# Multi-word search
query_results = search_by_query("document sensitive policy", flat, n_results=10)

```

## Example Input (`complex_json.json`)
```json
{
  "user": {
    "name": "Dev",
    "roles": ["admin", "editor"]
  },
  "meta": {
    "created": "2025-06-01"
  }
}
```

## Output of Flatten
```json
{
  "user.name": "Dev",
  "user.roles.0": "admin",
  "user.roles.1": "editor",
  "meta.created": "2025-06-01"
}
```

## License
MIT License

## Author
Devvjiit Bhuyan
