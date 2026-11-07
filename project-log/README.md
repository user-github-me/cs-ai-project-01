# Stage 2 process records

Reporting period: **25 October–7 November 2026**. The records are compiled from existing dated repository changes, recorded requests, and saved verification results. They explicitly distinguish historical records, current AI-assisted checks, and missing human evidence.

- [Project log — Word](BlueImpulse_Stage2_ProjectLog.docx)
- [Project log — PDF](BlueImpulse_Stage2_ProjectLog.pdf)
- [Editable project-log source](source/project-records.json)
- [Requirements and readiness](REQUIREMENTS_AND_READINESS.md)

The main Word/PDF files above are the complete assignment copies, including the recorded roster names and student IDs. Meeting summaries and significant AI interactions appear beside the relevant dated entry. The contribution table is at the end. Git links are supplementary: the document includes the selected changes and results needed to understand its claims.

The team must still verify its roster information, review the log, agree relative contribution scores, and provide missing meeting/feedback evidence if it exists. A retrospective evidence compilation cannot replace contemporaneous records or a student's own reflection. No attendance, scores, feedback, elapsed working hours, or personal learning has been invented.

Matching project-log copies and the personal logs are retained in `private-submissions/stage2/`. Despite that historical folder name, the user explicitly requested that the repository, logs, and submission materials remain public for the professor. GitHub visibility was restored and verified as PUBLIC. This is a recorded user-directed exception to the assignment privacy instruction. The required combined personal-log document remains a draft because four members' Stage 2 writing is not present in the available records. Each student must write and check their own section. Submit the completed single Word or PDF through the designated assignment channel, without a ZIP.

Rebuild the documents with Python 3.9+, `python-docx`, ReportLab, and PyMuPDF:

```sh
python3 project-log/source/build_records.py
```

The script refreshes its source copies from the existing personal logs when rebuilding. It never infers personal learning from file production. To record verified final outcomes of the current revision, append documented blocks to `source/completion-updates.json` and rebuild; do not mark a check passed before it has actually run.
