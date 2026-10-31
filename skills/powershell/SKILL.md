---
name: powershell
description: >-
  Avoid the PowerShell mistakes that survive review: output that leaks from
  functions, scalars where arrays were expected, `==` instead of `-eq`, and the
  Windows PowerShell 5.1 traps around UTF-8 BOM, Invoke-WebRequest and stderr
  redirection. Use when writing or debugging a .ps1 script, when a function
  returns the wrong shape, when Chinese text turns into question marks, when an
  HTTP call throws without a response, or when a pipeline silently drops items.
  Keywords — PowerShell, pwsh, 5.1, 脚本, 数组, 返回, 管道, 编码, BOM, 乱码,
  中文, Invoke-WebRequest, stderr, LASTEXITCODE.
metadata:
  version: "1.0.0"
---

# PowerShell

PowerShell is not "bash with objects". Its output model, its array behaviour and
its error model each produce bugs that look like logic errors but are language
semantics.

## Output is a stream, not a return value

Everything an expression emits goes to the pipeline, whether or not you wrote
`return`:

```powershell
function Get-Both {
    1            # emitted
    return 2     # also emitted, and does not discard the 1
}
@(Get-Both).Count   # 2, not 1
```

- `Write-Host` writes to the host, not the pipeline — it is for the human, never
  for data.
- Suppress noise with `$null = ...` or `[void](...)`; both are idiomatic.
- If a function must emit exactly one value, capture intermediate calls
  (`$x = Do-Thing`) instead of calling them bare.

## Arrays: three shapes, one variable

| Situation | Result | Guard |
| --- | --- | --- |
| one item | scalar, not an array | `@(...)` forces an array |
| no items | `$null` | `@($x).Count` is safe, `$x.Count` is not |
| pipeline input | items arrive one at a time | `,$array` passes it whole |

`+=` copies the whole array each time; in a loop it is quadratic. Use
`[System.Collections.Generic.List[object]]` and `.Add()`.

`return ,$array` keeps the array intact when a single-element array would
otherwise collapse to that element.

## Comparison and matching

- `-eq -ne -gt -lt -ge -le` — `==`, `!=`, `>` are not operators here (`>` is
  redirection, which is worse than an error).
- `-like` is wildcard, `-match` is regex; both return a boolean, and `-match`
  also populates `$Matches`.
- `-contains` asks "is this element in the collection"; `-in` is the mirror and
  also works.
- Comparisons are case-insensitive by default; `-ceq`, `-cmatch`, `-clike` are
  the case-sensitive forms.
- Put `$null` on the **left**: `$null -eq $var`. With an array on the left,
  `-eq` filters instead of comparing, so `$var -eq $null` can return an empty
  array rather than `$false`.

## Strings

```powershell
"Hello $name"        # interpolates
'Hello $name'        # literal
"Count: $($arr.Count)"   # subexpression, needed for members
@"
multi
line
"@
```

Backtick escapes: `` `n `` newline, `` `t `` tab, `` `` ` `` literal backtick.
Prefer single quotes when nothing needs expanding — it removes an entire class
of accidental `$` expansion, especially in regexes.

## Pipeline

- `$_` and `$PSItem` are the current object.
- `foreach ($x in $y)` is a statement and cannot take a pipeline; use
  `ForEach-Object` in a pipeline.
- `-PipelineVariable` (`-pv`) keeps an intermediate without breaking the chain.
- `Select-Object` produces copies. Mutating the result does not change the
  source object.

## Errors

- `$ErrorActionPreference` sets the default; `-ErrorAction Stop` promotes a
  non-terminating error to a terminating one **for that call**.
- `try/catch` only sees terminating errors. `catch` around a cmdlet without
  `-ErrorAction Stop` is decoration.
- `$?` is whether the last command succeeded; `$LASTEXITCODE` is the exit code
  of the last **native** program. They are not interchangeable.

## Windows PowerShell 5.1 traps

These do not reproduce in PowerShell 7, which is exactly why they bite: the
script is tested in `pwsh` and deployed to `powershell.exe`.

| Trap | Symptom | Fix |
| --- | --- | --- |
| `.ps1` with Chinese text and no BOM | parsed as GBK, mojibake and bizarre parse errors | save UTF-8 **with BOM**; after any tool rewrites the file, restore it: `[IO.File]::WriteAllText($p, $c, (New-Object Text.UTF8Encoding $true))` |
| `Invoke-WebRequest` without `-UseBasicParsing` | POST throws `NullReferenceException`, GET works | always pass `-UseBasicParsing` on 5.1 |
| Chinese JSON body sent as a string | arrives as `???`, irreversible | `-ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($json))` |
| `2>&1` on a native command under `$ErrorActionPreference='Stop'` | `NativeCommandError` from a mere warning line | do not redirect native stderr; branch on `$LASTEXITCODE` |
| `'[]' \| ConvertFrom-Json` | older 5.1 builds return `$null` (then `@($null).Count` is 1, an "empty list" counted as one item); 5.1.26100 returns an empty array | normalize once: `if ($null -eq $r) { ,@() } else { @($r) }` |
| `curl` | resolves to the `Invoke-WebRequest` alias | call `curl.exe` |
| variable names | case-insensitive: `$base` overwrites `$Base` | print the URI/path you are about to use before blaming the API |

The BOM rule and the alias rule are the two that cost the most time, because
neither produces an error that names the real cause.

## Verify instead of trusting

`scripts/check-gotchas.ps1` asserts the behaviours above against the engine you
run it on and prints PASS/FAIL per claim:

```powershell
pwsh -NoProfile -File scripts/check-gotchas.ps1        # PowerShell 7
powershell -NoProfile -File scripts/check-gotchas.ps1  # Windows PowerShell 5.1
```

Claims that only exist on 5.1 are reported as SKIP under 7 rather than
pretending to pass. If a claim fails on your engine, that engine's behaviour is
the truth and this document needs a note — do not "fix" the test.

## Cross-platform

`pwsh` is PowerShell 7+; `powershell` is Windows PowerShell 5.1. Use
`Join-Path` rather than string concatenation, `$env:VAR` for environment, and
full cmdlet names in scripts — `ls` and `cat` are aliases that do not exist
everywhere.