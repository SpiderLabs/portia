###################################################################
###################################################################
##
##  ----====----==== CREDIT CARD FINDER ====----====----
##
##  Usage: .\find-credit-cards.ps1 -path C:\
##   - To output to a file, use .\find-credit-cards.ps1 -path C:\ > result.txt
##
##  Features:
##   - Searches recursively through the provided path
##     searching for valid credit card numbers
##   - Large files are read in chunks so as to not
##     exhaust system resources
##
##  License:
##
##    Copyright (C) 2011 Jaap Karan Singh
##    (github.com/jksdua)
##
##    This work is licensed under the Creative Commons
##    Attribution 3.0 United States License. To view a
##    copy of this license, visit http://creativecommons
##    .org/licenses/by/3.0/us/ or send a letter to
##    Creative Commons, 171 Second Street, Suite 300,
##    San Francisco, California, 94105, USA.
##
##    This program is distributed in the hope that it
##    will be useful, but WITHOUT ANY WARRANTY; without
##    even the implied warranty of MERCHANTABILITY or
##    FITNESS FOR A PARTICULAR PURPOSE.
##
##    Contact: Twitter - @jksdua, Email - jksdua@gmail.com
##
###################################################################
###################################################################

###################################################################
## To do:
## - Allow logging to file
## - Add support for word and powerpoint
## - Modularise the file
##     Separate scanner and output
##     Compress size using techniques in
##        http://technet.microsoft.com/en-us/magazine/2008.04.securitywatch.aspx
##        http://blesseddlo.wordpress.com/2011/01/31/powershell-re-to-match-credit-card-patterns/
## - Add debug ability for printing errors
## - Add matcher for key strings such as "credit card, pci, invoice etc"
## - Add support for logging output to file
## - Use Github issue tracker for recording to do items
## - Output file type next to the filename when outputting
## - Provide stats on what filetype had the most findings etc
## - Add support for multiple streams such as db etc
## - Add support for hasehd credit cards
##     https://www.netspi.com/blog/entryid/182/cracking-credit-card-hashes-with-powershell
##     http://www.sectechno.com/2013/09/15/checking-credit-card-numbers-with-powershell/
## - Add support for detecting credit card type
## - Add incremental scan support
## - Watch for interrupt and cleanup excel and other variables
###################################################################

param (
  [string]$path = $(throw "-path is required")
)


## normalise path so both absolute and relative paths work
$path = Resolve-Path($path)

$REGEX = [regex]"(?im)(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})"
$MAX_SIZE = 50mb
$MAX_SIZE_STR = "50mb"
$BATCH = 1000

[long]$global:found = 0
$global:baseDir = split-path -parent $MyInvocation.MyCommand.Definition;

## Add support for pdf documents
try {
  $PdfDll = Join-Path -path $baseDir -childPath "\lib\itextsharp-dll-core\itextsharp.dll"
  Add-Type -Path $PdfDll
} catch [Exception] {
  #Write-Host -ForegroundColor RED ("Failed to load PDF dll. PDF files will be reported, review these manually.")
  #Write-Host ""
}

## Add support for excel documents
try {
  $global:Excel = New-Object -comobject Excel.Application
  $global:Excel.visible = $False
} catch [Exception] {
  #Write-Host -ForegroundColor RED ("Failed to load Excel dll. Excel files will be reported, review these manually.")
  #Write-Host ""
}

####################################################################
## Returns true if the given array of digits represents 
## a valid Luhn number, and false otherwise.
## source: http://codegolf.stackexchange.com/questions/22/the-luhn-algorithm-for-verifying-credit-card-numbers-etc
filter Luhn($x){$l=$x.Length-1;$l..0|%{$d=$x[$_]-48;if($_%2-eq$l%2){$s+=$d}elseif($d-le4){$s+=$d*2}else{$s+=$d*2-9}};!($s%10)}

function FindCreditCards($path) {
  [long[]]$creditCards = @()

  Foreach ($data in $input) {
    Select-String -pattern $REGEX -input $data -AllMatches |
      Foreach {
        Foreach ($match in $_.matches) {
          $creditCards += $match.value
        }
      }
  }
  # ideally this function should only return an array of findings and then the parent function should decide what to do
  ProcessFileResults -path $path -results $creditCards

  ## cleanup
  $creditCards = $data = $path = $match = $null
}

## Ensures credit cards are valid, increments global counter and prints results to console
function ProcessFileResults($path, $results) {
  [long[]]$validatedCreditCards = @()
  Foreach($val in $results) {
    if (Luhn([string]$val)) {
      $global:found++;
      $validatedCreditCards += $val
    }
  }
  PrintFileResults -path $path -results $validatedCreditCards

  ## cleanup
  $validatedCreditCards = $val = $results = $path = $null
}

function PrintFileResults($path, $results) {
  if ($results.length) {
    Write-Host -ForegroundColor GREEN ("File: " + $path)
    $len = $path.length + 6
    $line = ''
    Do {
      $line += '-'
    } Until (--$len -le 0)
    Write-Host -ForegroundColor GREEN $line
    Foreach ($item in $results) {
      Write-Host $item
    }
    #Write-Host "Found:" $results.length
    #Write-Host ""

    ## cleanup
    $path = $results = $null
  }
}

function Get-PdfContent($path) {
  $reader = New-Object iTextSharp.text.pdf.pdfreader -ArgumentList $path
  for ($page = 1; $page -le $reader.NumberOfPages; $page++) {
      $strategy = new-object  'iTextSharp.text.pdf.parser.SimpleTextExtractionStrategy'
      $currentText = [iTextSharp.text.pdf.parser.PdfTextExtractor]::GetTextFromPage($reader, $page, $strategy);
      [string[]]$Text += [system.text.Encoding]::UTF8.GetString([System.Text.ASCIIEncoding]::Convert( [system.text.encoding]::default  , [system.text.encoding]::UTF8, [system.text.Encoding]::Default.GetBytes($currentText)));
  }
  $reader.Close();
  return $Text
}

function Get-ExcelContent($path) {
  [long[]]$creditCards = @()
  $excelSheet = Get-Item -Path $path -ea stop
  $workbook = $global:Excel.Workbooks.Open($excelSheet)

  For($i = 1 ; $i -le $workbook.Sheets.count ; $i++) {
    $worksheet = $workbook.sheets.item($i)
    #"`tLooking for matches on $($worksheet.name) worksheet"
    $rowMax = ($worksheet.usedRange.rows).count
    $columnMax = ($worksheet.usedRange.columns).count
    For($row = 1 ; $row -le $rowMax ; $row ++) {
      For($column = 1 ; $column -le $columnMax ; $column ++) {
        [string]$formula = $workSheet.cells.item($row,$column).formula
        if($formula -match [regex]$REGEX) {
          $creditCards += "`t`t$($formula)"
        }
      } #end for $column
    } #end for $row
    $worksheet = $rowmax = $columnMax = $row = $column = $formula = $null
  } #end for

  $workbook.saved = $True
  $workbook.close()

  ProcessFileResults -path $path -results $creditCards

  $creditCards = $path = $null
}

# Checks if the user pressed Ctrl+C
function gotInterrupt() {
  if ([console]::KeyAvailable) {
    $key = [system.console]::readkey($true)
    return (($key.modifiers -band [consolemodifiers]"control") -and ($key.key -eq "C"))
  }
}

###################################################################
## Loops through the provided path running a scan on files and
## returns subfolders found
function Scan([string]$path) {
  ## reduce memory load if possible
  [gc]::collect()

  [string[]]$todo = @()

  $fc = new-object -com scripting.filesystemobject
  $folder = $fc.getfolder($path)

  foreach ($i in $folder.files) {
    ## get out if user wants to exit
    if (gotInterrupt) { throw "INTERRUPT" }

    $path = [string]$i.path

    try {
      if ($i.Size -gt $MAX_SIZE) {
        #Write-Host -ForegroundColor YELLOW "Review $path manually. File size of $([Math]::Truncate($i.Size/1mb))mb is greater than the max allowed size of $MAX_SIZE_STR."
        #Write-Host ""
      } else {
        ## dev
        #Write-Host "Processing file: " + $path

        if ($path -cmatch ".*\.(doc|ppt).{0,1}$") {
          ## dev
          #Write-Host "File type: office"

          #Write-Host -ForegroundColor YELLOW "Review $path manually. Office files are currently not supported."
          #Write-Host ""
        } elseif ($path -cmatch ".*\.(zip|tar|gz).{0,1}$") {
          ## dev
          #Write-Host "File type: zipped"

          #Write-Host -ForegroundColor YELLOW "Review $path manually. Zipped files are currently not supported."
          #Write-Host ""
        } elseif ($path -cmatch ".*\.(xls|xlsx).{0,1}$") {
          ## dev
          #Write-Host "File type: excel"

          Get-ExcelContent -path $path
        } elseif ($path -cmatch "\.pdf$") {
          ## dev
          #Write-Host "File type: pdf"

          # pdf by default reads line by line
            # still need to run benchmarks to ensure memory is flushed after a line has been read
          Get-PdfContent $path | FindCreditCards -path $path
        } elseif ($path -cmatch ".*\.(txt|log|bak).{0,1}$") {
          Get-Content $path -ReadCount $BATCH -ea stop |
            FindCreditCards -path $path
        } else {
          ## dev
          #Write-Host "File type: anything really"

          # using get content and batch reads the file in chunks
          # -ea stop added because open files still print an error to the console
          # see: http://stackoverflow.com/questions/3097785/powershell-ioexception-try-catch-isnt-working
          #Get-Content $path -ReadCount $BATCH -ea stop |
          #  FindCreditCards -path $path
        }
      }
    } catch [Exception] {
      ## required since streamreader may throw this
      if (!$($_.Exception.Message).CompareTo("INTERRUPT")) {
        throw $_.Exception
      }
      #Write-Host -ForegroundColor RED ("Failed to process file: " + $i.Path)
      #Write-Host ""
    }
  }

  try {
    foreach ($i in $folder.subfolders) {
      ## Dev
      #Write-Host "Found additional folder: " + $i.path

      $todo += $i.path
    }
  } catch [Exception] {
    Write-Host -ForegroundColor RED ("Failed to queue folder for scanning: " + $i.path)
    Write-Host ""
  }

  return $todo
}

function ScanManager() {
  [string[]]$todo = @()
  [string]$next = $path

  while ($next) {
    try {
      # add any additional folders identified to todo list
      $todo += Scan($next)
    } catch [Exception] {
      if (!$($_.Exception.Message).CompareTo("INTERRUPT")) {
        Write-Host "[Ctrl+C] Caught user interrupt"
        throw $_.Exception
      }
      #Write-Host -ForegroundColor RED ("Failed to scan folder: " + $next + ". Reason: " + $($_.Exception.Message))
      #Write-Host ""
    }

    # shift array to get next element
    # http://blogs.msdn.com/b/powershell/archive/2007/02/06/powershell-tip-how-to-shift-arrays.aspx
    $next, $todo = $todo
  }
}

## Catch Ctrl+C to garbage collect on exit
## http://sushihangover.blogspot.com.au/2012/03/powershell-using-try-finally-block-to.html
try {
  [console]::TreatControlCAsInput = $true
  ScanManager
  ""
  #"Total found: " + $found
  ""
# ignore exception
} catch [Exception] {
} finally {
  # No matter what the user did, reset the console to process Ctrl-C inputs 'normally'
  [console]::TreatControlCAsInput = $false

  #Write-Host "Cleaning up..."
  #Write-Host ""

  # wrapped since excel is only optionally loaded if it exists on the system
  try {
    ## cleanup excel objects
    $global:Excel.quit()
    $global:Excel = $null
  } catch [Exception] {}

  ## cleanup memory
  [gc]::collect()
  [gc]::WaitForPendingFinalizers()
  # force clean since in some instances it does not shut properly
  #try {
  #  ps excel | kill
  #} catch [Exception] {}
}



# Sample credit card data for testing
#378282246310005
#371449635398431
#371449635398432