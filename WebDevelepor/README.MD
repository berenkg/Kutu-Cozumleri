# UNKNOWNDEVICE64-V1 Kutusunun Çözümü
**Yazar:**Beren Kuday GÖRÜN
**Tarih:**10.05.2019
**IP:**192.168.171.136
**Not:**Kutunun indirme adresi 'kutu' isimli klasöre eklenmiştir.
**Flag:** /root/flag.txt'yi oku
**Sayfa:**

## 1.	Bilgi Toplama

### 1.1 IP Tespiti
```sh
root@kali:~# arp-scan -l
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.5 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.171.1	00:50:56:c0:00:08	VMware, Inc.
192.168.171.2	00:50:56:ff:0c:9c	VMware, Inc.
192.168.171.140	00:0c:29:8b:15:9e	VMware, Inc.
192.168.171.254	00:50:56:f3:88:2b	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.5: 256 hosts scanned in 2.744 seconds (93.29 hosts/sec). 4 responded
```
Hedef makinenin IP adresi 192.168.171.140


### 1.2	Servis Tespiti:
```sh
root@kali:~# nmap -p- -A 192.168.171.140
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-10 07:40 EDT
Nmap scan report for 192.168.171.140
Host is up (0.00088s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d2:ac:73:4c:17:ec:6a:82:79:87:5a:f9:22:d4:12:cb (RSA)
|   256 9c:d5:f3:2c:e2:d0:06:cc:8c:15:5a:5a:81:5b:03:3d (ECDSA)
|_  256 ab:67:56:69:27:ea:3e:3b:33:73:32:f8:ff:2e:1f:20 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 4.9.8
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Example site &#8211; Just another WordPress site
MAC Address: 00:0C:29:8B:15:9E (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.88 ms 192.168.171.140

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.08 seconds
```

80. ve 22. port açık olduğu görülmültür. 80. porta gidildiğinde internet sayfasının bir *wordpress* sayfası olduğu anlaşılmıştır. 
## 2	Zayıflık Tarama
`wpscan` aracı ile yaptığım taramalar sonucu şimdilik çok net bir şey bulamadım. Diğer yollara başvuracağım ve hiç bir şey bulamazsam buraya geri döneceğim. İlk olarak dizin keşfi yapalım.
```sh
root@kali:~# dirb http://192.168.171.140

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Fri May 10 09:02:59 2019
URL_BASE: http://192.168.171.140/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.171.140/ ----
+ http://192.168.171.140/index.php (CODE:301|SIZE:0)                                                                                                                                                              
==> DIRECTORY: http://192.168.171.140/ipdata/                                                                                                                                                                     
+ http://192.168.171.140/server-status (CODE:403|SIZE:303)                                                                                                                                                        
==> DIRECTORY: http://192.168.171.140/wp-admin/                                                                                                                                                                   
==> DIRECTORY: http://192.168.171.140/wp-content/                                                                                                                                                                 
==> DIRECTORY: http://192.168.171.140/wp-includes/                                                                                                                                                                
+ http://192.168.171.140/xmlrpc.php (CODE:405|SIZE:42)                                                                                                                                                            
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/ipdata/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/ ----
+ http://192.168.171.140/wp-admin/admin.php (CODE:302|SIZE:0)                                                                                                                                                     
==> DIRECTORY: http://192.168.171.140/wp-admin/css/                                                                                                                                                               
==> DIRECTORY: http://192.168.171.140/wp-admin/images/                                                                                                                                                            
==> DIRECTORY: http://192.168.171.140/wp-admin/includes/                                                                                                                                                          
+ http://192.168.171.140/wp-admin/index.php (CODE:302|SIZE:0)                                                                                                                                                     
==> DIRECTORY: http://192.168.171.140/wp-admin/js/                                                                                                                                                                
==> DIRECTORY: http://192.168.171.140/wp-admin/maint/                                                                                                                                                             
==> DIRECTORY: http://192.168.171.140/wp-admin/network/                                                                                                                                                           
==> DIRECTORY: http://192.168.171.140/wp-admin/user/                                                                                                                                                              
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-content/ ----
+ http://192.168.171.140/wp-content/index.php (CODE:200|SIZE:0)                                                                                                                                                   
==> DIRECTORY: http://192.168.171.140/wp-content/plugins/                                                                                                                                                         
==> DIRECTORY: http://192.168.171.140/wp-content/themes/                                                                                                                                                          
==> DIRECTORY: http://192.168.171.140/wp-content/uploads/                                                                                                                                                         
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-includes/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/css/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/images/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/includes/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/js/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/maint/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/network/ ----
+ http://192.168.171.140/wp-admin/network/admin.php (CODE:302|SIZE:0)                                                                                                                                             
+ http://192.168.171.140/wp-admin/network/index.php (CODE:302|SIZE:0)                                                                                                                                             
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-admin/user/ ----
+ http://192.168.171.140/wp-admin/user/admin.php (CODE:302|SIZE:0)                                                                                                                                                
+ http://192.168.171.140/wp-admin/user/index.php (CODE:302|SIZE:0)                                                                                                                                                
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-content/plugins/ ----
+ http://192.168.171.140/wp-content/plugins/index.php (CODE:200|SIZE:0)                                                                                                                                           
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-content/themes/ ----
+ http://192.168.171.140/wp-content/themes/index.php (CODE:200|SIZE:0)                                                                                                                                            
                                                                                                                                                                                                                  
---- Entering directory: http://192.168.171.140/wp-content/uploads/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
-----------------
END_TIME: Fri May 10 09:03:37 2019
DOWNLOADED: 32284 - FOUND: 12

```
Genelde klasörler wordpress'e ait klasörler ancak `http://192.168.171.140/ipdata/` isimli klasör biraz ilginç geldi tarayıcı üzerinden adrese gittiğimde bir `.cap` dosyası gördüm. `Wireshark` aracı ile bu dosyayı incelemeye başlayalım.

![](dosyalar/wireshark.png | width=100)




## 4	Yetki Yükseltme


### Kaynaklar:### 

