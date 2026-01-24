# Recipe Vision Engine

Converts recipes from .jpg images into Markdown text using [Gemini image understanding](https://ai.google.dev/gemini-api/docs/image-understanding).

Each recipe can be provided as a single .jpg image or as a folder containing multiple .jpg images. The AI converter iterates over all images and directories in the source directory and sends them to the AI for conversion.

The generated Markdown can then be passed to a Markdown-to-HTML parser to produce a web page with the available recipes.

## Prerequesites

- Python 3.10 + installed
- The [uv](https://github.com/astral-sh/uv) project/package manager ([installation docs](https://docs.astral.sh/uv/getting-started/installation/))
- Access to a Unix-like shell (e.g. ```zsh``` or ```bash```)
- A [Google AI Studio](https://aistudio.google.com/app/welcome) account

## Quick Start:

Create a ```.env``` file with ```GEMINI_API_KEY``` in it.
 
Create a venv
```bash
uv venv
```

Activate the .venv
```bash
source .venv/bin/activate
```

Sync dependencies:
```bash
uv sync
```

Run the project:
```bash
uv run main.py 
```

or verbose:

```bash
uv run main.py --verbose
```

## Tools available for the model:

- **Write files:** To save the markdown in the destination folder.

## Example of files in the recipes_source folder:
├── 2015-07-31 Esfirra
│   ├── Esfirra 001.jpg
│   └── Esfirra 002.jpg
└── bife a milanesa.png

## Improvement Ideas
- Cost estimation: I want to know how much the convertio from image to Markdown would cost, before the convention. For me to decide if I should remove some recipes for convention.
