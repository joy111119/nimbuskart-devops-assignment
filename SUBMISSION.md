# Submission — DevOps Engineer Assignment

**Candidate name: Saharsh Verma**  
**Email: saharshvermaxb@gmail.com**  
**Date submitted: 24th May 2026** 
**Hours spent (approximate): 18 hours**   

## Deliverables checklist

- [x] Part A: Terraform code under /terraform applies cleanly on LocalStack
- [x] Part A: `terraform validate` and `terraform fmt -check` both pass
- [x] Part B: Janitor script runs in --dry-run mode and produces report.json
- [x] Part B: GitHub Actions workflow runs green on a fresh PR
- [x] Part B: --delete mode respects Protected=true tag
- [x] Part C: DESIGN.md is present and within 2 pages
- [x] Walkthrough video link below is accessible (unlisted is fine)

## Walkthrough video

Link (Loom / YouTube unlisted / Google Drive):  https://www.loom.com/share/c72aeb8519264c80818de9bc6b567949
Length: max 5 minutes  

## Sample report

Path to a sample report.json produced by your script:  
`samples/report.example.json`

## Known limitations

- LocalStack does not fully emulate all AWS behaviors and services.
- The Janitor currently focuses only on a limited set of AWS orphan resource patterns.
- Cost estimates use static pricing values instead of live AWS pricing APIs.
- Monitoring and alerting integrations are conceptual and not fully implemented.

## AI usage disclosure

AI tools used:
- ChatGPT was used for understanding what is being done (for example code and real world examples of this project), Code generation for terraform, Terraform debugging, LocalStack troubleshooting, assisting and giving ideas in README.md and DESIGN.md, and generating the ASCII diagram. I continuously asked my doubts to ChatGPT about anything related to this project to keep myself on track as I progressed in the project.  
