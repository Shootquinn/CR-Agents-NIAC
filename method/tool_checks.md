# Tool Checks (first session only)

1. Run `python scripts/check_tools.py`.
2. Expected output is four lines, one per tool: python, python-docx, LibreOffice, PDF text extraction. Each reads `OK <tool>` or `MISSING <tool>`.
3. On a missing tool, tell the user the install command (python-docx: `pip install python-docx`; PDF text: `pip install pypdf`; LibreOffice: download from libreoffice.org), then STOP rule (d). Resume after the user confirms the install and the script prints OK.
4. The user is likely on Windows with spaces in paths. Quote every path. Use only commands that run in PowerShell or cmd, never bash-only commands.
