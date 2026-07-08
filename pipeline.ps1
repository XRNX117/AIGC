param([string]$Step="all")
$env:DEEPSEEK_API_KEY=""
$env:DREAMINA_SESSION=""
$DREAMINA = Join-Path $env:USERPROFILE "bin\dreamina.exe"
$KF_DIR = "F:\aigc\Neon_Ruins_Project\01_Keyframes"
$VID_DIR = "F:\aigc\Neon_Ruins_Project\02_Video_Clips"
New-Item -ItemType Directory -Force -Path $KF_DIR, $VID_DIR | Out-Null
$SHOTS = @(
    @{id=1; name="city"; prompt="cyberpunk wasteland city skyline at dusk, ruined skyscrapers half-buried in sand, flickering neon signs, volumetric god rays, hyperdetailed, cinematic"; duration=3.0},
    @{id=2; name="hand"; prompt="cybernetic hand with glowing exoskeleton glove picking up cyan data chip from desert sand, electric sparks, shallow depth of field, cinematic lighting"; duration=3.0},
    @{id=3; name="hologram"; prompt="triptych of cracked CRT monitor with neon ad, holographic geisha projection on wall, sparking underground cables, glitch aesthetic, cyberpunk"; duration=3.0},
    @{id=4; name="megastructure"; prompt="aerial drone rising above ruined city, massive biomechanical structure buried beneath with glowing orange veins, epic scale reveal, cinematic"; duration=3.0},
    @{id=5; name="pulse"; prompt="glowing chip inserted into rusty terminal port, massive cyan shockwave expanding outward, slow motion, cyberpunk, symmetrical, dark"; duration=3.0}
)
function Invoke-Dreamina($argsList) {
    for ($attempt = 0; $attempt -lt 3; $attempt++) {
        if ($attempt -gt 0) { Start-Sleep -Seconds 3 }
        try {
            $result = & $DREAMINA @argsList 2>&1
            if ($LASTEXITCODE -eq 0 -and $result) { return $result }
        } catch { }
    }
    return $null
}
function DownloadFromJson($JsonText, $OutputDir, $ShotId) {
    try { $data = $JsonText | ConvertFrom-Json } catch { return $null }
    if ($data.gen_status -ne "success") { return $null }
    $media = $data.media_info
    $url = ""
    if ($media.video_url) { $url = $media.video_url }
    elseif ($media.image_urls) { $url = $media.image_urls[0] }
    else { $url = $data.download_url }
    if (-not $url) { return $null }
    $ext = ".png"
    if ($url -match '\.mp4') { $ext = ".mp4" }
    $out = "$OutputDir\shot_$ShotId$ext"
    try {
        Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing -TimeoutSec 120
        $size = (Get-Item $out).Length
        if ($size -gt 100) { return $out }
    } catch { }
    return $null
}
function RunKeyframes() {
    $kfs = @{}
    foreach ($s in $SHOTS) {
        $existing = Get-ChildItem $KF_DIR -Filter "shot_$($s.id).*" | Select-Object -First 1
        if ($existing) { Write-Host "Shot $($s.id): using existing $($existing.Name)"; $kfs[$s.id] = $existing.FullName; continue }
        Write-Host "`nShot $($s.id): $($s.name) text2image..."
        $result = Invoke-Dreamina @("text2image", "--prompt", $s.prompt, "--ratio", "1:1", "--resolution_type", "2k", "--generate_num", "1", "--poll", "120")
        if (-not $result) { Write-Host "  FAILED text2image" -ForegroundColor Red; continue }
        $file = DownloadFromJson $result $KF_DIR $s.id
        if (-not $file) { Write-Host "  FAILED download" -ForegroundColor Red; continue }
        $size = [math]::Round((Get-Item $file).Length / 1KB, 1)
        Write-Host "  OK: $(Split-Path $file -Leaf) ($size KB)" -ForegroundColor Green
        $kfs[$s.id] = $file
    }
    return $kfs
}
function RunVideos($kfs) {
    $vids = @{}
    foreach ($s in $SHOTS) {
        $img = $kfs[$s.id]
        if (-not $img -or -not (Test-Path $img)) { continue }
        $existing = Get-ChildItem $VID_DIR -Filter "shot_$($s.id).*" | Select-Object -First 1
        if ($existing) { Write-Host "Shot $($s.id): using existing $($existing.Name)"; $vids[$s.id] = $existing.FullName; continue }
        Write-Host "`nShot $($s.id): $($s.name) image2video..."
        $vp = "cinematic motion, slow camera push, cyberpunk atmosphere, floating dust particles, volumetric lighting"
        $result = Invoke-Dreamina @("image2video", "--image", $img, "--prompt", $vp, "--duration", "5", "--poll", "180")
        if (-not $result) { Write-Host "  FAILED image2video" -ForegroundColor Red; continue }
        $file = DownloadFromJson $result $VID_DIR $s.id
        if (-not $file) { Write-Host "  FAILED download" -ForegroundColor Red; continue }
        $size = [math]::Round((Get-Item $file).Length / 1MB, 2)
        Write-Host "  OK: $(Split-Path $file -Leaf) ($size MB)" -ForegroundColor Green
        $vids[$s.id] = $file
    }
    return $vids
}
function ComposeJson($kfs, $vids) {
    $clips = @(); foreach ($s in $SHOTS) { $clips += @{shot_id=$s.id; name=$s.name; start_time=($s.id-1)*3; duration=3.0; keyframe=$kfs[$s.id]; video_clip=$vids[$s.id] } }
    @{project="Neon_Ruins"; title="Neon Ruins"; fps=24; duration=15; clips=$clips; export=@{codec="H.264"; bitrate="15Mbps"} } | ConvertTo-Json -Depth 4 | Set-Content "F:\aigc\Neon_Ruins_Project\compose_params.json" -Encoding UTF8
    Write-Host "`ncompose_params.json saved" -ForegroundColor Cyan
}
Switch ($Step) {
    "info" { foreach ($s in $SHOTS) { Write-Host "Shot $($s.id): $($s.name) | $($s.duration)s" } }
    "keyframes" { RunKeyframes }
    "video" {
        $kfs = @{}; foreach ($s in $SHOTS) { $f = Get-ChildItem $KF_DIR -Filter "shot_$($s.id).*" | Select-Object -First 1; if ($f) { $kfs[$s.id] = $f.FullName } }
        if ($kfs.Count -eq 0) { Write-Host "No keyframes" -ForegroundColor Red; return }
        RunVideos $kfs
    }
    "all" {
        $kfs = RunKeyframes
        if ($kfs.Count -gt 0) { $vids = RunVideos $kfs; ComposeJson $kfs $vids }
        Write-Host "`n=== PIPELINE COMPLETE ===" -ForegroundColor Cyan
        Write-Host "Keyframes: $($kfs.Count)/5"
        if ($vids) { Write-Host "Videos: $($vids.Count)/$($kfs.Count)" }
        $fails = @(); foreach ($s in $SHOTS) { if (-not $kfs[$s.id]) { $fails += "Shot$($s.id)-keyframe" } }
        foreach ($s in $SHOTS) { if ($kfs[$s.id] -and (-not $vids -or -not $vids[$s.id])) { $fails += "Shot$($s.id)-video" } }
        if ($fails.Count -gt 0) { Write-Host "Failed: $($fails -join ', ')" -ForegroundColor Red }
        Write-Host "Output: F:\aigc\Neon_Ruins_Project\"
    }
}
