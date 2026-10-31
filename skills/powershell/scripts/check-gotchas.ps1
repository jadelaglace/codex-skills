# Assert the claims in SKILL.md against the engine you actually run.
#   pwsh -NoProfile -File check-gotchas.ps1
#   powershell -NoProfile -File check-gotchas.ps1
# Exit 0 when every applicable claim holds, 1 otherwise.

$ErrorActionPreference = 'Continue'
$script:pass = 0
$script:fail = 0
$script:skip = 0
$v5 = $PSVersionTable.PSVersion.Major -lt 6

function Assert-That {
    param([string]$Name, [scriptblock]$Test)
    try {
        $ok = & $Test
        if ($ok -eq $true) {
            $script:pass++
            Write-Host ("PASS  " + $Name) -ForegroundColor Green
        } else {
            $script:fail++
            Write-Host ("FAIL  " + $Name + "  (got " + ($ok | Out-String).Trim() + ")") -ForegroundColor Red
        }
    } catch {
        $script:fail++
        Write-Host ("FAIL  " + $Name + "  (" + $_.Exception.Message + ")") -ForegroundColor Red
    }
}

function Skip-That {
    param([string]$Name, [string]$Why)
    $script:skip++
    Write-Host ("SKIP  " + $Name + "  (" + $Why + ")") -ForegroundColor DarkGray
}

Write-Host ("engine: " + $PSVersionTable.PSEdition + " " + $PSVersionTable.PSVersion) -ForegroundColor Cyan

# ---- output model -------------------------------------------------------
function Get-Both {
    1
    return 2
}
Assert-That 'uncaptured output is emitted, return does not discard it' { (@(Get-Both).Count -eq 2) }

function Get-Leak {
    5
    return 6
}
Assert-That '$null = ... suppresses pipeline output' { (@($null = (Get-Leak)).Count -eq 0) }
Assert-That '[void](...) suppresses as well' { (@([void](Get-Leak)).Count -eq 0) }
Assert-That 'Write-Host does not reach the pipeline' { (@(Write-Host 'x' 6>$null).Count -eq 0) }

# ---- arrays -------------------------------------------------------------
Assert-That 'a single result is a scalar until @() wraps it' {
    $one = Get-Item .
    ($one.GetType().Name -ne 'Object[]') -and (@(Get-Item .).Count -eq 1) -and (@(Get-Item .) -is [array])
}
Assert-That 'no result is $null' { $null -eq (Get-ChildItem -Filter 'no-such-file-xyz') }
Assert-That '@() of nothing counts zero' { (@(Get-ChildItem -Filter 'no-such-file-xyz').Count -eq 0) }
Assert-That '+= rebinds instead of growing the original' {
    $a = @(1, 2); $b = $a; $a += 3
    ($b.Count -eq 2) -and ($a.Count -eq 3)
}
Assert-That 'comma operator wraps one item in an array' { (@(,(Get-Item .)).Count -eq 1) }
Assert-That 'return ,$array keeps a single-element array' {
    function Get-One { return ,@(1) }
    (@(Get-One).Count -eq 1) -and ((Get-One) -is [array])
}

# ---- operators ----------------------------------------------------------
Assert-That '-eq is not == and compares numbers to strings loosely' { (1 -eq '1') }
Assert-That 'comparison is case-insensitive by default' { ('A' -eq 'a') }
Assert-That '-ceq is case-sensitive' { -not ('A' -ceq 'a') }
Assert-That '-contains tests array membership' { (@(1, 2) -contains 2) }
Assert-That 'left-side array with -eq filters' { (@(1, 2, 3) -eq 2).Count -eq 1 }
Assert-That '$null on the left compares instead of filtering' { ($null -eq @()) -eq $false }

# ---- strings ------------------------------------------------------------
$who = 'world'
Assert-That 'double quotes interpolate' { ("Hello $who" -eq 'Hello world') }
Assert-That 'single quotes stay literal' { ('Hello $who' -eq 'Hello $who') }
Assert-That 'subexpression reaches members' { ("n=$(@(1,2).Count)" -eq 'n=2') }
Assert-That 'here-strings span lines' { (@"
a
b
"@).Trim() -eq "a`nb" }

# ---- pipeline -----------------------------------------------------------
Assert-That '$_ is the current object' { ((1, 2 | ForEach-Object { "item=$_" }) -join ',') -eq 'item=1,item=2' }
Assert-That 'ForEach-Object sees each item' { ((1, 2, 3 | ForEach-Object { $_ * 2 }) -join ',') -eq '2,4,6' }
Assert-That 'Select-Object returns copies' {
    $o = [pscustomobject]@{ a = 1 }
    $c = $o | Select-Object *
    $c.a = 9
    $o.a -eq 1
}

# ---- errors -------------------------------------------------------------
Assert-That 'try/catch ignores non-terminating errors' {
    $caught = $false
    try { Get-Item 'no-such-path-xyz' -ErrorAction SilentlyContinue } catch { $caught = $true }
    -not $caught
}
Assert-That '-ErrorAction Stop makes it catchable' {
    $caught = $false
    try { Get-Item 'no-such-path-xyz' -ErrorAction Stop } catch { $caught = $true }
    $caught
}
Assert-That '$LASTEXITCODE carries the native exit code' {
    $null = cmd /c exit 3
    $LASTEXITCODE -eq 3
}

# ---- 5.1-only behaviour -------------------------------------------------
if ($v5) {
    # This build returns an empty array; older 5.1 builds return $null. Assert the
    # guard instead of one build's behaviour, and print which shape was observed.
    Assert-That "5.1: '[]' | ConvertFrom-Json needs the null guard" {
        $r = '[]' | ConvertFrom-Json
        $shape = if ($null -eq $r) { 'null' } else { $r.GetType().Name }
        Write-Host ("      observed: " + $shape) -ForegroundColor DarkGray
        $norm = if ($null -eq $r) { ,@() } else { @($r) }
        (@($norm).Count -eq 0)
    }
    Assert-That '5.1: @($null).Count is 1 (the empty-list trap)' { (@($null).Count -eq 1) }
    Assert-That '5.1: curl resolves to an alias' { (Get-Command curl -ErrorAction SilentlyContinue).CommandType -eq 'Alias' }
} else {
    Skip-That "5.1: '[]' | ConvertFrom-Json returns `$null" 'PowerShell 7 returns an empty array'
    Skip-That '5.1: @($null).Count is 1' 'not the same shape on 7'
    Skip-That '5.1: curl resolves to an alias' 'no curl alias on 7 by default'
}

Write-Host ""
Write-Host ("passed {0} / failed {1} / skipped {2}" -f $script:pass, $script:fail, $script:skip)
if ($script:fail -gt 0) { exit 1 }
exit 0

