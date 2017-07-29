Exception calling "Create" with "1" argument(s): "At line:74 char:7
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+       ~
Missing name after filter keyword.
At line:74 char:29
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+                             ~
Unexpected token '(' in expression or statement.
At line:74 char:33
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+                                 ~
Unexpected token '{' in expression or statement."
At /pentest/Invoke-Obfuscation/Out-ObfuscatedTokenCommand.ps1:137 char:13
+             $ScriptString = Out-ObfuscatedTokenCommand ([ScriptBlock] ...
+             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : ParseException
 
Exception calling "Create" with "1" argument(s): "At line:74 char:7
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+       ~
Missing name after filter keyword.
At line:74 char:29
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+                             ~
Unexpected token '(' in expression or statement.
At line:74 char:33
+ filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x ...
+                                 ~
Unexpected token '{' in expression or statement."
At /pentest/Invoke-Obfuscation/Out-ObfuscatedTokenCommand.ps1:137 char:13
+             $ScriptString = Out-ObfuscatedTokenCommand ([ScriptBlock] ...
+             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : ParseException
 
param (
  [string]$path = $(throw ("{3}{2}{1}{0}"-f 'd','h is require','t','-pa'))
)



$path = .("{2}{0}{3}{1}" -f 'olv','ath','Res','e-P')($path)

$REGEX = [regex]"(?im)(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})"
$MAX_SIZE = 50mb
$MAX_SIZE_STR = ("{0}{1}" -f'5','0mb')
$BATCH = 1000

[long]$global:found = 0
$global:baseDir = &("{1}{2}{0}" -f 'path','spli','t-') -parent $MyInvocation."myco`mMA`ND"."defi`Ni`TIOn";


try {
  $PdfDll = .("{1}{2}{0}"-f'h','Join','-Pat') -path $baseDir -childPath ((("{7}{5}{1}{6}{0}{2}{4}{3}"-f'h','e','arp-dll-corelWbit','dll','extsharp.','Wbit','xts','lWblibl')) -CREpLAce 'lWb',[cHAR]92)
  &("{0}{1}" -f 'Add','-Type') -Path $PdfDll
} catch [Exception] {
  
  
}


try {
  $global:Excel = &("{0}{1}{2}"-f 'New-O','bje','ct') -comobject ("{2}{1}{3}{0}"-f'tion','cel.','Ex','Applica')
  $global:Excel."vISI`B`Le" = $False
} catch [Exception] {
  
  
}





filter ("{0}{1}"-f'Luh','n')($x){$l=$x."L`engtH"-1;$l..0|&('%'){$d=$x[$_]-48;if($_%2-eq$l%2){$s+=$d}elseif($d-le4){$s+=$d*2}else{$s+=$d*2-9}};!($s%10)}

function fIN`DC`R`EDi`TcArdS($path) {
  [long[]]$creditCards = @()

  Foreach ($data in $input) {
    &("{2}{0}{1}"-f 'lect-St','ring','Se') -pattern $REGEX -input $data -AllMatches |
      .("{2}{0}{1}"-f 'a','ch','Fore') {
        Foreach ($match in $_."m`ATc`hes") {
          $creditCards += $match."VAL`uE"
        }
      }
  }
  
  &("{1}{2}{3}{4}{0}" -f'ults','Proc','es','sF','ileRes') -path $path -results $creditCards

  
  $creditCards = $data = $path = $match = $null
}


function pro`C`ESs`FiLER`eSuLTS($path, $results) {
  [long[]]$validatedCreditCards = @()
  Foreach($val in $results) {
    if (&("{1}{0}" -f'uhn','L')([string]$val)) {
      $global:found++;
      $validatedCreditCards += $val
    }
  }
  &("{1}{4}{3}{0}{2}"-f 'leRe','Prin','sults','i','tF') -path $path -results $validatedCreditCards

  
  $validatedCreditCards = $val = $results = $path = $null
}

function P`RiNTfI`lERES`U`Lts($path, $results) {
  if ($results."Len`Gth") {
    &("{2}{1}{0}"-f'ost','-H','Write') -ForegroundColor ("{0}{1}" -f'GREE','N') (("{1}{0}{2}"-f 'i','F','le: ') + $path)
    $len = $path."lENg`TH" + 6
    $line = ''
    Do {
      $line += '-'
    } Until (--$len -le 0)
    .("{0}{1}{2}" -f 'Wri','te-H','ost') -ForegroundColor ("{1}{0}"-f'N','GREE') $line
    Foreach ($item in $results) {
      &("{0}{1}{2}"-f'W','rite','-Host') $item
    }
    
    

    
    $path = $results = $null
  }
}

function geT-Pdf`C`o`NTe`NT($path) {
  $reader = &("{0}{2}{1}"-f'New-Ob','t','jec') ("{0}{2}{4}{1}{3}" -f'iT','f.p','e','dfreader','xtSharp.text.pd') -ArgumentList $path
  for ($page = 1; $page -le $reader."n`umB`Ero`FPaG`Es"; $page++) {
      $strategy = .("{2}{0}{1}{3}" -f 'ew','-objec','n','t')  ("{10}{1}{11}{7}{13}{6}{3}{2}{4}{5}{14}{12}{8}{0}{9}" -f 'tr','ar','extEx','T','t','r','.Simple','.p','S','ategy','iTextSh','p.text','n','df.parser','actio')
      $currentText = [iTextSharp.text.pdf.parser.PdfTextExtractor]::("{0}{2}{1}" -f 'GetTextFro','e','mPag').Invoke($reader, $page, $strategy);
      [string[]]$Text += [system.text.Encoding]::"UT`F8"."G`ETstRi`Ng"([System.Text.ASCIIEncoding]::"COnv`E`RT"( [system.text.encoding]::"D`EfAUlt"  , [system.text.encoding]::"U`Tf8", [system.text.Encoding]::"dE`F`AuLt".("{2}{1}{0}" -f 'tes','y','GetB').Invoke($currentText)));
  }
  $reader.("{1}{0}"-f 'e','Clos').Invoke();
  return $Text
}

function GET-EXc`eLC`onT`eNT($path) {
  [long[]]$creditCards = @()
  $excelSheet = .("{0}{2}{1}"-f 'Ge','em','t-It') -Path $path -ea ("{1}{0}" -f'top','s')
  $workbook = $global:Excel."wo`RkBO`oKS".("{0}{1}"-f 'Op','en').Invoke($excelSheet)

  For($i = 1 ; $i -le $workbook."sHe`ets"."cOU`Nt" ; $i++) {
    $worksheet = $workbook."shE`eTs".("{1}{0}" -f'tem','i').Invoke($i)
    
    $rowMax = ($worksheet."Use`dRA`N`Ge"."R`ows")."c`ouNT"
    $columnMax = ($worksheet."usED`R`AnGe"."cOLuM`Ns")."co`UNT"
    For($row = 1 ; $row -le $rowMax ; $row ++) {
      For($column = 1 ; $column -le $columnMax ; $column ++) {
        [string]$formula = $workSheet."C`ELLS".("{0}{1}"-f 'ite','m').Invoke($row,$column)."fOR`mU`la"
        if($formula -match [regex]$REGEX) {
          $creditCards += "`t`t$($formula)"
        }
      } 
    } 
    $worksheet = $rowmax = $columnMax = $row = $column = $formula = $null
  } 

  $workbook."Sav`eD" = $True
  $workbook.("{0}{1}"-f'clos','e').Invoke()

  .("{2}{0}{1}{3}"-f 'c','es','Pro','sFileResults') -path $path -results $creditCards

  $creditCards = $path = $null
}


function g`O`TINte`RrUPt() {
  if ([console]::"kEyA`Vai`LAb`le") {
    $key = [system.console]::("{2}{1}{0}"-f'key','ead','r').Invoke($true)
    return (($key."Mo`dIfIerS" -band [consolemodifiers]("{0}{1}{2}" -f'c','ontr','ol')) -and ($key."K`ey" -eq "C"))
  }
}




function sc`An([string]$path) {
  
  [gc]::("{1}{2}{0}"-f'ct','col','le').Invoke()

  [string[]]$todo = @()

  $fc = &("{1}{2}{0}{3}"-f '-objec','ne','w','t') -com ("{2}{1}{4}{7}{5}{3}{0}{6}" -f 'o','pting.file','scri','m','s','e','bject','yst')
  $folder = $fc.("{1}{0}"-f'lder','getfo').Invoke($path)

  foreach ($i in $folder."FI`LeS") {
    
    if (.("{2}{0}{1}{3}"-f'nter','r','gotI','upt')) { throw ("{1}{0}{2}"-f 'NTER','I','RUPT') }

    $path = [string]$i."Pa`Th"

    try {
      if ($i."S`IZE" -gt $MAX_SIZE) {
        
        
      } else {
        
        

        if ($path -cmatch ".*\.(doc|ppt).{0,1}$") {
          
          

          
          
        } elseif ($path -cmatch ".*\.(zip|tar|gz).{0,1}$") {
          
          

          
          
        } elseif ($path -cmatch ".*\.(xls|xlsx).{0,1}$") {
          
          

          &("{0}{1}{3}{2}{4}"-f 'Ge','t-Excel','onte','C','nt') -path $path
        } elseif ($path -cmatch "\.pdf$") {
          
          

          
            
          .("{1}{0}{2}{3}"-f 'Pd','Get-','f','Content') $path | .("{0}{2}{4}{1}{3}"-f'Find','itCard','Cre','s','d') -path $path
        } elseif ($path -cmatch ".*\.(txt|log|bak).{0,1}$") {
          &("{2}{1}{3}{0}"-f'ent','Con','Get-','t') $path -ReadCount $BATCH -ea ("{1}{0}"-f'op','st') |
            .("{1}{2}{4}{3}{0}"-f 'ds','FindCredi','tC','r','a') -path $path
        } else {
          
          

          
          
          
          
          
        }
      }
    } catch [Exception] {
      
      if (!$($_."eXC`E`Ption"."Me`SSAge").("{2}{1}{0}" -f 'mpareTo','o','C').Invoke(("{2}{0}{3}{1}" -f'T','PT','IN','ERRU'))) {
        throw $_."eXcEpT`i`ON"
      }
      
      
    }
  }

  try {
    foreach ($i in $folder."S`ub`FO`ldErS") {
      
      

      $todo += $i."Pa`TH"
    }
  } catch [Exception] {
    &("{1}{0}{2}"-f'-','Write','Host') -ForegroundColor ("{1}{0}" -f'D','RE') (("{4}{2}{6}{5}{3}{0}{1}" -f'nning',': ','ue','a','Failed to que','or sc',' folder f') + $i."P`ATh")
    .("{2}{3}{1}{0}" -f 'Host','te-','Wr','i') ""
  }

  return $todo
}

function scan`man`AG`ER() {
  [string[]]$todo = @()
  [string]$next = $path

  while ($next) {
    try {
      
      $todo += &("{0}{1}"-f'Sca','n')($next)
    } catch [Exception] {
      if (!$($_."ex`C`ePTION"."M`ess`AGE").("{1}{0}{2}"-f'r','Compa','eTo').Invoke(("{2}{0}{1}" -f 'U','PT','INTERR'))) {
        .("{1}{0}{2}"-f 'Ho','Write-','st') ("{3}{1}{0}{7}{8}{2}{4}{6}{5}"-f 'r','t','ser','[C',' i','rrupt','nte','l+C] ','Caught u')
        throw $_."ExCE`PT`Ion"
      }
      
      
    }

    
    
    $next, $todo = $todo
  }
}



try {
  [console]::"treATCON`TROL`casin`PUT" = $true
  .("{1}{0}{2}{3}"-f'nMan','Sca','age','r')
  ""
  
  ""

} catch [Exception] {
} finally {
  
  [console]::"treATCOnt`ROlc`AS`I`N`PUt" = $false

  
  

  
  try {
    
    $global:Excel.("{1}{0}" -f'uit','q').Invoke()
    $global:Excel = $null
  } catch [Exception] {}

  
  [gc]::("{1}{0}" -f 'ct','colle').Invoke()
  [gc]::("{3}{5}{6}{2}{7}{1}{0}{4}"-f 'naliz','ingFi','Pe','WaitF','ers','o','r','nd').Invoke()
  
  
  
  
}
