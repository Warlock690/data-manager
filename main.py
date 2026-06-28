import streamlit as st
import socket
import requests





st.set_page_config(
    page_title="megagigawhat",
    page_icon="gemini.jpg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
.css-1rs6os {visibility: hidden;}
.css-18e3th9 {padding-top: 0rem;}
.css-1d391kg {padding-top: 0rem;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




def sure_hesapla(hiz_mbit, transfer_tb):
    if hiz_mbit is None or hiz_mbit == 0:
        return "Hata: İnternet hızı 0 olamaz."
    if transfer_tb is None or transfer_tb < 0:
        return "Hata: Transfer miktarı negatif olamaz."

    toplam_mb = transfer_tb * 1_000_000
    sure_saniye = toplam_mb / (hiz_mbit / 8)
    sure_saat = sure_saniye / 3600

    gun = int(sure_saat // 24)
    saat = sure_saat % 24

    return f"{gun} gün {saat:.2f} saat"


def yerel_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def genel_ip():
    return requests.get("https://ipinfo.io/ip").text


def ip_bilgisi(ip):
    apis = [
        f"https://ipinfo.io/{ip}/json",
        f"https://ipapi.co/{ip}/json/",
        f"http://ip-api.com/json/{ip}"
    ]

    veri = {}

    for url in apis:
        try:
            r = requests.get(url, timeout=5).json()
            if r and ("city" in r or "country" in r or "region" in r):
                veri = r
                break
        except:
            continue

    return f"""
Ülke        : {veri.get("country") or veri.get("country_name")}
Şehir       : {veri.get("city")}
Posta Kodu  : {veri.get("postal")}
Saat Dilimi : {veri.get("timezone")}
ISP         : {veri.get("org") or veri.get("isp")}
"""


def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return f"{domain} → {ip}"
    except:
        return "Geçersiz domain veya çözümlenemedi"









st.title("megagigawhat")

tab1, tab2, tab3 ,tab4 = st.tabs([
    "transfer time calculate",
    "IP Tracker",
    "DNS Lookup",
    "abaut developer"
])


with tab1:
    hiz = st.number_input("İnternet Hızı (Mbit)", min_value=0)
    tb = st.number_input("Transfer Miktarı (TB)", min_value=0.0)

    if st.button("Hesapla"):
        st.success(sure_hesapla(hiz, tb))



with tab2:
    if st.button("IP Bilgilerini Getir"):
        local = yerel_ip()
        public = genel_ip()
        info = ip_bilgisi(public)

        st.write("**Yerel IP:**", local)
        st.write("**Genel IP:**", public)
        st.text(info)


with tab3:
    domain = st.text_input("Domain (örnek: google.com)")

    if st.button("Çöz"):
        st.write(dns_lookup(domain))



with tab4:
    st.header("About developer")
    st.markdown("This site developed by **Mercan Olcek**.")
    st.markdown("Github: [https://github.com/Warlock690](https://github.com/Warlock690)")
    st.markdown("Gitlab: [https://gitlab.com/Warlock690](https://gitlab.com/Warlock690)")
    st.markdown("Netdev:[https://books.netdev.com.tr/user/warlock]")
    st.image("mercan.jpg", width=400)
