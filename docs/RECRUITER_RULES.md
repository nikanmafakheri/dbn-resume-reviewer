# Recruiter Rules

## DBN Scoring Standards

Recruiters can define custom evaluation criteria via DBN Standards. Each standard contains:

- **Name** — e.g., "Tech Lead 2026"
- **Version** — e.g., "1.0"
- **Criteria** — weighted evaluation dimensions:
  - Name (e.g., "Experience", "Education", "Skills")
  - Weight (relative importance)
  - Max Score (per-criterion ceiling)
  - Sort Order (display sequence)

## Current vs. Flexible Scoring

The current MVP uses flat four-dimension scoring (Overall, ATS, Grammar, Recruiter) determined by the AI. The DBN Standard system provides the infrastructure for configurable rubrics where recruiters can:

1. Define custom criteria
2. Set relative weights
3. Activate/deactivate standards
4. Map analysis results to standard criteria (future)

## Future Enhancements

- Bulk candidate comparison view
- Standard-based filtering and search
- Score normalization across different standards