# 1. 强制当前会话的所有输入输出使用 UTF-8
$OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()

# 2. 临时设置 Git 配置，确保输出不乱码
git config --local i18n.logOutputEncoding utf-8
$env:LESSCHARSET = "utf-8"

# 获取脚本所在目录（与 merge_code.py 行为一致）
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}
$logFile = Join-Path $scriptDir "Project_Dev_Context.md"

# 3. 使用 Out-File 并明确指定 Encoding 为 utf8
"## Project Development History - $(Get-Date -Format 'yyyy-MM-dd')" | Out-File $logFile -Encoding utf8
"---" | Out-File $logFile -Append -Encoding utf8

# 提取最近 50 条记录
git log -n 100 --pretty=format:"### [%ad] %s %n* **Author:** %an %n* **Hash:** %h %n* **Files Changed:**" --date=short | Out-File $logFile -Append -Encoding utf8

# 细致的文件变更列表
git log -n 100 --name-status --pretty=format:"---%n**Date:** %ad | **Summary:** %s" --date=short | Out-File $logFile -Append -Encoding utf8

Write-Host "✅ 乱码已修复！记录已重新整理至 $logFile" -ForegroundColor Green