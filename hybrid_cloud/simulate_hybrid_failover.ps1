# PowerShell Hybrid Cloud Failover Simulation Script
# This script demonstrates active-passive failover between Primary and Secondary clusters.

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   HYBRID CLOUD WITH AUTOMATED FAILOVER SIMULATION       " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$RouterUrl = "http://localhost:8080"
$PrimaryUrl = "http://127.0.0.1:30005"
$SecondaryUrl = "http://127.0.0.1:30006"

Write-Host "`n[Step 1] Checking Router at $RouterUrl..." -ForegroundColor Green
try {
    $res = Invoke-RestMethod -Uri "$RouterUrl/healthz" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Router responded: Pod $($res.pod) on Cluster: $($res.cluster)" -ForegroundColor Green
} catch {
    Write-Host "Router not running yet. Start it using: python hybrid_cloud/failover_router.py" -ForegroundColor Yellow
}

Write-Host "`n[Step 2] Sending 10 consecutive requests to demonstrate steady-state routing to PRIMARY cluster:" -ForegroundColor Cyan
1..10 | ForEach-Object {
    try {
        $res = Invoke-RestMethod -Uri "$RouterUrl/healthz" -TimeoutSec 2
        Write-Host "  Request #$_: Routed to -> $($res.cluster) (Pod: $($res.pod))" -ForegroundColor Gray
    } catch {
        Write-Host "  Request #$_: Failed ($($_.Exception.Message))" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 500
}

Write-Host "`n[Step 3] Simulating Primary Cluster OUTAGE..." -ForegroundColor Magenta
Write-Host "Command to simulate in Minikube / K8s:" -ForegroundColor Yellow
Write-Host "  kubectl scale deployment visitor-counter-web --replicas=0" -ForegroundColor White
Write-Host "`nWaiting 3 seconds for router health check to detect failure..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host "`n[Step 4] Sending requests during outage (Should automatically FAILOVER to Secondary):" -ForegroundColor Cyan
1..10 | ForEach-Object {
    try {
        $res = Invoke-RestMethod -Uri "$RouterUrl/healthz" -TimeoutSec 2
        Write-Host "  Request #$_: Routed to -> $($res.cluster) (Pod: $($res.pod))" -ForegroundColor Green
    } catch {
        Write-Host "  Request #$_: Failed ($($_.Exception.Message))" -ForegroundColor Red
    }
    Start-Sleep -Milliseconds 500
}

Write-Host "`n[Step 5] Simulating Recovery / Failback..." -ForegroundColor Magenta
Write-Host "Command to restore:" -ForegroundColor Yellow
Write-Host "  kubectl scale deployment visitor-counter-web --replicas=2" -ForegroundColor White
Write-Host "`nSimulation completed successfully! Take your screenshots now." -ForegroundColor Green

