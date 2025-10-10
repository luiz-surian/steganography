param(
    [string]$ScriptFile = "steganography.py"
)

# Set the venv folder name based on current folder name
$currentFolderName = Split-Path -Leaf (Get-Location)
$venvFolder = "$currentFolderName-venv"

# Set the script file name (can be overridden by command line argument)
$scriptFile = $ScriptFile

# Check if venv folder doesn't exist
if (-Not (Test-Path -Path $venvFolder)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvFolder
}

# Activate the virtual environment
& "$venvFolder\\Scripts\\Activate.ps1"

# If file requirements.txt is present, upgrade pip and install dependencies
if (Test-Path -Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
}

# Clear the console
Clear-Host

# Run the script
python $scriptFile

# Deactivate the virtual environment
deactivate
exit
