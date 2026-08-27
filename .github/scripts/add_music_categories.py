from __future__ import annotations

import base64
import json
import re
import zlib
from pathlib import Path

DATA = r"""c-n1P+fEzXmi?7Fc}cdkPt@INwR-o<5e|Wn4LdZK9i48ShXNN+!mhHaY&brxmbirbJwSj!Lc%rSeoL@1hKK$Y*Tqlg7kbP&SJ_0}l0(YnT5HWU=NMy-RsZ#<DdU=*kN!>j&qpnGXRlV{*cmIXrF#tRSpqj6{j5EDY4=!GR*OB=>TNr2@Gad;^w=5K&|1_(FL+$7-A!L&iHxDOW{f!g_Sl9?_v#%(Pirwfk#IG;ORF;-o~cpCy<~?@*KIv|`f(zm#S9LhR?pJi*Lts^wWqX3Go4P*w64h`Us;K)_Gddo*R5$Ct9N9zCjO}=tu^Xynnz<!P1j!AR@`v9G6`Hci8%ezZguwPre(x2C}GEWt!KLRIIX=f5-F_?k(ySwW?EXK-N(~5Wwm<KNzi4B;iimEUZDZc>rPy2NNa69NMCmkM_=#gDWebbb3i7|`<tybAx&wls=YAr+;fW_rw6bPO)Z{roNQ&u*0i1agVtd2l)vdogK`)BSgTu|Dn$CZHSHJ%hlB(o)|lQQ2{e&YT7br3vs#;-v>nIp=SMSUf-*oEj%Ctm!|BYVxETGWi_9UdC}BqJ^tEoKwY06hurUZzI@$|7!8^nil7N~$cD3KIIUYfo`~&aLa4~gUD*D36YA-W_q(&o6nTzq4XLgdJ>o%|*N1k*5MBH^{hZ&3RHY0&F>SryM&;@=^8dUn~4a)ORTC1Km-7dW|ZQ7Q?r_0Hsd0I@D@}{OERBOMR9ga>9yMlv+*=0MHscW^sZ4%{U066YbAil%2T$#1C9~sBWj-61Ijv=p>_B;z%MObOIEm~ODnlV);cBVDyGCJd?%uW-LX-%dT=arj*Ak;&5I8!ayY22|>uJ)^8M3{W6VM5dwu#3wy-MaI$#{cnF^;9bRLmC^Bdbf&?i-w4pr)?&9O(>Gbh|AcHimutzEj#*BlQbN&Q@6BcAzvGj5~z8B+Wd?P0o6cli>=EpUfKym*5mYv0N8?<SIEz61q3^7B(!R>D>DNT&vlodX*9cx2;p@gHJGh3ZTA>S#Hh9O=qXnbxYi~R5Njy9-vr~Y4UIX#3a1nU_i7x`nP)wEG8I+66&vcnWQ6jFXEl~hnbclch88o^3XHWGQJ9E@|DG`n&Q+71OzNnpF6sr`Cv01(RF=wDlQ3oC7k0l^ONDK4B{$KEOdze!=u`ER_**khpBnk+r%g|vJ*{~v6w>ODW#&PvkxCoM4jBe+fsC~34`^u3qzuPRn-Mh{T+SJ`M9U|#)uHu5&R15Xq;$`w&C0Dt1L-F)a!kLPqL@g0tKF4`I`^CD9w?n#0US2@*rA`b-+^pNmIK(DX}u4ljVh-ISV)xKp(i<y*dZm~VZ=Atm;~Lz0;%c@gH{#Rl62Y(uYOXaR@q=1widIqE>}DT#UMPjfu{`f1f_?%L|w+}MF-)ASb-8y8>8g%#+Y+X`oT^J2m}kBK=e@xn=%rH>mmoWMjucfCp;<WDH$b2jw$(yQR)osr6FvKQLAi7OY9CM#*tiE5fhqB2)Gp41Yby7^sMpl#_y)n9i<o$H1$M9km!FG3Jfw;1YJjKs1rSGGb#057^Kl<C1gt%t&p-tM5(lB)kBOfDh_R~-u`2~t?I(r&|deLXqy~mosLQP!nV`khs*2KC3LqZPK!K!`czZB`$2_S94dgT=^{;{tLGp}mT5~Ha%o2`nS_+5((naXB1qa3!a|cC=bq4pxPGeEoPvK+XFH&bR?~szhxLAv)b=U)eVB0GD|jjWmHbScTeW1yqT<&=sx{lGG9L{hYDR5lx6DH@turkYiuE+E0Qx}EVn_se3T{TPQicUYi@4TUv~~7FQd2=sYbFWdrj;K5%P-PUQE0)vG=iidjiZ{?c5+J8t6VoD9*qKPw)<tGNTOsWQZD2IZJ6uw9PHq#J_mYeCn%^SqRmd@>+{ZpnX2~T3Y(O+a02UXMr5rmIFpSuJ7ynX{GeI=syk3w(r#c&c>WS0n+9o=0{Uw`!Nf&m==E-o>Vd!fqBUl^(jDlgO7$sittpdIfG$B!_KBiVi_vL2@t*{ICKt0}2TiogtRkkVcZx5JYxM86T8e?m3WBZBDuiG$Ww-%E(Eo%mr41FSLWZPxLKc@@M)X8f=_bWHVhEQTxd5{{^fq)O+7q;u*JA_Rk1ba*)o9zj6+Nu6x+~2_03@QOT6L9SPiTb8UK6RNFPt56n=FMQ&Sq5hzlxgH8<xp^9Q?4!$a9;swbo82)8SS+Wfz?fI0`xl@ctMS57iSqmQ=)yPMus`<Za^$!I4f&*Mx#gw^CiSCeg2F71q?8u$i{x8RlGU$M3L+;@c`c876?h1Us67pt;&VY3;H_$CCC3g_8gp98=5$49Xt?Q71{TfstXVQYTN#4w{;pVs=Uig{5~yS*bO<yUlb~>W%&hmXTM0X#p*S5iLeK<5&@snp7icS2noK&UE&$t}!t($yB9A#ILCDG=R4BFFGnb@V(KtUuMisF>Bcre31FK|G(FBjdiQrP3u5Kv+n3|Q#8GaPCXVZKQ7>II}(OSR-^5zrrH8o>sDsuKkQ_OSj=ZYn2Or%WtT1UDXnNv{YjqE|CW7tNNdHUQ2s`&j~YE`&QJ?!Q7X`oW~{a+JJ695+&W%BkTk^yQ!N1R3b_A_288p6@?cc<1lkQ0fS2k0SLk8PHr1L)VmtI1oU6B$KUL^Ng%r%t)-!1nhfp~Y={<Zjs(r~NX?H93{=shGkm)M`DpHJ-U@cTHk?9aijbj*LMH#!aV@E8eGuEGVUZ4qwmY2j?$uMV39W|1s+nK@nLy4F{6cph8H5*~%nM22FPGVp6oFINRrVK!{-HUA0p$iCPAXlu^Qa(tcos7OV&~DQ|boH2RCpG@lEQTHMNoOOg)Bdzo8QoaIFyd6niZM^w3A<ZCl7z9v(B0^~*U!4p0t#A@Fx2u<3I%zYNttS^m7)O1Qkfd?205XlZ<Cpjw-?QPG@_?in5(^{-Rg(Jrd3ZBA$L^QaFy^hIZx37$kMx}oO;_`;|BxvJGz^eAk!9SQ1ZJMS8@X%(?@0&3*&Iv3xrkARO;yW+8{4V&KyV<*U$v^QRji1wa^wtQj;8=VqYJ<F|gG+)2_Vi;G>OV9)$=rOG8m0rWZH;w!_e%9;0^~5|GRzy4KpGPI0fgx}<Wt)r)SVS0NFD=@TZUv(gRPQ)xOolMSz+DE*+@)d&UZ9W1I|9#B={+AE|T*{OOPJ^@SD0jo2ey^**j2+2))wxgmX++$oZ;}7Y{si9e+PmywCSE+}5ZbrXSFM*)67F!L9r4dJXNuML>je3pa8i}sT%C)vMahU!;Md~a{1NX=8C(tEac?}RZZF-lX-uoCy<y)E|N`}cA)S_OfwAfi)TIjPLLr-aPfKWGpX|j-9qt}kn$sxy-DG=7lYd{N$PpZR!I!(5jy=W`F>hN60E-4}+zl$T+r9Dyas@Qdlr#5wjEAItpM;&%nAOT)7nVA^;tFF=n^P+Yx-Hfz?3K0p+E65(5-}r@t@WARykVEA$rqiiti(`#$>7r==b8gc)QxfO`ie}oDLu?;zr<E2(Zky~w^!k8Q5zdNTq<Y6v;}W`G>#oQODI@u=PQ#KW#qX5<SqwrQN5)S+cT?o6Z8`IiLhy^BI<kid{x7)g&CG_U$K}n-QhuJ_%laGRrJIvdVLSZ%#UEb?-oNqghiQUfX(QaA4}I~@=Df{We|e;IGezI=q&IiqZG0)^XG_ITeCzhmKi)0f+yqOT;q@tx+S%|w?3VY|=u4?M>c6?i@8#wDQhtPo44##4Z!sRL`nj+E=8`<P?62&4^XuN|42JVW8(;jht5R;jf0yThU*Gt9Z~RXSvdTN}>nKfeH|yu$`T08z|8UpKU&$&{{`$o~{_@K|@Y5p`<<%>Cy1JRwS#RfS>Gr+9e&y{J=~nq}4Ud#=KOtU@DL3G4-1xbiKR&0fxAu7K)?Rt^t-tc!8z1Fm$IoeCVY^hg=7G06!OAjExi#t!ZPHaZcIllhg!ild#)L|qH-F@R;{o2p0p{SVh0F5bB46DN`WrKRH8tj+Ey;-4C^>iI7$JYvbfw%41+sD#Obw~1yuBg6c!Df)1ovaX;2{qlKlBHdQBDM^3Qzl+87}1x<QBFQ%#Q|364QJEBlzlmH9R@PdIW{R_odv7H-5$$`F34iT|z>GuQw{;;oXFHfh~-4EE}6NWhGYc-G+a(RSA3sRSzcf;W@A3509t{csu*v1}_i{o`n+^Vew0N&tNET&jyA4pm6NX3pg$&%7s;b^|U-D_!#)=?OuBMV)>Yp;T0Ew49v_A4;)}=<OB5!?q*B5qU4AFLmKcYudeyW(-OmSc@@l=ioWk&BD!$$Tq=EwH5pYmsxsm5arkD)pV;QGZ?*tyUUOsIo0%j^fgkG^D(9dL?S5{RADP_2w58&GIKW|gr_<i{p?7{>%1udRg9_aMEZBsR;r^hc|HRwL@zwRJe}1OQkL`xVqhP-f0X~0KDoj=a8YmSn{h3W~PR+g?78%~ZVyD<|Fw6JLgS+AV21&%OWPbNPn7Rc^!c&Q5?!X_ul)Z%4o0QmZf{D{P0tDCG+W}YxN;m8L!-rYOgEw-fk^tc-<t88SVmFUm5<6I${M#jO=^RWI1P%k#-uQqw5#=!ac8wJY-FOxnay+k~itQ`td!uLN^)DiD*C>^@2;A%=e<)s1Jm4P+!=*egAD(UDBLWq%a&V45KZ2Hv2iZCwl5|d~MEV!|paT(V`z$zGP^)@x?t#H@?7+KaXqOiU!_NbyT)slUNsRIfU*!uJe?>?<KlcX;1TjG_@D!epDlvw#`fui>{t+_#?WrgM6*2~!8~!xogoJp7p9|KCB!9@j*boqjt(FT5vh;9yY+A{;zjlSE`1vmdb+7#4El?UPUPodtU=B_oAj>LWgv{Y0075C;U-eE$McXE^ETk-$S6kj78h=tST0mjT>jz31y}faKFg`r}z*U)>#IoMp1JHQ$3*Ph!$2mXfe-qA}Oq4&Y3FE(pYmC_N?S(gT6i$&y2RD1(2_q?(n+z7-D*=Y|do$OFMnX9y?PQ({GbX)@brdXEf6J>Ec7yTnV2C$AqnL#DMw2gn^NO4RY#kgW(&Tf&-ki6v#j6YqK*43mQ8+UZ+*}0fC$i+UKYrkE^L)X?da1AkZTIfilp>)dwBF7;9(=y(&8(;nT^@NG9B_t8_b0*7t<YZ4s6tWTXT!hvO#R>^_jZ3h?=Q}XUQK(adHnUKc70K`^3XP@O0-1`qi@S=Ux`}M`%qdmn(%Be9GET@2{@51j$D?PPQuffYCB=Q*;QKxKm;TB@Ve)t{<l&80$l&hze9)t&+}WJ?0AnB63&-ycKjLeZViMJZC_F(s``iEU@&;|9XTg05{3qwyW#gsWd@LzhTrPNX?#+|-`Mnzx7qs~k};wodj;<njs6S>g*7UF;IdT{<K-{>52uQLG|QX&@Z>AcI6%Eq;f1?2Wd;uwj(Fnrb#G@5T~X1rlsop;iwfE_(eNc8gm%YsUvByDPJ`*gC@s07|L&}mdlxKori0;QFSiFl^FOYr?NR&LIPeRfMX|?JUjTVQYsG9*3;^){8zSQ$vD5u2@V|5;E~apg00pO`>I!;FT%MQCIPezhDtK3Wc{u*j`?4xsev0#g20B=}nO1F05LwDiQ2!b^4o{@q6M1j)^Gjat{k&J)BL3Wugrftz?$LgTtWQZegDc(+llN{`S+x?F!={U%D%Gsu-oKtgZb+ZkuT(4Yme64aB1f?~3*JOZ#b^Lj;JV1eRh%vgSH*Ve?gP+O-LkS?3}?~Flk&j(Y70P@C3QtB+#B=`2ZO>IW{e2CJm&2$sEn1jKl&RtaFztanZaNv53z|n(cKD#raBN~)Vmt<r#4gsXzk%X3sP`#ha!|$zEr^;-rXrQQq-6X-TgD~#ee?}pQ<cK`l8l5KI%_QRS5wGdJDJSe2%ievMvfc2q-I`rt$-6LHn+%3w*f3c5rk=4*p1LUJ+k^c3Sm463?+2<cTscdZ~UFK6%4)#2V^T>T9q+r5ciG6t#pm_l&}U!Sd}VD$LG)aDFM1?7*CaAFjd=-+9R18oDY1^-tf5jt-TIyeFBK(zO0j**JAX%1@y&i+?|W9Y(!^dlsB<=GyxVGd~`R5y3u!p+o;{!C#q+`pDT_IF*l5A}q+Cc{A_S8G)E3?T7a_hAmc2cX+z%9~XW&BR#Os#l`6AZ0<oBRsiPN((Rsqx+HW_)|Tx0Lun*rZXJ4~YjnmElXX0e9#c(hWHjMd^SSVTUS^s1M!qQihiB5rV9pj+We*G92+kGCO^v|13ZmZAM`#<K?8r$#^?7#Tt0+Ee)2#oAvjJ11Ivt9FD-zR*ucC~f{fk3&z@Y9@?TH_D$y?$1PeU~S@lyHdR*9CsEFv(s>&+?G@*bA942J@GZhR3BDLyfB)Y7+b?7=bT0k4an{(d`6?i*0qE&ly>Q;rj}rTn;3Q6T{d5cvbi(OHh3-#HHlm#UsJ7~aHj3`r;8pRIbE!^+vCOhn-OHR>oV`ra}_5FG=aoGP6ESjurp5I4Z4mM#?+RmVbo{N-)$>>Pj9(S}ZB>R53{F62Qw&0pbUO7=S^P4)Y@|3=!!@Ei(*NKhCSM`>^QOK<EmeMgfQG6Hz;LJuC9JB9!A=J!<6XxGO}{^xPQ)Ph1+IQcf%pHZ?Lb^fsleE8~m4_f3;kEt^x3DxFelw)DNcf5nsvD#QEKkaXg!2Xs;L^D?>yc2#e;4L1IsU0p>mCheJ@>Q^dQ8VBp$TA<uxXA}spUPXz-tziL>3+o<IS;=n>AM6_=pg)mE(G)iVHO=%ZkDOS^E2M@N);ej0TAQwxjlMtw%||PkrQ9q^snT=HhJi;Zu;X;Eb_q*j16=EPHAZkXCC#U1U2$*xU=Pkq+J3N(c^_RaVWv!cksf$Tn=YWql1w^`6TbJE=Gh?c5Qab+Z(RJn;^xWr>a8!)l|4}9;Jiz@zG!Y`+os}jVDY"""

word_file = Path("words.js")
prefix = "window.CHARADES_CATEGORIES = "
new_categories = json.loads(zlib.decompress(base64.b85decode(DATA)).decode("utf-8"))

for category_name, songs in new_categories.items():
    if len(songs) != 300:
        raise SystemExit(f"{category_name}: expected 300 songs, found {len(songs)}")
    normalized = [re.sub(r"[^a-z0-9\u3400-\u9fff]+", "", song.casefold()) for song in songs]
    if len(normalized) != len(set(normalized)):
        raise SystemExit(f"{category_name}: duplicate songs found")

if not all(re.search(r"[\u3400-\u9fff]", song) for song in new_categories["华语音乐"]):
    raise SystemExit("Every 华语音乐 title must contain Chinese characters")

text = word_file.read_text(encoding="utf-8")
header, payload = text.split(prefix, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
untouched = {name: list(words) for name, words in categories.items() if name not in new_categories}

for name, songs in new_categories.items():
    categories[name] = songs

if {name: list(words) for name, words in categories.items() if name not in new_categories} != untouched:
    raise SystemExit("An existing category changed unexpectedly")

word_file.write_text(
    header + prefix + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Added Music and 华语音乐 with 300 songs each")
