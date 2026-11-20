Get-ChildItem -Path src, services, tests -Recurse -Include *.ts, *.tsx | ForEach-Object {
  "## FILE: $($_.FullName)`n"
  Get-Content $_.FullName -Raw
} | Set-Content src_dump.txt