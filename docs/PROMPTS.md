# Prompt Templates

The AI layer uses Markdown prompt templates located in `backend/app/ai/prompts/`.

## resume_analysis.md

The main scoring prompt. Injects `{resume_text}` and asks the LLM to return JSON with:
- `overall_score` (0-100)
- `ats_score` (0-100)
- `grammar_score` (0-100)
- `recruiter_score` (0-100)
- `summary` (string)
- `feedback` (object, optional)

## ats.md

ATS compatibility analysis. Returns:
- `ats_score` (0-100)
- `issues` (list of strings)
- `recommendations` (list of strings)

## grammar.md

Grammar and style analysis. Returns:
- `grammar_score` (0-100)
- `issues` (list of `{type, text, suggestion}`)

## cover_letter.md

Cover letter generation. Returns:
- `subject` (string)
- `body` (string)

## Adding New Prompts

1. Create a new `.md` file in `backend/app/ai/prompts/`
2. Use `{variable_name}` for template variables
3. Load it via `_load_prompt("filename.md", variable_name=value)`
4. The LLM will receive the rendered prompt and return JSON