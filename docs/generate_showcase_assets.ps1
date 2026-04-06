Add-Type -AssemblyName System.Drawing

$ErrorActionPreference = "Stop"

$screenshotsDir = Join-Path $PSScriptRoot "screenshots"
$socialPreviewPath = Join-Path $PSScriptRoot "social-preview.png"
New-Item -ItemType Directory -Force -Path $screenshotsDir | Out-Null

function New-Color {
    param(
        [string]$Hex,
        [int]$Alpha = 255
    )

    $clean = $Hex.TrimStart("#")
    $r = [Convert]::ToInt32($clean.Substring(0, 2), 16)
    $g = [Convert]::ToInt32($clean.Substring(2, 2), 16)
    $b = [Convert]::ToInt32($clean.Substring(4, 2), 16)
    return [System.Drawing.Color]::FromArgb($Alpha, $r, $g, $b)
}

function New-RoundedPath {
    param(
        [float]$X,
        [float]$Y,
        [float]$Width,
        [float]$Height,
        [float]$Radius
    )

    $diameter = $Radius * 2
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddArc($X, $Y, $diameter, $diameter, 180, 90)
    $path.AddArc($X + $Width - $diameter, $Y, $diameter, $diameter, 270, 90)
    $path.AddArc($X + $Width - $diameter, $Y + $Height - $diameter, $diameter, $diameter, 0, 90)
    $path.AddArc($X, $Y + $Height - $diameter, $diameter, $diameter, 90, 90)
    $path.CloseFigure()
    return $path
}

function Draw-RoundedCard {
    param(
        [System.Drawing.Graphics]$Graphics,
        [float]$X,
        [float]$Y,
        [float]$Width,
        [float]$Height,
        [float]$Radius,
        [System.Drawing.Color]$FillColor,
        [System.Drawing.Color]$BorderColor,
        [float]$BorderWidth = 1
    )

    $path = New-RoundedPath -X $X -Y $Y -Width $Width -Height $Height -Radius $Radius
    $brush = New-Object System.Drawing.SolidBrush($FillColor)
    $pen = New-Object System.Drawing.Pen($BorderColor, $BorderWidth)
    $Graphics.FillPath($brush, $path)
    $Graphics.DrawPath($pen, $path)
    $brush.Dispose()
    $pen.Dispose()
    $path.Dispose()
}

function Draw-Text {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [string]$FontName,
        [float]$Size,
        [System.Drawing.FontStyle]$Style,
        [System.Drawing.Color]$Color,
        [float]$X,
        [float]$Y
    )

    $font = New-Object System.Drawing.Font($FontName, $Size, $Style, [System.Drawing.GraphicsUnit]::Pixel)
    $brush = New-Object System.Drawing.SolidBrush($Color)
    $Graphics.DrawString($Text, $font, $brush, $X, $Y)
    $brush.Dispose()
    $font.Dispose()
}

function Draw-BlockText {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [string]$FontName,
        [float]$Size,
        [System.Drawing.FontStyle]$Style,
        [System.Drawing.Color]$Color,
        [float]$X,
        [float]$Y,
        [float]$Width,
        [float]$Height
    )

    $font = New-Object System.Drawing.Font($FontName, $Size, $Style, [System.Drawing.GraphicsUnit]::Pixel)
    $brush = New-Object System.Drawing.SolidBrush($Color)
    $format = New-Object System.Drawing.StringFormat
    $format.Trimming = [System.Drawing.StringTrimming]::EllipsisWord
    $format.FormatFlags = [System.Drawing.StringFormatFlags]::LineLimit
    $Graphics.DrawString($Text, $font, $brush, [System.Drawing.RectangleF]::new($X, $Y, $Width, $Height), $format)
    $format.Dispose()
    $brush.Dispose()
    $font.Dispose()
}

function Draw-Tag {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [float]$X,
        [float]$Y,
        [float]$Width
    )

    Draw-RoundedCard -Graphics $Graphics -X $X -Y $Y -Width $Width -Height 34 -Radius 17 `
        -FillColor (New-Color "#17243d" 210) -BorderColor (New-Color "#5fa9d9" 95)
    Draw-Text -Graphics $Graphics -Text $Text -FontName "Segoe UI" -Size 15 `
        -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#eaf3ff") -X ($X + 16) -Y ($Y + 8)
}

function Draw-Metric {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Label,
        [string]$Value,
        [float]$X,
        [float]$Y,
        [float]$Width = 160
    )

    Draw-RoundedCard -Graphics $Graphics -X $X -Y $Y -Width $Width -Height 98 -Radius 24 `
        -FillColor (New-Color "#16233a" 222) -BorderColor (New-Color "#6eb8de" 75)
    Draw-Text -Graphics $Graphics -Text $Label.ToUpper() -FontName "Segoe UI" -Size 12 `
        -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#9eb6cf") -X ($X + 20) -Y ($Y + 18)
    Draw-Text -Graphics $Graphics -Text $Value -FontName "Segoe UI" -Size 28 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#eff8ff") -X ($X + 20) -Y ($Y + 42)
}

function Draw-Background {
    param(
        [System.Drawing.Graphics]$Graphics,
        [int]$Width,
        [int]$Height,
        [bool]$ShowConstellations = $true
    )

    $topRect = [System.Drawing.Rectangle]::new(0, 0, $Width, $Height)
    $backBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $topRect,
        (New-Color "#06101d"),
        (New-Color "#17294a"),
        90
    )
    $Graphics.FillRectangle($backBrush, $topRect)
    $backBrush.Dispose()

    foreach ($glow in @(
        @{ X = $Width * 0.15; Y = $Height * 0.14; W = $Width * 0.26; H = $Height * 0.22; Color = (New-Color "#7cc6ff" 36) },
        @{ X = $Width * 0.78; Y = $Height * 0.10; W = $Width * 0.24; H = $Height * 0.18; Color = (New-Color "#d8efff" 26) },
        @{ X = $Width * 0.48; Y = $Height * 0.76; W = $Width * 0.34; H = $Height * 0.24; Color = (New-Color "#62b1ff" 22) }
    )) {
        $brush = New-Object System.Drawing.SolidBrush($glow.Color)
        $Graphics.FillEllipse($brush, [float]$glow.X, [float]$glow.Y, [float]$glow.W, [float]$glow.H)
        $brush.Dispose()
    }

    foreach ($mountain in @(
        @{ Points = @([System.Drawing.PointF]::new(0, $Height * 0.50), [System.Drawing.PointF]::new($Width * 0.22, $Height * 0.36), [System.Drawing.PointF]::new($Width * 0.44, $Height * 0.56), [System.Drawing.PointF]::new($Width, $Height * 0.40), [System.Drawing.PointF]::new($Width, $Height), [System.Drawing.PointF]::new(0, $Height)); Color = (New-Color "#0e1d37" 230) },
        @{ Points = @([System.Drawing.PointF]::new(0, $Height * 0.64), [System.Drawing.PointF]::new($Width * 0.20, $Height * 0.48), [System.Drawing.PointF]::new($Width * 0.40, $Height * 0.68), [System.Drawing.PointF]::new($Width * 0.72, $Height * 0.50), [System.Drawing.PointF]::new($Width, $Height * 0.62), [System.Drawing.PointF]::new($Width, $Height), [System.Drawing.PointF]::new(0, $Height)); Color = (New-Color "#10274c" 212) },
        @{ Points = @([System.Drawing.PointF]::new(0, $Height * 0.78), [System.Drawing.PointF]::new($Width * 0.26, $Height * 0.68), [System.Drawing.PointF]::new($Width * 0.46, $Height * 0.82), [System.Drawing.PointF]::new($Width * 0.72, $Height * 0.72), [System.Drawing.PointF]::new($Width, $Height * 0.80), [System.Drawing.PointF]::new($Width, $Height), [System.Drawing.PointF]::new(0, $Height)); Color = (New-Color "#163663" 210) }
    )) {
        $brush = New-Object System.Drawing.SolidBrush($mountain.Color)
        $Graphics.FillPolygon($brush, $mountain.Points)
        $brush.Dispose()
    }

    $waterBrush = New-Object System.Drawing.SolidBrush((New-Color "#79d8ff" 22))
    $Graphics.FillRectangle($waterBrush, 0, [int]($Height * 0.89), $Width, [int]($Height * 0.11))
    $waterBrush.Dispose()

    if ($ShowConstellations) {
        $pen = New-Object System.Drawing.Pen((New-Color "#7cc0ff" 32), 2)
        foreach ($segment in @(
            @([System.Drawing.PointF]::new($Width * 0.03, $Height * 0.22), [System.Drawing.PointF]::new($Width * 0.13, $Height * 0.18), [System.Drawing.PointF]::new($Width * 0.21, $Height * 0.22), [System.Drawing.PointF]::new($Width * 0.34, $Height * 0.17)),
            @([System.Drawing.PointF]::new($Width * 0.70, $Height * 0.17), [System.Drawing.PointF]::new($Width * 0.80, $Height * 0.14), [System.Drawing.PointF]::new($Width * 0.88, $Height * 0.19), [System.Drawing.PointF]::new($Width * 0.94, $Height * 0.15))
        )) {
            $Graphics.DrawLines($pen, $segment)
            foreach ($point in $segment) {
                $starBrush = New-Object System.Drawing.SolidBrush((New-Color "#f3fbff" 130))
                $Graphics.FillEllipse($starBrush, $point.X - 4, $point.Y - 4, 8, 8)
                $starBrush.Dispose()
            }
        }
        $pen.Dispose()
    }
}

function New-Canvas {
    param(
        [int]$Width,
        [int]$Height
    )

    $bitmap = New-Object System.Drawing.Bitmap($Width, $Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    Draw-Background -Graphics $graphics -Width $Width -Height $Height
    return @{ Bitmap = $bitmap; Graphics = $graphics }
}

function Save-Canvas {
    param(
        [hashtable]$Canvas,
        [string]$Path
    )

    $Canvas.Bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
    $Canvas.Graphics.Dispose()
    $Canvas.Bitmap.Dispose()
}

function Draw-SocialPreview {
    $canvas = New-Canvas -Width 1280 -Height 640
    $g = $canvas.Graphics

    Draw-RoundedCard -Graphics $g -X 72 -Y 56 -Width 1136 -Height 92 -Radius 36 `
        -FillColor (New-Color "#121f34" 208) -BorderColor (New-Color "#80c9ff" 80)

    Draw-RoundedCard -Graphics $g -X 92 -Y 76 -Width 78 -Height 52 -Radius 26 `
        -FillColor (New-Color "#7dc8ff" 255) -BorderColor (New-Color "#d7f2ff" 140)
    Draw-Text -Graphics $g -Text "MV" -FontName "Segoe UI" -Size 24 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#071324") -X 114 -Y 87
    Draw-Text -Graphics $g -Text "MindGrid Voyager" -FontName "Segoe UI" -Size 30 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f5fbff") -X 192 -Y 82
    Draw-Text -Graphics $g -Text "Agentic travel intelligence" -FontName "Segoe UI" -Size 16 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a9c2d9") -X 194 -Y 116

    Draw-BlockText -Graphics $g `
        -Text "An agentic AI decision engine for real-world travel exploration." `
        -FontName "Segoe UI" -Size 40 -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f0fbff") `
        -X 88 -Y 192 -Width 720 -Height 172
    Draw-BlockText -Graphics $g `
        -Text "Grounded ranking, hybrid evidence retrieval, explainable recommendations, comparison mode, and local-first feedback-aware learning." `
        -FontName "Segoe UI" -Size 25 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d5e5f5") `
        -X 92 -Y 300 -Width 650 -Height 120

    Draw-RoundedCard -Graphics $g -X 808 -Y 170 -Width 384 -Height 338 -Radius 40 `
        -FillColor (New-Color "#20324b" 214) -BorderColor (New-Color "#92d8ff" 96)
    Draw-Text -Graphics $g -Text "Decision preview" -FontName "Segoe UI" -Size 16 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#8db9d8") -X 848 -Y 204
    Draw-Text -Graphics $g -Text "Tokyo" -FontName "Segoe UI" -Size 44 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f9fdff") -X 846 -Y 236
    Draw-Text -Graphics $g -Text "89.4" -FontName "Segoe UI" -Size 66 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#86d7ff") -X 846 -Y 290
    Draw-Text -Graphics $g -Text "Decision score" -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a9c2d9") -X 850 -Y 366
    Draw-Metric -Graphics $g -Label "Grounding" -Value "87%" -X 846 -Y 410 -Width 146
    Draw-Metric -Graphics $g -Label "Confidence" -Value "91%" -X 1006 -Y 410 -Width 146

    Save-Canvas -Canvas $canvas -Path $socialPreviewPath
}

function Draw-HeroOverview {
    $canvas = New-Canvas -Width 1600 -Height 900
    $g = $canvas.Graphics

    Draw-RoundedCard -Graphics $g -X 60 -Y 30 -Width 1480 -Height 86 -Radius 34 `
        -FillColor (New-Color "#16243b" 210) -BorderColor (New-Color "#7ebde7" 70)
    Draw-RoundedCard -Graphics $g -X 90 -Y 50 -Width 62 -Height 46 -Radius 20 `
        -FillColor (New-Color "#7fcfff") -BorderColor (New-Color "#eff9ff" 130)
    Draw-Text -Graphics $g -Text "MV" -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#08111c") -X 108 -Y 60
    Draw-Text -Graphics $g -Text "MindGrid Voyager" -FontName "Segoe UI" -Size 28 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f4fbff") -X 182 -Y 53
    Draw-Text -Graphics $g -Text "AGENTIC TRAVEL INTELLIGENCE" -FontName "Segoe UI" -Size 14 `
        -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#a9c2d9") -X 184 -Y 86

    Draw-Text -Graphics $g -Text "MindGrid`nVoyager" -FontName "Segoe UI" -Size 90 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#eff9ff") -X 120 -Y 170
    Draw-BlockText -Graphics $g -Text "Exploring the world through intelligent decisions." `
        -FontName "Segoe UI" -Size 26 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#dbe8f5") `
        -X 126 -Y 396 -Width 520 -Height 100
    Draw-BlockText -Graphics $g `
        -Text "A calm decision engine for destination intelligence, comparison, and explainable travel guidance." `
        -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#a8bfd5") `
        -X 128 -Y 485 -Width 580 -Height 80

    Draw-RoundedCard -Graphics $g -X 126 -Y 580 -Width 220 -Height 56 -Radius 28 `
        -FillColor (New-Color "#8edfff" 255) -BorderColor (New-Color "#dff7ff" 100)
    Draw-Text -Graphics $g -Text "Open Live Results" -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#061523") -X 156 -Y 595
    Draw-RoundedCard -Graphics $g -X 366 -Y 580 -Width 260 -Height 56 -Radius 28 `
        -FillColor (New-Color "#18273f" 222) -BorderColor (New-Color "#77bfe6" 70)
    Draw-Text -Graphics $g -Text "Compare Destinations" -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#e3eefb") -X 395 -Y 595

    foreach ($tag in @(
        @{ Text = "Agentic orchestration"; X = 126 },
        @{ Text = "Explainable reasoning"; X = 356 },
        @{ Text = "Local Python runtime"; X = 598 }
    )) {
        Draw-Tag -Graphics $g -Text $tag.Text -X $tag.X -Y 664 -Width 210
    }

    Draw-RoundedCard -Graphics $g -X 864 -Y 148 -Width 594 -Height 616 -Radius 42 `
        -FillColor (New-Color "#24364e" 212) -BorderColor (New-Color "#8edbff" 88)
    Draw-Text -Graphics $g -Text "AI PROMPT INTERFACE" -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#9ac9e6") -X 904 -Y 188
    Draw-Text -Graphics $g -Text "Start with a trip brief" -FontName "Segoe UI" -Size 56 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f9feff") -X 900 -Y 214

    foreach ($field in @(
        @{ Y = 312; H = 64; Label = "Destination"; Value = "Bangkok" },
        @{ Y = 402; H = 122; Label = "What matters most?"; Value = "food, culture, walkable, local" },
        @{ Y = 566; H = 64; Label = "Budget"; Value = "1800" },
        @{ Y = 652; H = 64; Label = "Travel style"; Value = "Balanced Explorer" }
    )) {
        Draw-Text -Graphics $g -Text $field.Label.ToUpper() -FontName "Segoe UI" -Size 12 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#aac2d8") -X 900 -Y ($field.Y - 26)
        Draw-RoundedCard -Graphics $g -X 896 -Y $field.Y -Width 524 -Height $field.H -Radius 24 `
            -FillColor (New-Color "#172435" 224) -BorderColor (New-Color "#6caed3" 55)
        Draw-Text -Graphics $g -Text $field.Value -FontName "Segoe UI" -Size 22 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#eff5ff") -X 922 -Y ($field.Y + 18)
    }

    Draw-RoundedCard -Graphics $g -X 896 -Y 740 -Width 524 -Height 68 -Radius 32 `
        -FillColor (New-Color "#8edfff" 255) -BorderColor (New-Color "#f0fbff" 110)
    Draw-Text -Graphics $g -Text "Run Decision Engine" -FontName "Segoe UI" -Size 22 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#081625") -X 1052 -Y 760

    Save-Canvas -Canvas $canvas -Path (Join-Path $screenshotsDir "hero-overview.png")
}

function Draw-RecommendationResults {
    $canvas = New-Canvas -Width 1600 -Height 900
    $g = $canvas.Graphics

    Draw-Text -Graphics $g -Text "Inspect the decision output in layers." -FontName "Segoe UI" -Size 52 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f5fbff") -X 92 -Y 72
    Draw-BlockText -Graphics $g -Text "Summary first. Evidence next. Itinerary and support details underneath." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#b3c8dd") `
        -X 96 -Y 142 -Width 620 -Height 60

    Draw-RoundedCard -Graphics $g -X 92 -Y 220 -Width 1416 -Height 214 -Radius 40 `
        -FillColor (New-Color "#1e3049" 212) -BorderColor (New-Color "#80c4f0" 82)
    Draw-Text -Graphics $g -Text "TOP RANKED DESTINATION" -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#9ab8d3") -X 130 -Y 262
    Draw-Text -Graphics $g -Text "Bali" -FontName "Segoe UI" -Size 62 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f7fdff") -X 126 -Y 286
    Draw-BlockText -Graphics $g -Text "Balanced fit across local discovery, food exploration, safety, and flexible pacing." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d4e4f4") `
        -X 132 -Y 366 -Width 540 -Height 80

    Draw-RoundedCard -Graphics $g -X 1140 -Y 256 -Width 240 -Height 52 -Radius 26 `
        -FillColor (New-Color "#1b2b43" 230) -BorderColor (New-Color "#f5c58d" 90)
    Draw-Text -Graphics $g -Text "Medium priority" -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#ffd0a0") -X 1178 -Y 270
    Draw-Text -Graphics $g -Text "87.4" -FontName "Segoe UI" -Size 74 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#87dcff") -X 1144 -Y 318
    Draw-Text -Graphics $g -Text "Decision score" -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a6bdd5") -X 1150 -Y 398

    $metricXs = @(94, 292, 490, 688, 886)
    $metricData = @(
        @{ L = "Grounding"; V = "87%" },
        @{ L = "Budget fit"; V = "90%" },
        @{ L = "Local signal"; V = "94%" },
        @{ L = "Safety"; V = "83%" },
        @{ L = "Trip style"; V = "Balanced" }
    )
    for ($i = 0; $i -lt $metricData.Count; $i++) {
        Draw-Metric -Graphics $g -Label $metricData[$i].L -Value $metricData[$i].V -X $metricXs[$i] -Y 468 -Width 180
    }

    Draw-RoundedCard -Graphics $g -X 92 -Y 598 -Width 712 -Height 238 -Radius 36 `
        -FillColor (New-Color "#1b2a42" 210) -BorderColor (New-Color "#71bbdf" 70)
    Draw-Text -Graphics $g -Text "REASONING WORKFLOW" -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a2bed7") -X 124 -Y 632
    Draw-Text -Graphics $g -Text "Discover -> Verify -> Prioritize -> Explain" -FontName "Segoe UI" -Size 28 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f2f9ff") -X 122 -Y 662
    Draw-BlockText -Graphics $g -Text "Evidence spans seeded passages, official snippets, social references, and blended score diagnostics." `
        -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#cdddfe") `
        -X 126 -Y 714 -Width 620 -Height 70

    Draw-RoundedCard -Graphics $g -X 836 -Y 598 -Width 672 -Height 238 -Radius 36 `
        -FillColor (New-Color "#1b2a42" 210) -BorderColor (New-Color "#71bbdf" 70)
    Draw-Text -Graphics $g -Text "GROUNDING & EVIDENCE" -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a2bed7") -X 870 -Y 632
    foreach ($line in @(
        "Official API snippets: 6",
        "Local seeded passages: 4",
        "Confidence calibration: active",
        "Trace: stored locally"
    )) {
        Draw-RoundedCard -Graphics $g -X 870 -Y (672 + [array]::IndexOf(@("Official API snippets: 6","Local seeded passages: 4","Confidence calibration: active","Trace: stored locally"), $line) * 38) `
            -Width 396 -Height 30 -Radius 15 -FillColor (New-Color "#17243d" 205) -BorderColor (New-Color "#6db7df" 60)
        Draw-Text -Graphics $g -Text $line -FontName "Segoe UI" -Size 16 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#e6f1ff") -X 890 -Y (679 + [array]::IndexOf(@("Official API snippets: 6","Local seeded passages: 4","Confidence calibration: active","Trace: stored locally"), $line) * 38)
    }

    Save-Canvas -Canvas $canvas -Path (Join-Path $screenshotsDir "recommendation-results.png")
}

function Draw-ComparisonMode {
    $canvas = New-Canvas -Width 1600 -Height 900
    $g = $canvas.Graphics

    Draw-Text -Graphics $g -Text "Compare destinations side by side." -FontName "Segoe UI" -Size 52 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f5fbff") -X 92 -Y 82
    Draw-BlockText -Graphics $g -Text "Ranking remains readable with score, confidence, fit, and 'best for' labels." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#b3c8dd") `
        -X 96 -Y 150 -Width 580 -Height 60

    $cards = @(
        @{ X = 92; Name = "Tokyo"; Score = "89.4"; Label = "Food exploration" },
        @{ X = 468; Name = "Bangkok"; Score = "87.1"; Label = "Budget trip" },
        @{ X = 844; Name = "Singapore"; Score = "84.8"; Label = "Safety-first" },
        @{ X = 1220; Name = "Paris"; Score = "82.3"; Label = "Premium stay" }
    )
    foreach ($card in $cards) {
        Draw-RoundedCard -Graphics $g -X $card.X -Y 244 -Width 288 -Height 358 -Radius 36 `
            -FillColor (New-Color "#1d2f49" 214) -BorderColor (New-Color "#7bc0e8" 74)
        Draw-Text -Graphics $g -Text "RANKED OPTION" -FontName "Segoe UI" -Size 13 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#9eb8cf") -X ($card.X + 30) -Y 280
        Draw-Text -Graphics $g -Text $card.Name -FontName "Segoe UI" -Size 38 -Style ([System.Drawing.FontStyle]::Bold) `
            -Color (New-Color "#f8fdff") -X ($card.X + 28) -Y 312
        Draw-Text -Graphics $g -Text $card.Score -FontName "Segoe UI" -Size 56 -Style ([System.Drawing.FontStyle]::Bold) `
            -Color (New-Color "#84dbff") -X ($card.X + 28) -Y 370
        Draw-Text -Graphics $g -Text "Decision score" -FontName "Segoe UI" -Size 17 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#aac3da") -X ($card.X + 32) -Y 444
        Draw-RoundedCard -Graphics $g -X ($card.X + 28) -Y 478 -Width 220 -Height 42 -Radius 20 `
            -FillColor (New-Color "#16243b" 230) -BorderColor (New-Color "#71b7dd" 60)
        Draw-Text -Graphics $g -Text $card.Label -FontName "Segoe UI" -Size 16 -Style ([System.Drawing.FontStyle]::Bold) `
            -Color (New-Color "#edf7ff") -X ($card.X + 50) -Y 490
        Draw-BlockText -Graphics $g -Text "Why this ranks here: strong cultural fit, credible evidence, and balanced cost-to-signal ratio." `
            -FontName "Segoe UI" -Size 15 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d6e4f3") `
            -X ($card.X + 30) -Y 540 -Width 226 -Height 68
    }

    Draw-RoundedCard -Graphics $g -X 92 -Y 648 -Width 1416 -Height 170 -Radius 36 `
        -FillColor (New-Color "#1a2941" 206) -BorderColor (New-Color "#73badf" 68)
    Draw-Text -Graphics $g -Text "REASONING DIFFERENCE MATRIX" -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#9ebbd5") -X 124 -Y 684
    Draw-BlockText -Graphics $g -Text "Budget fit, safety, local signal, trip style, and confidence stay visible without forcing a dense table layout." `
        -FontName "Segoe UI" -Size 18 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d7e4f3") `
        -X 126 -Y 720 -Width 1180 -Height 60

    Save-Canvas -Canvas $canvas -Path (Join-Path $screenshotsDir "comparison-mode.png")
}

function Draw-HistoryPanel {
    $canvas = New-Canvas -Width 1600 -Height 900
    $g = $canvas.Graphics

    Draw-Text -Graphics $g -Text "Local history restores earlier decision runs." -FontName "Segoe UI" -Size 50 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f5fbff") -X 92 -Y 84
    Draw-BlockText -Graphics $g -Text "Saved searches, top-ranked destination, average score, and one-click restore." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#b6c8dc") `
        -X 96 -Y 150 -Width 560 -Height 60

    Draw-RoundedCard -Graphics $g -X 92 -Y 250 -Width 520 -Height 520 -Radius 40 `
        -FillColor (New-Color "#1d2f49" 214) -BorderColor (New-Color "#78bee6" 76)
    Draw-Text -Graphics $g -Text "RECENT SEARCHES" -FontName "Segoe UI" -Size 15 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a3bed6") -X 128 -Y 286

    $rows = @(
        "Tokyo, Bangkok, Singapore  |  Tokyo  |  87.1",
        "Bali  |  Bali  |  86.4",
        "Paris, Dubai  |  Paris  |  84.7",
        "Goa  |  Goa  |  82.8"
    )
    for ($i = 0; $i -lt $rows.Count; $i++) {
        $y = 326 + ($i * 88)
        Draw-RoundedCard -Graphics $g -X 126 -Y $y -Width 452 -Height 66 -Radius 22 `
            -FillColor (New-Color "#152236" 220) -BorderColor (New-Color "#6eb6dd" 58)
        Draw-Text -Graphics $g -Text $rows[$i] -FontName "Segoe UI" -Size 16 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#eef7ff") -X 148 -Y ($y + 20)
    }

    Draw-RoundedCard -Graphics $g -X 668 -Y 250 -Width 840 -Height 520 -Radius 40 `
        -FillColor (New-Color "#1c2d45" 212) -BorderColor (New-Color "#78bee6" 76)
    Draw-Text -Graphics $g -Text "RESTORED RESULT SNAPSHOT" -FontName "Segoe UI" -Size 15 -Style ([System.Drawing.FontStyle]::Regular) `
        -Color (New-Color "#a3bed6") -X 708 -Y 286
    Draw-Text -Graphics $g -Text "Tokyo" -FontName "Segoe UI" -Size 56 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f8fdff") -X 706 -Y 320
    Draw-BlockText -Graphics $g -Text "Accepted for food depth, walkability, and high evidence confidence across guide signals." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d8e6f4") `
        -X 712 -Y 402 -Width 540 -Height 70
    Draw-Metric -Graphics $g -Label "Average score" -Value "87.1" -X 706 -Y 514 -Width 180
    Draw-Metric -Graphics $g -Label "Confidence" -Value "91%" -X 908 -Y 514 -Width 180
    Draw-Metric -Graphics $g -Label "Trace" -Value "saved" -X 1110 -Y 514 -Width 180

    Save-Canvas -Canvas $canvas -Path (Join-Path $screenshotsDir "history-panel.png")
}

function Draw-ArchitectureSnapshot {
    $canvas = New-Canvas -Width 1600 -Height 900
    $g = $canvas.Graphics

    Draw-Text -Graphics $g -Text "A simple view of how the AI works in MindGrid Voyager." -FontName "Segoe UI" -Size 46 `
        -Style ([System.Drawing.FontStyle]::Bold) -Color (New-Color "#f5fbff") -X 92 -Y 82
    Draw-BlockText -Graphics $g -Text "Input -> orchestration -> ranking -> grounding -> generation -> feedback refresh." `
        -FontName "Segoe UI" -Size 20 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#b5c8de") `
        -X 96 -Y 144 -Width 660 -Height 60

    $boxes = @(
        @{ X = 94; Y = 264; W = 226; H = 170; Title = "User Input"; Body = "Destination, budget, duration, interests, travel style, pace." },
        @{ X = 380; Y = 264; W = 246; H = 170; Title = "Reasoning Engine"; Body = "Perceive -> Reason -> Plan -> Act orchestration." },
        @{ X = 686; Y = 264; W = 246; H = 170; Title = "Ranking + Calibration"; Body = "Feature engineering, learned ranking, confidence fitting." },
        @{ X = 992; Y = 264; W = 246; H = 170; Title = "Grounding + Verification"; Body = "Seeded passages, official snippets, trust and recency checks." },
        @{ X = 1298; Y = 264; W = 226; H = 170; Title = "Gen-AI Layer"; Body = "Mission brief, narrative, playbook, journal draft." }
    )

    foreach ($box in $boxes) {
        Draw-RoundedCard -Graphics $g -X $box.X -Y $box.Y -Width $box.W -Height $box.H -Radius 30 `
            -FillColor (New-Color "#1d2f49" 212) -BorderColor (New-Color "#7bbfe6" 72)
        Draw-Text -Graphics $g -Text $box.Title.ToUpper() -FontName "Segoe UI" -Size 14 -Style ([System.Drawing.FontStyle]::Regular) `
            -Color (New-Color "#a5bfd7") -X ($box.X + 24) -Y ($box.Y + 26)
        Draw-BlockText -Graphics $g -Text $box.Body -FontName "Segoe UI" -Size 19 -Style ([System.Drawing.FontStyle]::Bold) `
            -Color (New-Color "#eff7ff") -X ($box.X + 24) -Y ($box.Y + 58) -Width ($box.W - 48) -Height 92
    }

    $arrowPen = New-Object System.Drawing.Pen((New-Color "#79d5ff" 140), 4)
    foreach ($segment in @(320, 626, 932, 1238)) {
        $g.DrawLine($arrowPen, $segment, 349, $segment + 50, 349)
        $g.DrawLine($arrowPen, $segment + 42, 340, $segment + 50, 349)
        $g.DrawLine($arrowPen, $segment + 42, 358, $segment + 50, 349)
    }
    $arrowPen.Dispose()

    Draw-RoundedCard -Graphics $g -X 236 -Y 556 -Width 1128 -Height 166 -Radius 34 `
        -FillColor (New-Color "#1b2b42" 208) -BorderColor (New-Color "#73bde3" 68)
    Draw-Text -Graphics $g -Text "Feedback + Replan" -FontName "Segoe UI" -Size 30 -Style ([System.Drawing.FontStyle]::Bold) `
        -Color (New-Color "#f6fbff") -X 272 -Y 588
    Draw-BlockText -Graphics $g -Text "User verdicts, natural-language replans, and live local retraining refresh the ranking and calibration artifacts for future runs." `
        -FontName "Segoe UI" -Size 21 -Style ([System.Drawing.FontStyle]::Regular) -Color (New-Color "#d3e3f2") `
        -X 272 -Y 634 -Width 1040 -Height 56

    Save-Canvas -Canvas $canvas -Path (Join-Path $screenshotsDir "architecture-snapshot.png")
}

Draw-SocialPreview
Draw-HeroOverview
Draw-RecommendationResults
Draw-ComparisonMode
Draw-HistoryPanel
Draw-ArchitectureSnapshot
