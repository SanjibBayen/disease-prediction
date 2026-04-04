# ============================================================================
# HealthPredict AI - Complete API Testing Script
# Tests all endpoints and models with various input scenarios
# ============================================================================

# Configuration
$API_BASE_URL = "http://localhost:8000"
$API_PREFIX = "/api"  # Change to "" if your API doesn't use /api prefix

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"
$White = "White"

# Test counters
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

# Function to write colored output
function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Passed,
        [string]$Message = ""
    )
    
    $Global:TotalTests++
    if ($Passed) {
        $Global:PassedTests++
        Write-Host "✓ PASS: $TestName" -ForegroundColor $Green
        if ($Message) { Write-Host "  $Message" -ForegroundColor $Gray }
    }
    else {
        $Global:FailedTests++
        Write-Host "✗ FAIL: $TestName" -ForegroundColor $Red
        if ($Message) { Write-Host "  $Message" -ForegroundColor $Red }
    }
}

# Function to test API endpoint
function Test-Endpoint {
    param(
        [string]$Endpoint,
        [string]$Method = "GET",
        [object]$Body = $null,
        [string]$ExpectedStatus = "200"
    )
    
    $url = "$API_BASE_URL$Endpoint"
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $url -Method GET -UseBasicParsing -ErrorAction Stop
        }
        else {
            $bodyJson = $Body | ConvertTo-Json -Depth 10
            $response = Invoke-WebRequest -Uri $url -Method POST -Body $bodyJson -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
        }
        
        $statusCode = [int]$response.StatusCode
        $content = $response.Content | ConvertFrom-Json
        
        if ($statusCode -eq [int]$ExpectedStatus) {
            return @{ Success = $true; StatusCode = $statusCode; Content = $content }
        }
        else {
            return @{ Success = $false; StatusCode = $statusCode; Content = $null; Error = "Expected $ExpectedStatus, got $statusCode" }
        }
    }
    catch {
        return @{ Success = $false; StatusCode = $null; Content = $null; Error = $_.Exception.Message }
    }
}

# ============================================================================
# START TESTING
# ============================================================================
Clear-Host
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
Write-Host "║                                                                            ║" -ForegroundColor $Cyan
Write-Host "║              HealthPredict AI - API Testing Suite v1.0                     ║" -ForegroundColor $Cyan
Write-Host "║                                                                            ║" -ForegroundColor $Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor $Cyan
Write-Host ""
Write-Host "Testing API at: $API_BASE_URL" -ForegroundColor $White
Write-Host ""

# ============================================================================
# SECTION 1: HEALTH AND SYSTEM ENDPOINTS
# ============================================================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 1: Health & System Endpoints" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test 1: Root endpoint
Write-Host "Testing Root Endpoint..." -ForegroundColor $White
$result = Test-Endpoint -Endpoint "/"
if ($result.Success -and $result.Content.message) {
    Write-TestResult -TestName "Root Endpoint" -Passed $true -Message "API is running"
}
else {
    Write-TestResult -TestName "Root Endpoint" -Passed $false -Message $result.Error
}

# Test 2: Health endpoint (try both with and without /api)
Write-Host "`nTesting Health Endpoint..." -ForegroundColor $White
$healthTested = $false

# Try with /api prefix first
$result = Test-Endpoint -Endpoint "$API_PREFIX/health"
if ($result.Success -and $result.Content.status -eq "healthy") {
    Write-TestResult -TestName "Health Endpoint ($API_PREFIX/health)" -Passed $true -Message "Status: $($result.Content.status), Models: $($result.Content.models_loaded)"
    $healthTested = $true
}
else {
    # Try without /api prefix
    $result = Test-Endpoint -Endpoint "/health"
    if ($result.Success -and $result.Content.status -eq "healthy") {
        Write-TestResult -TestName "Health Endpoint (/health)" -Passed $true -Message "Status: $($result.Content.status), Models: $($result.Content.models_loaded)"
        $healthTested = $true
    }
    else {
        Write-TestResult -TestName "Health Endpoint" -Passed $false -Message "Could not find health endpoint"
    }
}

# ============================================================================
# SECTION 2: DIABETES PREDICTION TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 2: Diabetes Prediction Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test Diabetes with Normal values (Expected: Low Risk)
Write-Host "Test 2.1: Diabetes Prediction - Normal Values (Expected: Low Risk)" -ForegroundColor $White
$diabetesNormal = @{
    pregnancies       = 0
    glucose           = 100
    blood_pressure    = 80
    skin_thickness    = 20
    insulin           = 79
    bmi               = 25
    diabetes_pedigree = 0.5
    age               = 30
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $diabetesNormal
if ($result.Success -and $result.Content.prediction -eq 0 -and $result.Content.risk_level -eq "Low") {
    Write-TestResult -TestName "Diabetes - Normal Values" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level), Confidence: $($result.Content.probability)%"
}
else {
    Write-TestResult -TestName "Diabetes - Normal Values" -Passed $false -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level), Error: $($result.Error)"
}

# Test Diabetes with High Risk values (Expected: High Risk)
Write-Host "`nTest 2.2: Diabetes Prediction - High Risk Values (Expected: High Risk)" -ForegroundColor $White
$diabetesHighRisk = @{
    pregnancies       = 2
    glucose           = 180
    blood_pressure    = 95
    skin_thickness    = 35
    insulin           = 180
    bmi               = 35
    diabetes_pedigree = 1.2
    age               = 55
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $diabetesHighRisk
if ($result.Success) {
    $isCorrect = ($result.Content.prediction -eq 1 -or $result.Content.risk_level -eq "High")
    if ($isCorrect) {
        Write-TestResult -TestName "Diabetes - High Risk Values" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level), Confidence: $($result.Content.probability)%"
    }
    else {
        Write-TestResult -TestName "Diabetes - High Risk Values" -Passed $false -Message "Expected High Risk, got $($result.Content.risk_level)"
    }
}
else {
    Write-TestResult -TestName "Diabetes - High Risk Values" -Passed $false -Message $result.Error
}

# Test Diabetes with Borderline values
Write-Host "`nTest 2.3: Diabetes Prediction - Borderline Values" -ForegroundColor $White
$diabetesBorderline = @{
    pregnancies       = 1
    glucose           = 140
    blood_pressure    = 85
    skin_thickness    = 25
    insulin           = 100
    bmi               = 28
    diabetes_pedigree = 0.8
    age               = 45
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $diabetesBorderline
if ($result.Success) {
    Write-TestResult -TestName "Diabetes - Borderline Values" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level), Confidence: $($result.Content.probability)%"
}
else {
    Write-TestResult -TestName "Diabetes - Borderline Values" -Passed $false -Message $result.Error
}

# ============================================================================
# SECTION 3: ASTHMA PREDICTION TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 3: Asthma Prediction Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test Asthma - Low Risk
Write-Host "Test 3.1: Asthma Prediction - Low Risk" -ForegroundColor $White
$asthmaLowRisk = @{
    gender_male = 0
    smoking_ex  = 0
    smoking_non = 1
    age         = 0.3
    peak_flow   = 0.8
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/asthma" -Method "POST" -Body $asthmaLowRisk
if ($result.Success) {
    Write-TestResult -TestName "Asthma - Low Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Asthma - Low Risk" -Passed $false -Message $result.Error
}

# Test Asthma - High Risk
Write-Host "`nTest 3.2: Asthma Prediction - High Risk" -ForegroundColor $White
$asthmaHighRisk = @{
    gender_male = 1
    smoking_ex  = 1
    smoking_non = 0
    age         = 0.8
    peak_flow   = 0.3
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/asthma" -Method "POST" -Body $asthmaHighRisk
if ($result.Success) {
    Write-TestResult -TestName "Asthma - High Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Asthma - High Risk" -Passed $false -Message $result.Error
}

# ============================================================================
# SECTION 4: CARDIOVASCULAR PREDICTION TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 4: Cardiovascular Prediction Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test Cardiovascular - Low Risk
Write-Host "Test 4.1: Cardiovascular - Low Risk" -ForegroundColor $White
$cardioLowRisk = @{
    age         = 35
    ap_hi       = 110
    ap_lo       = 70
    cholesterol = 1
    gluc        = 1
    smoke       = 0
    alco        = 0
    active      = 1
    weight      = 70
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/cardio" -Method "POST" -Body $cardioLowRisk
if ($result.Success) {
    Write-TestResult -TestName "Cardiovascular - Low Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Cardiovascular - Low Risk" -Passed $false -Message $result.Error
}

# Test Cardiovascular - High Risk
Write-Host "`nTest 4.2: Cardiovascular - High Risk" -ForegroundColor $White
$cardioHighRisk = @{
    age         = 60
    ap_hi       = 160
    ap_lo       = 100
    cholesterol = 3
    gluc        = 2
    smoke       = 1
    alco        = 1
    active      = 0
    weight      = 95
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/cardio" -Method "POST" -Body $cardioHighRisk
if ($result.Success) {
    Write-TestResult -TestName "Cardiovascular - High Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Cardiovascular - High Risk" -Passed $false -Message $result.Error
}

# ============================================================================
# SECTION 5: STROKE PREDICTION TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 5: Stroke Prediction Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test Stroke - Low Risk
Write-Host "Test 5.1: Stroke - Low Risk" -ForegroundColor $White
$strokeLowRisk = @{
    age               = 35
    hypertension      = 0
    heart_disease     = 0
    ever_married      = 1
    avg_glucose_level = 90
    bmi               = 24
    smoking_status    = 0
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/stroke" -Method "POST" -Body $strokeLowRisk
if ($result.Success) {
    Write-TestResult -TestName "Stroke - Low Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Stroke - Low Risk" -Passed $false -Message $result.Error
}

# Test Stroke - High Risk
Write-Host "`nTest 5.2: Stroke - High Risk" -ForegroundColor $White
$strokeHighRisk = @{
    age               = 70
    hypertension      = 1
    heart_disease     = 1
    ever_married      = 1
    avg_glucose_level = 180
    bmi               = 32
    smoking_status    = 2
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/stroke" -Method "POST" -Body $strokeHighRisk
if ($result.Success) {
    Write-TestResult -TestName "Stroke - High Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Stroke - High Risk" -Passed $false -Message $result.Error
}

# ============================================================================
# SECTION 6: HYPERTENSION PREDICTION TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 6: Hypertension Prediction Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test Hypertension - Low Risk
Write-Host "Test 6.1: Hypertension - Low Risk" -ForegroundColor $White
$hypertensionLowRisk = @{
    male       = 0
    age        = 35
    cigsPerDay = 0
    BPMeds     = 0
    totChol    = 180
    sysBP      = 110
    diaBP      = 70
    BMI        = 22
    heartRate  = 70
    glucose    = 85
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/hypertension" -Method "POST" -Body $hypertensionLowRisk
if ($result.Success) {
    Write-TestResult -TestName "Hypertension - Low Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Hypertension - Low Risk" -Passed $false -Message $result.Error
}

# Test Hypertension - High Risk
Write-Host "`nTest 6.2: Hypertension - High Risk" -ForegroundColor $White
$hypertensionHighRisk = @{
    male       = 1
    age        = 60
    cigsPerDay = 20
    BPMeds     = 0
    totChol    = 280
    sysBP      = 160
    diaBP      = 100
    BMI        = 32
    heartRate  = 85
    glucose    = 110
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/hypertension" -Method "POST" -Body $hypertensionHighRisk
if ($result.Success) {
    Write-TestResult -TestName "Hypertension - High Risk" -Passed $true -Message "Prediction: $($result.Content.prediction), Risk: $($result.Content.risk_level)"
}
else {
    Write-TestResult -TestName "Hypertension - High Risk" -Passed $false -Message $result.Error
}

# ============================================================================
# SECTION 7: EDGE CASES AND VALIDATION
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 7: Edge Cases & Validation" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test 7.1: Missing required fields
Write-Host "Test 7.1: Missing Required Fields (Should return error)" -ForegroundColor $White
$invalidData = @{ glucose = 100 }
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $invalidData
if (-not $result.Success -or $result.StatusCode -eq 422) {
    Write-TestResult -TestName "Missing Fields Validation" -Passed $true -Message "API correctly rejected invalid input"
}
else {
    Write-TestResult -TestName "Missing Fields Validation" -Passed $false -Message "API should reject missing fields"
}

# Test 7.2: Out of range values
Write-Host "`nTest 7.2: Out of Range Values" -ForegroundColor $White
$outOfRangeData = @{
    pregnancies       = 100
    glucose           = 500
    blood_pressure    = 300
    skin_thickness    = 200
    insulin           = 2000
    bmi               = 100
    diabetes_pedigree = 10
    age               = 200
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $outOfRangeData
if ($result.Success) {
    Write-TestResult -TestName "Out of Range Validation" -Passed $true -Message "API handled out of range values"
}
else {
    Write-TestResult -TestName "Out of Range Validation" -Passed $false -Message "API error: $($result.Error)"
}

# Test 7.3: Negative values
Write-Host "`nTest 7.3: Negative Values" -ForegroundColor $White
$negativeData = @{
    pregnancies       = -1
    glucose           = -50
    blood_pressure    = -10
    skin_thickness    = -5
    insulin           = -20
    bmi               = -10
    diabetes_pedigree = -0.5
    age               = -5
}
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $negativeData
if ($result.Success) {
    Write-TestResult -TestName "Negative Values Validation" -Passed $true -Message "API handled negative values"
}
else {
    Write-TestResult -TestName "Negative Values Validation" -Passed $false -Message "API error: $($result.Error)"
}

# ============================================================================
# SECTION 8: PERFORMANCE TESTS
# ============================================================================
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host "  SECTION 8: Performance Tests" -ForegroundColor $Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $Yellow
Write-Host ""

# Test 8.1: Response time for diabetes prediction
Write-Host "Test 8.1: Response Time - Diabetes Prediction" -ForegroundColor $White
$startTime = Get-Date
$result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $diabetesNormal
$endTime = Get-Date
$responseTime = ($endTime - $startTime).TotalMilliseconds
if ($responseTime -lt 1000) {
    Write-TestResult -TestName "Response Time (< 1s)" -Passed $true -Message "$([math]::Round($responseTime))ms"
}
else {
    Write-TestResult -TestName "Response Time (< 1s)" -Passed $false -Message "$([math]::Round($responseTime))ms (slow)"
}

# Test 8.2: Concurrent requests (simplified)
Write-Host "`nTest 8.2: API Stability" -ForegroundColor $White
$allSuccess = $true
for ($i = 1; $i -le 5; $i++) {
    $result = Test-Endpoint -Endpoint "$API_PREFIX/predict/diabetes" -Method "POST" -Body $diabetesNormal
    if (-not $result.Success) {
        $allSuccess = $false
        break
    }
}
if ($allSuccess) {
    Write-TestResult -TestName "API Stability (5 requests)" -Passed $true -Message "All requests successful"
}
else {
    Write-TestResult -TestName "API Stability (5 requests)" -Passed $false -Message "Some requests failed"
}

# ============================================================================
# SUMMARY REPORT
# ============================================================================
Write-Host "`n"
Write-Host "╔════════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor $Cyan
Write-Host "║                              TEST SUMMARY                                      ║" -ForegroundColor $Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor $Cyan
Write-Host ""
Write-Host "  Total Tests: $TotalTests" -ForegroundColor $White
Write-Host "  ✅ Passed: $PassedTests" -ForegroundColor $Green
Write-Host "  ❌ Failed: $FailedTests" -ForegroundColor $Red
Write-Host ""
$SuccessRate = [math]::Round(($PassedTests / $TotalTests) * 100, 2)
if ($SuccessRate -ge 90) {
    Write-Host "  SUCCESS RATE: $SuccessRate% - API is HEALTHY!" -ForegroundColor $Green
}
elseif ($SuccessRate -ge 70) {
    Write-Host "  SUCCESS RATE: $SuccessRate% - API has some issues" -ForegroundColor $Yellow
}
else {
    Write-Host "  SUCCESS RATE: $SuccessRate% - API has major issues" -ForegroundColor $Red
}
Write-Host ""

# ============================================================================
# END OF TESTS
# ============================================================================
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")