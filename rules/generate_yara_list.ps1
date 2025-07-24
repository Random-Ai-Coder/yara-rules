# PowerShell script to generate a list of YARA files in a specific directory and save it as JSON
# Usage: Run this script in PowerShell to generate a list of YARA files

#Input: Specify the folder containing YARA files
$folder = "<path to rule folder in here > rules"
$output = "$folder\yara_files_list.json"


$files = Get-ChildItem -Path $folder -Recurse -Include *.yar,*.yara | Select-Object -ExpandProperty FullName
$json = @()
for ($i=0; $i -lt $files.Count; $i++) {
    $rel = $files[$i] -replace [regex]::Escape($folder + "\"), "rules/"
    $json += "$($i+1). $rel"
}
$json | ConvertTo-Json | Set-Content $output
Write-Host "File list saved to $output"