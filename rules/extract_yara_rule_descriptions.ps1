# Save as: extract_yara_rule_descriptions.ps1
# PowerShell script to extract YARA rule descriptions from .yar and .yara files
# Usage: Run this script in PowerShell to extract descriptions and save them as JSON


# Input: Specify the folder containing YARA files
$folder = "c:\Users\-loper-araj234\TfCodebase\binaryalert\rules"
$output = "$folder\yara_rule_descriptions.json"
$results = @()
$counter = 1

# Loop through each YARA file in the specified folder
Get-ChildItem -Path $folder -Recurse -Include *.yar,*.yara | ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file
    $ruleName = ""
    $description = ""
    for ($i = 0; $i -lt $lines.Length; $i++) {
        if ($lines[$i] -match '^rule\s+(\w+)') {
            $ruleName = $matches[1]
        }
        if ($lines[$i] -match 'description\s*=\s*"([^"]+)"') {
            $description = $matches[1]
        }
        if ($ruleName -and $description) {
            $results += [PSCustomObject]@{count=$counter; rule=$ruleName; description=$description; file=(Split-Path -Leaf $file)}
            $counter++
            $ruleName = ""
            $description = ""
        }
    }
}

# Save the results as JSON
$results | ConvertTo-Json | Set-Content $output
Write-Host "Rule descriptions saved to $output"