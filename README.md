# McAfee automation tools

## McAfee ePo Python connector
This scripts & libs will allow you to communicate with McAfee ePo
### How to install
#### Python 2.7
copy libs from <libs> folder to python lib or root folder
#### Python 3.x
copy libs from <libs/Python3> to python lib or root folder. *For new scripts I don't use McAfee PYC module anymore* (i use built-in requests python module), so no additional requirements. 

## unpacking quarantine files
1. Download 7zip
2. goto c:\quarantine, un7zip .bup file
3. xor file_0 content with 0x6A or use *mcafee_unxor_bup.ps1* file
