from pathlib import Path
import base64
import json
import re
import zlib

DATA = """c-mcA%W@;T4gD2nHaDq?T}i64$xaVj8cVhnNi)t&Dho(Wb#p|K3cD#yE0vGQB8$7oA7nQ_mII($a_-
9R7YPCf2M5qUK8&olo8+4I!=L{8VI2=<N?~7r`0a<eje$}T&Df3Tm|VoYVWPq;T+`tHr&xv1nz20|akY#an;J8Y=U`j&l<skFY{SKR^G0>$LfOQCd%VLaWmj
8VJjYa0FptUF1M$;0=e=1STvOp<V)59Tk&h8;^6S)K2Rg_?LmSLsxAS(p$JMAxu5KI_8<OXxXO==XOKVS-4>QeWWu9oe*L{{P-
dx%?L|@eX^(59FcJ`~8sXf%^n8X&n^Khb2U#}L4#1YSw_GX!PJM!$K6&*58J-?UzYB9F=jx{eX@k;}57PNJN|L50me_KVbZ;xO`V;-
n(&M_8jJtb@y;i;JTdXU&~v)Wc?N*5b!S=z)~w;soBY%;5cyocK)W_fE3d)Be-PYwaVdg9SRK?k#<P<Z+Np(va+&p90{e!6PlJ$~7GuZM6!7or0%HRNdF?L-
nCoPcofAr1~R#m}RPinGJ<hOzEK{6q)r@fg2<$Hm7&-0C+ZeynV&EAnIp-Z6eCI4n3y<Txq|XA@2`OtB8K)Cw^+qZoost=I=InCBRiy?wl-
V(Z;*$G4XG$WfRixR+1s-8ZVtoBH@8)_UH~a8%1{FQ`duID7yfHwrjgxNT!b`G9C{sM%H;{l>k=@E{b)p3Q{P4h9s0`3-
X7nab?MG|95)J^U^X*;_MddEbi2OJ>pEGuB*G(FVtUnp$cqGq;7tc_c9iw@8hmXB#-
I5~?{OWL~W8&`17QnMY^gDUKUVYt5@K`hYO90GOtt13T_aZLo&ZTR;DdrN_?J){9><XSCmoA^PoeJVXxQ!WJn4*Y#G8@ru96e5{GKV#LA02i|hJuH7Lv)sLT
nE{^xXvV#Y?W={@tqiF1s29dyRHKoTGvRmooGvUJdgM7f0uxj8Nxq3ZYLF@Gpz|Lm^4=8ltPX>&507O@rsT0?IrLB3`rP#qY1W<xmQ<D!J162s_^A@n<wIqu
eL9LmJ_jR|KJ>eu%1&*@CG73?R=_H3f9vNwT0}COSCqACkrSLn_rL`pqg`U^};`)_4WHWcUqYNkOi2b&~eO(KnH(%sbn)h>S#e{e^UvjwHQ6m5ZanEfQvSXj
JE%+=}VmsVM4F%fpr&ADCoA-`sf(o{272%N?h4QY7QYVm;ZRX1?uC3tAW!_h2rsfS0`P5&m$OCrQN1%GzR3Pnbwbffw)S}9PP-Cq(mJ~MpJspwR{LLN@S~JT
B;>#C0(<Otr5POF|$Q;h*ly>j72|$aB*d`P<k<cKWKqt793VV>80IZN0+aLcSGqfoPgaP|9nt2YSiQUR8j`}#wEpqyTio__OG6?_V#Lr)0o>{dL9tw9OPq|<
K2CiTSseV+{=GpD{K#fEUT*IVbR(ncy`QzWp_1=CLv;Y6LaPR-!(GnPu=}6D!a-
+au`tje&3)?4f0264@3fqI(3iE;zr^&^2?2Rgqv@6B#WDhOMBonNhxUTqPP>np@?NBm(vGI}`To>#ChucNlyJwx~6n(?)Kz)mzYE+X_skjE8Ft^9E_=3IfHt
(}%6zfJeo@LNL_eH<+FgcJRM-nv=HP5_NfReJ(oN}_9?vJjnHaUf^9*A1`?3(!ATX3w<S%;H~Q)3#Bdnc8?C!7&EEvE3_42)2F$^04nreUujIm+tB#7<>{$c
_mfHo|9T1b5Kvdp27E^~4a2eA-
G(Sfc0vWj38i%C**DEiz)ZJ+++oqMzm#iiI^rkDv)^6mwpo1j@!E!i&^O=3o_Q0x`Bw;c>7vT%x6#i$ZVeG#`!?Bm#)2>`4qCE9D#&0K+Uw<4VQIK9+uq=o%
;6PZE*`i!M~6N#%I4=T3nsxi4+8Q%y5g_MgVxPTzPq90+u-BIX$-9(Zq1Wsl-
H6j`_~L*&TfPZ<T#=%SL|2#njoyg8i(3;Yqvk++bLz$SE@#^41^$LCrg3;OyEA5OU%o<-
LTLTPbg!e@A~hq46>x&o@MxmdFXn6z$yvCR;v3}zLHIO7{{h`X0c2U%M4b;E)Ow5A0L`GNE~N!VYv4gSOVk8HdI)0S++Ocm-
p9|3ps(t?YB;#hvQp`cb}R4QY`zSxMl;ztmAms<>bsgu2~xw>i)I3vV<a2Q@fG)M8f$cY*|XH@qyM~dYQP@CF=O05xa#26ksy7Y&g=0Z1Qig4`Evv7<p4U28
zR)V8%@X0k(9|<@WPi5rXZOxmdzBU%39T|96DarL`1bbcmzL+g`mQ`QUf|NwzD3m_I9qTHmzT*fez_3YEW{PeIm%|7xCOTPnS|g<pjI#@B?8Cu%B!|zM*u<M
c6tJAGrL484|NqI>wcC>9Y(p+|j~CHazFQj`K5Bylpw)0S<OOyXW!J~+&4~tnMvOs)MTDZ08qW?u5l~kXm#`vs;`V|94sLqwxZ%-
9WyM7nrWyn+wWb!g@1A1YA%V;*&MeyFnN=om3?Q}4`)B2>=n}xYjH<!Mw2uwFQ;VxsXkc}=R=YOj0R-
;covfF1g5TMfw%x(_Lib^G1qooEkK>qB)Um6P2&kWFFIf!E#`85pLrKlm&c1I;<{UvN=0digKn4~}%FJETBnorpZQE(7XJpjf3sS@?^aH}gZhFf?sGL2cUb_
hEyo&d{L+8*5C>91Y>YB$zasc?Azlz7it_h+z#-
J{T+Y2i4UZFVPlMO5CI0EFx87@NSDqT>*kf<DWa_@B#)B`~5kaXXje*P_bl}pgs8I|xG3nBC+4(?tsaz&ztA3ytewA_SWdOe2hY(<x^;*RytX9xgFs(Hvjwh
WLhe1-
>r3PnF$e*DYZi;|6#>cz5~gvjSVewOeSF@G0TUvME=Q*L7Jm>Q%ATp{z2H!Rj_AeEDLnvdL}$z&jK(hPAsZ?~?GJDE9yn7;`n6aXu=vZHO?XKIgJ@jKIe%iT
#xB1vv3p{SP<MO)?|FVK9-D)73-Y{oSpF>r2+4#o7IrO~JbZcoo$4U@AOZ2*Ohs4Q`#A825G#0xoC^-Kf#m-
IaPDJwUW1TFyHG5<qO=<&E0+{g=HjXPC8S4JE~&6P>l7Y<l2_8KEWj`t+A;3N`BB~yT=NhFf$F|jU%jzU1v`<gI{NFCh@uj3)R<MpShqT?Z#EI8)SB&x9be{
b)8wGDw@wDDX6x`jJimI2*32n&64W^oT6cLeh1j5GkLHEu`jsJAM{qf@D=!gR_`;LuCkKcNkXgztQU##jA_C%+gwNyM4KciPLNaBhG6{7&KBhBXiVB-
0(+i9BQ)`YO`YRw=P`+!;!O6xMfBmJnH|NtzU9RatZz8d+^?9pWebOG1c9q*ftRM1ne@TtJTXk{%2}ZiGsYR+sJg3m*^Ab^r%mxp#;#PidqVt@NX5%zZIO!g
D0X>YOK3-
R9kC#~DfGj@0!OK+^*Vx2|p&Tt@T_rH;1XYHW|qpi8tg_Ps1#)BcTx0g7$wCFCf+XTTgBESHc9%=RNm_$V#wH@@VctiBFJYg{hERKE&)i6wGV*}p4tXH_p~@
0b<_CuBL$a&l!ysko1}D#BGYC#%{JaE|p^%P&vA9HRwE(hb<gk#|9MsLPgi!$tTZG&-
<(BqVS@AXp=Hp0^0!S?b7M(r;7W#+j0%f<ur?3ofop^g;GEI9xT*(6;HY%1eJr8`27%q??FQMzC)hke7a}(2ZP2RCkR!E@bLe-
^QiT$Rq_}0hz=D7cDi=rl@dsFU&ShwAUdisEVgtbJAuS#WqMg{6y{DS2;px`NLYq28nskthP}K7Ig3)r3Qfbrd|cR4OQd83)s-
=7*cUJcRV+0#h6t<N~6S=r5JP1)Pw*2_&YPQqNvvSNL%C(?Q`mke~ArZ3RIin{m1*sy=VnK_s1>kKbcj`=R#QKN%Fd`Tl2u%i?!Soq8fBToachJNfk%O{tMS
^va+F%X6XveuI(Oet?Jx0Fr9vDKy4s>)~!O7_e|1)lH6o@?+?F+jy-
9k%g2VD<}aLIgo2e3G$G3ZY5xU6K?XEWJhwhMty^fQl?>2pn~4H=?<CuAeGO_j7vKqK4cLCDB_pm4<h5aZ2+93DTl29*K00yOJadA$GV4@H74M%j6avx&Ra{
ABYr1Y&nzfodgn<YG*GNPEltZ}(PR*}}>(y_#fw}&-Sbbs3?f|n=V*l||-$eX+I3J8=i;pj}-}I-
kzr0D@;KqK;#TVVAYHh*E$YU#4kHpAS2{yTZxPN9y4DOfrP)b#&36lHf8nZ$fs00E~s?UUeuCDfi_f-rT?Q^MvPv`mVF%BEPRjQqIAa2t(3nh0$pAcf`J6hH
1Ds{UQ?8o&IjZj8TgOs$^>_NTVv|dxcYtn0-4YH((XYJcO7(#?~N6jrRBxE|-
TOAV*A{wjHzPK^t)>Ah}Iyv!8HwO@pa`RhXyZ&C!Bhox<nZTJ6Bd~=Ro5Y6IA?_`6%%-
1N3=#ws`V~~Kz0Lu~QqBO8x^HH#+I*yH0=?oUk#z6CfHDwQRI|#5PPizFVMUOn;#$R%3`+d#fsW%F2bvmoQ&SuVQo7T~6OR&Fn^|yW)o2GVeIdfc3Ut&$bl_
W_{)-Oh##n;X-kil`c9nEb+O=a-sEh#A$SHKVDkRW%xx*|>41huO77#}KYlKcI(c_`Fv;cD5N&PKOIJ2z^L)1tx$Iv@riBGk9>c!rDiSLGsR-
851$J?NOY*Y5v3Dz}^i%N(8zi5O|AZE<kG7nr?8EUThH=j<DPUA&~HFJA*Je@ld+VvYsx(>GkcBhqOJMbEK&+C|M)oAYnsqp?6lf*x(T^nH@Jqe;ut{-
fLt2<vWm)5-2o7j!(`r*IVfz;qT3k>n(%6H|Dr-Gxn(V{MM^+}2{=+xh_J|lZO7_z5E5i1M71C}zn8d{m|YavDp<ayR`b03FL$LF0eLi%whR5z((9VoC=a8;
Aeibp&sUl%z!H=O}>UD8N?W}EX=(_YQFGBkV=rN+gB`4Y9s)zeVd>BS^shIe_1GNuMgmx>tqrRR3zZ~y!soxaa;"""

path = Path("words.js")
text = path.read_text(encoding="utf-8")
raw = "".join(DATA.split()).encode("ascii")
celebrity = json.loads(zlib.decompress(base64.b85decode(raw)).decode("utf-8"))["Celebrity"]

normalized = [re.sub(r"[^a-z0-9]+", "", name.casefold()) for name in celebrity]
assert len(celebrity) == 500
assert len(set(normalized)) == 500
assert all(name.strip() == name and name for name in celebrity)

if '"Celebrity": [' in text:
    raise SystemExit("Celebrity category already exists")
if not text.endswith("\n};"):
    raise SystemExit("Unexpected words.js ending")

addition = ',\n  "Celebrity": ' + json.dumps(celebrity, ensure_ascii=False, indent=4).replace("\n", "\n  ") + '\n};'
text = text[:-3] + addition
path.write_text(text, encoding="utf-8")
print("Celebrity: 500 unique names (300 actors, 200 musicians)")
print("Sample:", celebrity[:20])
