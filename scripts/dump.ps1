$out = "repo_dump.txt"

"# Repository Layout`n" | Set-Content $out
git ls-files | Add-Content $out

"`n# File Contents`n" | Add-Content $out

git ls-files | ForEach-Object {
    Add-Content $out "`n## FILE: $_`n"
    Get-Content $_ -Raw | Add-Content $out
}