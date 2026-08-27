from __future__ import annotations

import base64
import json
import re
import zlib
from pathlib import Path

DATA = r"""c-mc8!E)m`4*eBYUuLIjr)w|!0kWOgaqPrvdpb3}wFg*&CAKNjLs51sf7HkMhWyw(5|oqPi>pMF1n}_i0RH#W-nD8$_SAj)r~0&FXUSJi&GeMcUc0zB@l>ge4k3OlU1RN_W_&)!&#gPK4{GMFmIt-;pX1_;?JFDgLS3V69h{Ae(azNOy5souqK#3zR);2jt(~vQs(a7eQri8<WP7z`zHoAEJK+B<57wFLePQl80}Jtc+IZcm1-ISRdAU`V?k;4z_s@+d31rdNjapK9$`;q;PiosAk7QERJ8F9bvHF}gbrQtvN`qw;LC7m#v;|n)u}SC<mety|j^00afkH#AER-kBYTAg+!pC^ju57O4U)ge9vroncgTMp(c-R<cSrXBgtRi$eMYPm_l)UF5T~<-6c4R9fcidGKOs#u=Zqok~j;`QvHW7erJkG`l;unOnARk6Y)x_X8?d8y@t*beC{gp~}ck~i}48<Y`YEPk0F>a_g0J5q^?ies*>fBlEu7SUrQ7gxzQ^oOUSPZ2c1&!2B$fTI(3~s<r;{Za611@3{aJ_fF`p7|6Pui#46-I5S)Yb`O>CYaaZ5qc`e;<8l_^Q_B6nqB}<mM%{K<wUqPn#a9L?3fVsa)%_A@E@WKEN)G!B<xuk#gP0+!<MoeN#_55p$)HmM7-Sm%A&1TbFaswM%$BdxM-gfbCrS;estyrP0S@LSfsVV~BIFZ5WGb;Y>W4;<c4WICJtx9Ia%>0kE&B?zK->Oe1Zg?HeKXx^<y>`;qu)sO5C^hAZy?Ussa3Rq8$aktb_?0;>l0Qid+ZQ-qTq3u2G0$T$4ygaENnfrjm}5FoxJAYXJy`FYZ%Gt_~KHIE9T_MR@z1QJ38A3+9VubG|?3B*UZB$PzvxWh_ual^-K-BZ^c*j7Tl1>5KvU9^O<WY6sYS+Q0&6gD)@M%ZGR3iA&nghU}`ohU(Y!acn~)G4P%f1^gdI9JKF$0MZ4R0ks!G4XIA=^J%oXbYynieV`)-S%pwdnrS!mQdmP2E~*u32vy@3H1RLk{0f@wJ>Uq4M`!4wBE!N<Ny)yj<r2zTA)@?3Q0n!?F1C4lUi|=rDqcJ4U%|DS3F-i?eE5Nk43R{Qm!*p5A<tp+(iyA3FMd$F)a-Ve^B9E=`sMX7Ik`{P$qSrV~^Un>qsm113E%L3pk7Xg43iXJ=9N(EqnN^q}WCNkT-pVMy}`zgiA?SN!~Cd2H1gf*=>k>?Ls_!ki6ctEx}qA)&c~8^g*Ss67>^7cA*6u^pafHg{>LQhH$ZwJ8t$1t4DGtGP8QrRX&Cm)<w-mVtjXY8AZ?)`iaItuL;Lky%Xr#&^oEsM+)(j?Tl0<D%2bO%4*+mR^9~~0|+tZ`in*tL0B)+8@@)$4K(^m>e&abvy_<_+XP??YU0tlrR7wyh3~G+S!nN#OR%a96jC4{Rk133OUcHZ3^b>5K}e1}SL8>XgST{uedF15xo<c|e=-%l{Y8=kZQy|EMbiqDV(ej^d?5eG5D!P(E7Ya3K}n;?$4x1TFBG!L$Jjekle_7}j7~1l$9|2T28yoqg^ef$r^&;87o@sQm!yg;`tTMO7Bu8Kbw@Dp3u9REqD)>x-A)7nb!S;x_2n?ua#W!xQR)wN&3l7cF%-A=K@zpowd;L^{)H)*5fYEeQrjU5*OVfCG)VgV%Ocypu@9})=t{J64T^Rh#l{8%vdq(fL?W^JD2d|1+4AkjN1gmI;@p`_8j~2*OXs&bws?{egUvXJSO)=<CUA!lreXHN_+<~lL<84+$g1k0pM>Uxl%~@wss<28*a)T%?}`N$g+#+M=gad*fC~!rG7K-23tB^R<M@)!y)<%e;rg)@r*A(@glwiq4X9j>19{7Gu_VjkrwOkor0-0l6e3@D8la~9JsW*V8idiH&Qs#SN8jMcnQh2@hLY@t!N~BsgRY=o#Xi*K^4BJwIe;Bbg!EhdPWjn=EmGPV2mtd*I{eIow#jwZh1fZ=a-oJSrzW$r7_l&j*U~v?`0cB}YlnDICv$_3`hbDc$q<ZgQ>EUzqLzFXuoGGnV)`bo`bw+Gd!@iFmZ3Dmy3%pdAH<!1|0}jDY0+h5`5`Uu`!i-nz;NpQ7~7Kz4iAjJ!$|e;d7d5)cw`)U=?A}eP3C^;I5(Lpj4qLaM;`vK2VlN@&0wFjkYs{)%cRG&AyQC*b$_5-S&*|{|Jk#8sF5Wtg0@BQvHPPoMH4}HB=<iUAJP56hRj&+Abd$8J<F8MzU+m;cLw}RiZfCO?;<D9gE(_z_lp}R5@>KVmn$u``xPP*WYZumm7EoM9aFWW@s$w89uc~${_s55;n`+u2w|R#;LIdBbkT{zudjo8?hZ+FQZ!H^Xvl#i<l;L<PbZJG9mcZe_Etddhx~TfG)Vds^QV@l6`mF2D@-=*V@>R%331d#6gCJ%B14WWlDNNSqwx^~Tz-$RT=Nu_--ItT&UmXH!aa5EL3+<sl>UgDggW*ljE<(J2CunX(Z$8X+ZC{?CE_el7=Iy9W~{4*(un)hY?Pi<tN1YD_a+?sp*%2izVIxn-d}q&_PrE!amvx+EvsTOg)v~D+5w*+BrQCeB&oD+bXHJXpPW0Xe@ynfUvD&Le6Nb><L2S%@mCq<y0;%cE&lIsm#P2K"""

WORD_FILE = Path("words.js")
PREFIX = "window.CHARADES_CATEGORIES = "

celebrities = json.loads(zlib.decompress(base64.b85decode(DATA)).decode("utf-8"))

def normalized(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.casefold())

if len(celebrities) != 250:
    raise SystemExit(f"Expected 250 celebrities, found {len(celebrities)}")

keys = [normalized(name) for name in celebrities]
if len(keys) != len(set(keys)):
    raise SystemExit("Celebrity list contains duplicate names")

text = WORD_FILE.read_text(encoding="utf-8")
if PREFIX not in text:
    raise SystemExit("Could not find category object")

header, payload = text.split(PREFIX, 1)
payload = payload.strip()
if not payload.endswith(";"):
    raise SystemExit("Category object does not end with a semicolon")

categories = json.loads(payload[:-1])
other_categories = {name: list(words) for name, words in categories.items() if name != "Celebrity"}
categories["Celebrity"] = celebrities

if {name: list(words) for name, words in categories.items() if name != "Celebrity"} != other_categories:
    raise SystemExit("A non-Celebrity category changed unexpectedly")

WORD_FILE.write_text(
    header + PREFIX + json.dumps(categories, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)

print("Celebrity category rebuilt with 250 household names")
