# Public profile maintenance

- This is the independent profile repository `https://github.com/frostmoon-rui/frostmoon-rui`; commit and push verified profile changes to its own origin, not the bot repository.
- Use only technical skills, non-identifying project descriptions and public repository data. Never add legal names, contact details, education or institutions, addresses, age, demographic details, grades, certificates, or private accounts from reference documents.
- Do not copy, upload, link or commit source resumes, extracted resume text, document metadata or private configuration. Read references locally and write a technical summary only.
- Keep experience claims grounded. Do not invent proficiency levels, project results, awards or public repositories. Keep the already-approved public alias and artwork separate from private biographical information.
- Use English for all interactions, documentation, tracked text, SVG labels, accessibility descriptions, and test source. Use `frostmoon-rui` as the public profile alias and `CacheTide` as the contributor name; do not introduce private names or account identifiers.
- Preserve the original avatar without editing or translating it. Keep the night, moon, and cat branding; edit SVG text directly without changing the artwork.
- Verify changes offline with `python -m unittest discover -s tests -q`, parse every tracked SVG as XML, and scan all tracked UTF-8 text for Han characters. Do not run the live statistics updater for offline verification because it accesses GitHub.
- Run offline profile tests and inspect staged files before pushing. Preserve remote statistics updates with a fast-forward pull; never force-push or overwrite unrelated work.
