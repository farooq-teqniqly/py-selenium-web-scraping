param (
    [string] $tag
)

$ErrorActionPreference = "Stop"
$dockerFile = "./Dockerfile"
$companyName = "teqniqly"
$appName = "wineratingscollector"

$withTag = "$companyName/$appName"

if (-not [string]::IsNullOrEmpty($tag))
{
    $withTag = "${withTag}:${tag}"
}

Write-Host @"

                        ##         .
                  ## ## ##        ==
               ## ## ## ##       ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/

        Building docker image
        Path: $dockerFile
        Tag: $withTag

"@

docker build `
-f ./Dockerfile `
--no-cache `
-t $withTag `
.
