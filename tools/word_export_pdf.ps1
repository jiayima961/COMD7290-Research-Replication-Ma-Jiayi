param([Parameter(Mandatory=$true)][string]$InputDocument,[Parameter(Mandatory=$true)][string]$OutputPdf)
$ErrorActionPreference = 'Stop'
$verificationWord = $null
$verificationDocument = $null
$verificationNoSave = 0
try {
    $verificationWord = New-Object -ComObject Word.Application
    $verificationWord.Visible = $false
    $verificationWord.DisplayAlerts = 0
    $verificationWord.AutomationSecurity = 3
    $verificationDocument = $verificationWord.Documents.Open($InputDocument, $false, $true, $false)
    $verificationDocument.ExportAsFixedFormat($OutputPdf, 17)
    Write-Output $OutputPdf
} finally {
    if ($null -ne $verificationDocument) { $verificationDocument.Close([ref]$verificationNoSave) }
    if ($null -ne $verificationWord) {
        if ($verificationWord.Documents.Count -eq 0) { $verificationWord.Quit([ref]$verificationNoSave) }
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($verificationWord)
    }
}
