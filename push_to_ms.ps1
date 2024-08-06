$ApplicationId = 'df81e5f1-abd5-49f9-9647-7827cadf0f9c'
$Organization = 'esn-tumi.de'
$CertificateThumbprint = '7616B9AFA016E508E219A6481E529C162683C8DF'

Connect-ExchangeOnline -AppId $ApplicationId -Organization $Organization -CertificateThumbprint $CertificateThumbprint

$newcontacts=Import-Csv added_contacts.csv 
    foreach($contact in $newcontacts){
        try {
            New-MailContact -Name $contact.fullName -DisplayName $contact.fullName -ExternalEmailAddress $contact.email -FirstName $contact.firstName -LastName $contact.lastName
            
            # Wartezeit einfügen, um die Replikation zu gewährleisten
            Start-Sleep -Seconds 3

            # Versuch, den Kontakt zu verstecken
            $maxRetries = 10
            $retryCount = 0
            $success = $false

            while ($retryCount -lt $maxRetries -and -not $success) {
                try {
                    
                    Set-MailContact -Identity $contact.email -HiddenFromAddressListsEnabled $true -ErrorAction Stop
                    Write-Output "Kontakt $($contact.email) wurde erfolgreich versteckt."
                    $success = $true
                } catch {
                    $retryCount++
                    Write-Output "Versuch $retryCount, Kontakt $($contact.email) zu verstecken, ist fehlgeschlagen. Wartezeit 3 Sekunden."
                    Start-Sleep -Seconds 3
                }
            }

            if (-not $success) {
                Write-Output "Kontakt $($contact.email) konnte nach $maxRetries Versuchen nicht versteckt werden."
            }
            
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
            Add-DistributionGroupMember -Identity "full.members@esn-tumi.de" -Member $contact.email -BypassSecurityGroupManagerCheck
        }
        catch {
            Write-Warning "$_"
        }
    }

$deletedfull=Import-Csv deleted_full_members.csv 
    foreach($contact in $deletedfull){
        try {
            Add-DistributionGroupMember -Identity "full.members@esn-tumi.de" -Member $contact.email -Confirm:$false -BypassSecurityGroupManagerCheck
        }
        catch {
            Write-Warning "$_"
        }
    }


$newtrial=Import-Csv added_trial_members.csv 
foreach($contact in $newtrial){
    try {
        Add-DistributionGroupMember -Identity "trial.members@esn-tumi.de" -Member $contact.email -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}

$deletedtrial=Import-Csv deleted_trial_members.csv 
foreach($contact in $deletedtrial){
    try {
        Add-DistributionGroupMember -Identity "trial.members@esn-tumi.de" -Member $contact.email -Confirm:$false -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}


$newtrial=Import-Csv added_all_members.csv 
foreach($contact in $newtrial){
    try {
        Add-DistributionGroupMember -Identity "all.members@esn-tumi.de" -Member $contact.email -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}

$deletedtrial=Import-Csv deleted_all_members.csv 
foreach($contact in $deletedtrial){
    try {
        Add-DistributionGroupMember -Identity "all.members@esn-tumi.de" -Member $contact.email -Confirm:$false -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}


$newtrial=Import-Csv added_alumni.csv 
foreach($contact in $newtrial){
    try {
        Add-DistributionGroupMember -Identity "alumni@esn-tumi.de" -Member $contact.email -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}

$deletedtrial=Import-Csv deleted_alumni.csv 
foreach($contact in $deletedtrial){
    try {
        Add-DistributionGroupMember -Identity "alumni@esn-tumi.de" -Member $contact.email -Confirm:$false -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}


$newtrial=Import-Csv added_helpers.csv 
foreach($contact in $newtrial){
    try {
        Add-DistributionGroupMember -Identity "supporters@esn-tumi.de" -Member $contact.email -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}

$deletedtrial=Import-Csv deleted_helpers.csv 
foreach($contact in $deletedtrial){
    try {
        Add-DistributionGroupMember -Identity "supporters@esn-tumi.de" -Member $contact.email -Confirm:$false -BypassSecurityGroupManagerCheck
    }
    catch {
        Write-Warning "$_"
    }
}
    