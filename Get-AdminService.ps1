add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy


$body = @{"InputQuery"="Device"} | ConvertTo-Json
$runResponse = Invoke-RestMethod -ContentType "application/json" -Method 'Post' -Body  $body  -Uri "https://atlas.aperture.sci/AdminService/v1.0/Collections('PS100054')/AdminService.RunCMPivot" -UseDefaultCredentials
$runResponse.OperationId

$outputUrl = "https://atlas.aperture.sci/AdminService/v1.0/Collections('PS100054')/AdminService.CMPivotResult(OperationId=16791232)" 
iwr $outputUrl -UseDefaultCredentials
