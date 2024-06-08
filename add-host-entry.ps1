##**************************************************************************************
##**************************************************************************************
##**************************************************************************************
##**************************************************************************************
##************░█▀▀▄░▒█░░░░▒█▀▀█░▒█▀▀▀█░▒█▀▀▄░█▀▀▄░▒█▀▀▀█░▒█░▄▀░▒█▀▀▀░▀▀█▀▀**************
##************▒█▄▄█░▒█░░░░▒█░▄▄░▒█░░▒█░▒█▀▀▄▒█▄▄█░░▀▀▀▄▄░▒█▀▄░░▒█▀▀▀░░▒█░░**************
##************▒█░▒█░▒█▄▄█░▒█▄▄▀░▒█▄▄▄█░▒█▄▄█▒█░▒█░▒█▄▄▄█░▒█░▒█░▒█▄▄▄░░▒█░░**************
##**************************************************************************************
##************************** ▀▄▀▄▀▄GitHub - algobasket▄▀▄▀▄▀ ***************************
##**************************************************************************************
##********************************  Made By Algobasket  ********************************
##**************************************************************************************

# Function to read .env file
function Get-EnvVarsFromFile {
    param (
        [string]$envFilePath
    )
    
    $envVars = @{}
    
    if (Test-Path $envFilePath) {
        $lines = Get-Content -Path $envFilePath
        foreach ($line in $lines) {
            if ($line -match '^\s*#') { continue } # Skip comments
            if ($line -match '^\s*$') { continue } # Skip empty lines
            if ($line -match '^\s*(\w+)\s*=\s*(.+)\s*$') {
                $name = $matches[1]
                $value = $matches[2]
                $envVars[$name] = $value
            }
        }
    }
    
    return $envVars
}

# Path to .env file
$envFilePath = ".env"

# Get environment variables from .env file
$envVars = Get-EnvVarsFromFile -envFilePath $envFilePath

# Extract specific environment variables
$IP = $envVars["IP"]
$DOMAIN = $envVars["DOMAIN"]
$HOST_ENTRY = $envVars["HOST_ENTRY"]

# Path to hosts file
$hostsFile = "C:\Windows\System32\drivers\etc\hosts"

# Check if the entry already exists
if ((Get-Content $hostsFile) -notcontains $HOST_ENTRY) {
    # Add the entry to the hosts file
    Add-Content -Path $hostsFile -Value $HOST_ENTRY
    Write-Output "Entry added to hosts file."
} else {
    Write-Output "Entry already exists in hosts file."
}
