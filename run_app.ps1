# Set the venv folder name
$venvFolder = "steganography-venv"

# Set the script file name
$scriptFile = "steganography.py"

# Check if venv folder doesn't exist
if (-Not (Test-Path -Path $venvFolder)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvFolder
}

# Activate the virtual environment
& "$venvFolder\\Scripts\\Activate.ps1"

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Clear the console
Clear-Host

# Run the script
python $scriptFile

# Deactivate the virtual environment
deactivate
exit
