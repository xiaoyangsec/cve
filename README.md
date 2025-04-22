# Vulnerability Title: Arbitrary File Read in QCMS (Authenticated)

Affected Version: QCMS v6.0.5

Discovery Date: April 2025

Discovered By: xiaoyang

Analysis Report:

QCMS is a PHP-based content management system widely used in Chinese websites. In version 6.0.5, a security flaw exists in the backend template editing function that allows authenticated users to read arbitrary files from the server. The vulnerability stems from insufficient validation of the `Name` parameter in the template editor interface. The parameter is directly concatenated into a file path, allowing attackers to perform directory traversal.

By manipulating the `Name` parameter, an attacker can traverse outside of the intended template directory and read any file that the PHP process has permission to access. For example, submitting a request with `Name=../../Lib/Config/Config.ini` would cause the server to return the CMS configuration file. Similar payloads can be used to access PHP source code, log files, or even system-level files such as `C:\Windows\System32\drivers\etc\hosts` on Windows.

This vulnerability requires an authenticated attacker, meaning it can only be exploited by users who are logged into the backend. However, once exploited, it can lead to severe information disclosure, exposing sensitive system files.. The vulnerability was verified in a Windows 10 environment running PHP 7.3.4 with QCMS version 6.0.5, using Firefox and Burp Suite for manual testing.

Examples of vulnerable payloads include:

- `../../Lib/Config/Config.ini` — reads the CMS config file  
- `../../System/Controller/index.php` — reads backend PHP source code  
- `../../../../../../Windows/System32/drivers/etc/hosts` — reads the Windows hosts file

The root cause lies in the backend code located in `System\Controller\admin\templates.php`, specifically the `edit_Action()` function where the `Name` parameter is used without any sanitization. The code simply does:

```php
$FilePath = PATH_TEMPLATE . $this->SysRs['TmpPath'] . '/' . trim($_GET['Name']);
$Html = file_get_contents($FilePath);
```

Exploitation: HTTP Request Examples
GET /admin/templates/edit.html?Name=../../Lib/Config/Config.ini HTTP/1.1

Host: vulnerable-website.com

Cookie:<session_cookie>

