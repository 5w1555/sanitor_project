
# Sanitor

Sanitor is a static analyzer for Python codebases. Not a linter, not a style cop — just a tool that stares at your AST and says: "Why is this like that?"

It focuses on using AST, giving you a report in seconds of the most pressing strctural issues in your codebase.

---

## What It Looks For

* **Vague Naming** – `handle()`, `process_data()`, `get_info()` — all flagged if they're everywhere.
* **Cyclomatic Complexity** – Too many branches? It tells you. Default: >20.
* **Deep Nesting** – Once your function hits 3/4+ indentation levels.
* **Import Cycles** – Tarjan’s algorithm finds circular imports no matter how deep.
* **Magic Numbers** – `42`, `100`, `7` repeated 3/4+ times.
* **Similar Functions** – Heuristics catch near-duplicate functions that have essentially the same "format" and could be used as a form.

---


## Requirements

- Python 3.7+
- click

Install requirements:

```bash
pip install -r requirements.txt
```

## Installation

```bash
git clone https://github.com/TechBooper/sanitor.git
cd sanitor
pip install .
```

---


## How To Run It

```bash
python sanitor_cli.py path/to/codebase
```

Or specify thresholds/config manually:

```bash
python sanitor_cli.py . --config sanitor_config.json --json-output
```

---

## Output Example

```
📁 tests_cycles\trigger_sanitor.py
  [m] Line 1: Overused word 'handle' in 4 functions – be more specific
  [m] Line 1: Overused word 'process' in 4 functions – be more specific
  [m] Line 9: Magic number 42 appears 4× – consider a named constant
  [m] Line 12: Magic number 7 appears 4× – consider a named constant
  [m] Line 35: Functions with identical structure: compute_value, compute_val, calc_value
  [m] Line 35: Similar function cluster: compute_val, compute_value (threshold 0.8)
  [m] Line 37: Magic number 10 appears 4× – consider a named constant
  [m] Line 53: Functions with identical structure: step_one, step_two
  [m] Line 96: Large class 'BigClass' has 14 public methods - consider splitting
```


Output format: human-readable or `--json-output` for CI use.

---


## Config File (Optional)

Sanitor will use the config file you specify with `--config`. The file should be valid JSON and can override defaults:

```json
{
  "magic_numbers": {"min_repeats": 4},
  "vague_naming": {"threshold": 3},
  "ignore_patterns": ["tests/*"]
}
```

---


## Add Your Own Checks

All checks are modular. To add one:

1. Create a file in `sanitor/checks/`
2. Write an AST-based function
3. Decorate it with `@register("your-check-id")`
4. Yield `(line, message)` tuples or compatible Issue objects

It’ll be picked up automatically.

---


## Why This Exists

Sanitor was built to catch subtle code smells and structural issues that linters miss, as I had issues in my own code.

---

## License

MIT.
