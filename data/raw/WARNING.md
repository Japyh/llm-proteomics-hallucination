# CRITICAL PRIVACY WARNING

## NEVER COMMIT REAL PATIENT DATA TO THIS REPOSITORY

This directory is for LOCAL USE ONLY. Real clinical data, patient information, or protected health information (PHI) must NEVER be committed to version control.

### Prohibited Data

**DO NOT** place any of the following in this repository:
- Real patient records
- Clinical mass spectrometry results from actual patients
- Personally Identifiable Information (PII)
- Protected Health Information (PHI)
- Medical record numbers
- Patient names, dates of birth, addresses
- Real hospital or clinic identifiers
- Any data that could be traced back to individual patients

### Legal and Ethical Obligations

- **GDPR Compliance**: Real patient data requires proper consent and data protection measures
- **HIPAA Compliance**: Protected health information must be stored securely
- **Research Ethics**: IRB approval required before processing real clinical data
- **Data Breach**: Committing real patient data could constitute a serious data breach

### What You Should Do

1. **Use Synthetic Data**: Use the synthetic datasets in `data/synthetic/`
2. **Anonymize First**: If you must work with real data locally, anonymize it first
3. **Local Storage**: Keep real data on encrypted, secure local storage
4. **Check Before Commit**: Always review `git status` before committing
5. **Use .gitignore**: Verify that data files are properly ignored

### If Real Data Is Accidentally Committed

1. **DO NOT** just delete the file and commit again (it remains in history)
2. **STOP** immediately and do not push to remote
3. **Contact** project leads immediately (olaflaitinen, Japyh)
4. **Follow** data breach protocol in `/ethics/data_management_plan.md`
5. **Use** `git filter-branch` or BFG Repo-Cleaner to remove from history
6. **Report** to relevant authorities as required by law

### Verification

Before any commit, run:
```bash
python scripts/check_data_privacy.py
```

This will scan for potential PII in your staged files.

### Questions?

If you have ANY questions about what data is safe to commit, ask first. When in doubt, DO NOT commit.

---

**Remember**: Patient privacy and data protection are not just legal requirements - they are ethical obligations to the people who trust us with their health information.
