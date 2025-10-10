param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AllArgs = @()
)

# Set default script name
$defaultScript = "steganography.py"

# Set the venv folder name based on current folder name
$currentFolderName = Split-Path -Leaf (Get-Location)
$venvFolder = "$currentFolderName-venv"

# Handle arguments: first argument is script file, rest are script arguments
if ($AllArgs.Count -gt 0) {
    $scriptFile = $AllArgs[0]
    $scriptArgs = $AllArgs[1..($AllArgs.Count-1)]
} else {
    $scriptFile = $defaultScript
    $scriptArgs = @()
}

# Check if venv folder doesn't exist
if (-Not (Test-Path -Path $venvFolder)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvFolder
}

# Activate the virtual environment
& "$venvFolder\\Scripts\\Activate.ps1"

# If file requirements.txt is present, check and install dependencies
if (Test-Path -Path "requirements.txt") {
    Write-Host "Checking dependencies from requirements.txt..."
    
    # Get list of currently installed packages
    $installedPackages = pip list --format=freeze
    
    # Read requirements.txt and check each package
    $requirementsContent = Get-Content "requirements.txt"
    $needsInstall = $false
    
    foreach ($requirement in $requirementsContent) {
        # Skip empty lines and comments
        if ($requirement -match '^\s*$' -or $requirement -match '^\s*#') {
            continue
        }
        
        # Extract package name (handle version specifiers like ==, >=, etc.)
        $packageName = ($requirement -split '[=><]')[0].Trim()
        
        # Check if package is installed
        $isInstalled = $installedPackages | Where-Object { $_ -match "^$packageName==" }
        
        if (-not $isInstalled) {
            $needsInstall = $true
            Write-Host "Package $packageName not found, installation needed."
            break
        }
    }
    
    if ($needsInstall) {
        Write-Host "Installing missing dependencies..."
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    } else {
        Write-Host "All dependencies are already installed."
    }
}

# Clear the console
Clear-Host

# Run the script
if ($scriptArgs.Count -gt 0) {
    python $scriptFile @scriptArgs
} else {
    python $scriptFile
}

# Deactivate the virtual environment
deactivate
exit
