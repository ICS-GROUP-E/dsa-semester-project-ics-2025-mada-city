# PowerShell script to create dsaproject directory structure

# Define the base directory
$baseDir = "dsaproject"

# Create the directory structure
$directories = @(
    "$baseDir\src\datastructures",
    "$baseDir\src\db\__pycache__",
    "$baseDir\src\models",
    "$baseDir\src\ui\__pycache__",
    "$baseDir\src\__pycache__",
    "$baseDir\test"
)

# Create each directory
foreach ($dir in $directories) {
    if (!(Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "Directory already exists: $dir" -ForegroundColor Yellow
    }
}

Write-Host "Directory structure created successfully!" -ForegroundColor Cyan