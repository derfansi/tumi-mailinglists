$ApplicationId = 'df81e5f1-abd5-49f9-9647-7827cadf0f9c'
$Organization = 'esn-tumi.de'
$CertificateThumbprint = '7616B9AFA016E508E219A6481E529C162683C8DF'

Connect-ExchangeOnline -AppId $ApplicationId -Organization $Organization -CertificateThumbprint $CertificateThumbprint

$newcontacts=Import-Csv added_contacts.csv 
    foreach($contact in $newcontacts){
        try {
            New-MailContact -Name $contact.fullName -DisplayName $contact.fullName -ExternalEmailAddress $contact.email -FirstName $contact.firstName -LastName $contact.lastName
            Set-MailContact $contact.email -HiddenFromAddressListsEnabled $true
        }
        catch {
            Write-Warning "$_"
        }
    }

$deletedcontacts=Import-Csv deleted_contacts.csv 
    foreach($contact in $deletedcontacts){
        try {
            Remove-MailContact -Identity $contact.email -Confirm:$false
        }
        catch {
            Write-Warning "$_"
        }
    }


$newfull=Import-Csv added_full_members.csv 
    foreach($contact in $newfull){
        try {
            Add-DistributionGroupMember -Identity "Staff" -Member $contact.email -BypassSecurityGroupManagerCheck
        }
        catch {
            Write-Warning "$_"
        }
    }

$deletedfull=Import-Csv deleted_full_members.csv 
    foreach($contact in $deletedfull){
        try {
            Remove-MailContact -Identity $contact.email -Confirm:$false
        }
        catch {
            Write-Warning "$_"
        }
    }


$newtrial=Import-Csv added_trial_members.csv 
foreach($contact in $newtrial){
    try {
        New-MailContact -Name $contact.fullName -DisplayName $contact.fullName -ExternalEmailAddress $contact.email -FirstName $contact.firstName -LastName $contact.lastName
        Set-MailContact $contact.email -HiddenFromAddressListsEnabled $true
    }
    catch {
        Write-Warning "$_"
    }
}

$deletedtrial=Import-Csv deleted_trial_members.csv 
foreach($contact in $deletedtrial){
    try {
        Remove-MailContact -Identity $contact.email -Confirm:$false
    }
    catch {
        Write-Warning "$_"
    }
}
    ["deleted_alumni.csv", "deleted_all_members.csv", "deleted_helpers.csv", "added_alumni.csv", "added_all_members.csv", "added_helpers.csv", "added_contacts.csv", "deleted_contacts.csv"]
    