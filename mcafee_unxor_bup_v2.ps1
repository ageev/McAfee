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
 
$file = Get-FileName $env:HOMEDRIVE "Open unzipped .bup file" "McAfee Quarantine files (*.bup)|*.bup"
$dir = Split-path $file
$temp_dir = $dir + '\temp\'
$7zip64Path = "c:\Program Files\7-Zip\7z.exe"

$output_filename = $file + '.zip'
$temp_output_filename = $dir + '\temp\virus.decoded'
$xor_key = 0x6A  #fixed XOR key defined by McAfee

# unpack files using 7-zip (64bit version should be installed!)
write-host "[+] Unpacking $file to temp directory " -nonewline;
[Array]$keys = 'e', $file, "-o${dir}\temp"
& $7zip64Path $keys | out-null
Write-host "Done" -foregroundcolor yellow -nonewline; Write-host ".";

$file_b = [System.IO.File]::ReadAllBytes("$dir\temp\File_0") 
$xord_byte_array = New-Object Byte[] $file_b.Count

write-host "[+] Xoring..." -NoNewline;
for($i=0; $i -lt $file_b.Count ; $i++)
{
    $xord_byte_array[$i] = $file_b[$i] -bxor $xor_key
}
Write-host "Done" -foregroundcolor yellow -nonewline; Write-host ".";


# Write the XORd bytes to the temp output file
write-host "[+] writing XORed file to temp dir..." -NoNewline;
[System.IO.File]::WriteAllBytes("$temp_output_filename", $xord_byte_array)
Write-host "Done" -foregroundcolor yellow -nonewline; Write-host ".";

#archiving file with _infected_ password
[Array]$keys = 'a', $output_filename, "-tzip", '-pinfected', $temp_output_filename

write-host "[+] Archiving..." -NoNewline;
& $7zip64Path $keys | out-null
Write-host "Done" -foregroundcolor yellow -nonewline; Write-host ".";

#removing temp dir
write-host "[+] Removing temp dir..." -NoNewline;
Remove-Item $temp_dir -Force -Recurse
Write-host "Done" -foregroundcolor yellow -nonewline; Write-host ".";

# i've tried to pipe bytes directly to 7z via stdout but I failed because bytes OD OA (new line) are added to bytestream
# [System.Text.Encoding]::Default.GetString($xord_byte_array) | ."c:\Program Files\7-Zip\7z.exe" a $output_filename -tzip -sisample.txt -pinfected



write-host "[+] Saved to " -nonewline;
Write-host "$output_filename" -foregroundcolor yellow -nonewline; Write-host ".";