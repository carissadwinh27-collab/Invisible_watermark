import cv2
import numpy as np
import streamlit as st
from imwatermark import WatermarkEncoder, WatermarkDecoder

st.set_page_config(page_title="Watermark Digital Tersembunyi")
st.title("Watermark Digital Tersembunyi")
st.write("Sisipkan dan baca watermark tak terlihat pada foto (metode dwtDct).")
st.warning(
    "Jangan unggah foto sensitif atau milik orang lain. "
    "Simpan hasil sebagai PNG dan jangan dikirim lewat aplikasi yang mengompres foto."
)


def buka_gambar(file):
    data = np.frombuffer(file.getvalue(), np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


tab1, tab2 = st.tabs(["Sisipkan", "Baca"])

with tab1:
    file_asli = st.file_uploader("Foto asli", type=["jpg", "jpeg", "png"], key="asli")
    teks = st.text_input("Teks watermark (tepat 4 karakter)", value="ABCD", max_chars=4)

    if st.button("Sisipkan watermark"):
        if file_asli is None:
            st.error("Unggah foto dulu.")
        elif len(teks.encode("utf-8")) != 4:
            st.error("Teks watermark harus tepat 4 karakter (huruf/angka biasa).")
        else:
            bgr = buka_gambar(file_asli)
            enc = WatermarkEncoder()
            enc.set_watermark("bytes", teks.encode("utf-8"))
            hasil = enc.encode(bgr, "dwtDct")
            ok, buf = cv2.imencode(".png", hasil)
            st.session_state["hasil_png"] = buf.tobytes()
            st.session_state["hasil_rgb"] = cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB)

    if "hasil_png" in st.session_state:
        st.image(st.session_state["hasil_rgb"], caption="Hasil")
        st.download_button(
            "Unduh hasil (PNG)",
            data=st.session_state["hasil_png"],
            file_name="foto_watermark.png",
            mime="image/png",
        )

with tab2:
    file_cek = st.file_uploader("Foto yang ingin diperiksa", type=["jpg", "jpeg", "png"], key="cek")

    if st.button("Baca watermark"):
        if file_cek is None:
            st.error("Unggah foto dulu.")
        else:
            bgr = buka_gambar(file_cek)
            dec = WatermarkDecoder("bytes", 32)
            hasil = dec.decode(bgr, "dwtDct")
            st.write("Watermark yang terbaca:")
            st.code(hasil.decode("utf-8", errors="replace"))
