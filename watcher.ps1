### New-FileSystemWatcherAsynchronous

# Set the folder target
$PathToMonitor = Read-Host -Prompt 'Enter a directory path to monitor'
$Global:DestPath = Read-Host -Prompt 'Enter a directory to copy files to'

$FileSystemWatcher = New-Object System.IO.FileSystemWatcher
$FileSystemWatcher.Path  = $PathToMonitor
$FileSystemWatcher.IncludeSubdirectories = $true

# Set emits events
$FileSystemWatcher.EnableRaisingEvents = $true

# Define change actions
$Action = {
    $details = $event.SourceEventArgs
    $Name = $details.Name
    $FullPath = $details.FullPath
    $OldFullPath = $details.OldFullPath
    $OldName = $details.OldName
    $ChangeType = $details.ChangeType
    $Timestamp = $event.TimeGenerated
    $text = "{0} was {1} at {2}" -f $FullPath, $ChangeType, $Timestamp

    Write-Host $text -ForegroundColor Green

    # Define change types
    switch ($ChangeType)
    {
        'Changed' { "CHANGE"
                    Write-Host $DestPath
                    Copy-Item "$FullPath" -Destination "$DestPath" -Force -Recurse -Verbose
                  }
        'Created' { "CREATED"
                    Write-Host $DestPath
                    Copy-Item "$FullPath" -Destination "$DestPath" -Force -Recurse -Verbose
                  }
        'Deleted' { "DELETED"
                    # Set time intensive handler
                    Write-Host "Deletion Started" -ForegroundColor Gray
                    #Start-Sleep -Seconds 3    
                    Write-Warning -Message 'Deletion complete'
                  }
        'Renamed' { 
                    $text = "File {0} was renamed to {1}" -f $OldName, $Name
                    Write-Host $text -ForegroundColor Yellow
                  }
        default { Write-Host $_ -ForegroundColor Red -BackgroundColor White }
    }
}

# Set event handlers
$handlers = . {
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Changed -Action $Action -SourceIdentifier FSChange
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Created -Action $Action -SourceIdentifier FSCreate
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Deleted -Action $Action -SourceIdentifier FSDelete
    Register-ObjectEvent -InputObject $FileSystemWatcher -EventName Renamed -Action $Action -SourceIdentifier FSRename
}

Write-Host "Watching for changes to $PathToMonitor" -ForegroundColor Cyan

try
{
    do
    {
        Wait-Event -Timeout 1
        Write-Host '.' -NoNewline

    } while ($true)
}
finally
{
    # End script actions + CTRL+C executes the remove event handlers
    Unregister-Event -SourceIdentifier FSChange
    Unregister-Event -SourceIdentifier FSCreate
    Unregister-Event -SourceIdentifier FSDelete
    Unregister-Event -SourceIdentifier FSRename

    # Remaining cleanup
    $handlers | 
    Remove-Job

    $FileSystemWatcher.EnableRaisingEvents = $false
    $FileSystemWatcher.Dispose()

    Write-Warning -Message 'Event Handler completed and disabled.'
}
