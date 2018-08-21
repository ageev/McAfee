Function Get-FileName($initialDirectory, $Title, $Filter)
{
    [System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null
    
    $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $OpenFileDialog.initialDirectory = $initialDirectory
    $OpenFileDialog.Title = $Title
    $OpenFileDialog.filter = $Filter
    $OpenFileDialog.ShowDialog() | Out-Null
    $OpenFileDialog.filename
}
 
$file = Get-FileName $env:HOMEDRIVE "Open unzipped .bup file"
$output_filename = $file + '.virus'
$xor_key = 0x6A  #should be less than FF

$file_b = [System.IO.File]::ReadAllBytes("$file") 
$xord_byte_array = New-Object Byte[] $file_b.Count

for($i=0; $i -lt $file_b.Count ; $i++)
{
    $xord_byte_array[$i] = $file_b[$i] -bxor $xor_key
}
 
# Write the XORd bytes to the output file
[System.IO.File]::WriteAllBytes("$output_filename", $xord_byte_array)

write-host "[+] Saved to " -nonewline;
Write-host "$output_filename" -foregroundcolor yellow -nonewline; Write-host ".";