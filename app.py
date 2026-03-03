import streamlit as st
import os
import shutil

# UI Configuration
st.set_page_config(page_title="Fast Photo Copier", layout="centered")

# Bootstrap & Custom Styling
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .stTextArea textarea { font-family: monospace; font-size: 14px; }
        .main-card { border-radius: 15px; border: 1px solid #dee2e6; padding: 25px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .success-box { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 10px; border: 1px solid #c3e6cb; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 class="text-primary text-center mb-4">⚡ Fast Photo Copier</h2>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # --- INPUT PATH ---
    col1, col2 = st.columns(2)
    with col1:
        src_path = st.text_input("📁 Folder Sumber", placeholder="D:/Photos/Event/Raw")
    with col2:
        dest_path = st.text_input("🎯 Folder Tujuan", placeholder="D:/Photos/Event/Selection")

    st.divider()

    # --- INPUT LIST NAMA FILE ---
    st.markdown("##### 📋 Masukkan Nama File")
    file_list_raw = st.text_area("Pisahkan dengan koma, spasi, atau baris baru", height=200, 
                                 placeholder="IMG_001\nIMG_055\nIMG_123")

    # --- OPSIONAL: RAW SUPPORT ---
    include_raw = st.checkbox("Cari & Copy file RAW otomatis (.ARW, .CR2, .NEF, .DNG)", value=True)

    st.divider()

    # --- PROSES EKSEKUSI ---
    if st.button("🚀 MULAI SALIN SEKARANG"):
        if not src_path or not dest_path:
            st.error("❌ Mohon isi folder sumber dan tujuan!")
        elif not os.path.exists(src_path):
            st.error("❌ Folder Sumber tidak ditemukan!")
        else:
            # Parsing daftar nama (membersihkan spasi dan ekstensi jika user tak sengaja mengetiknya)
            names_to_find = set([n.strip().split('.')[0] for n in file_list_raw.replace('\n', ',').replace(' ', ',').split(',') if n.strip()])
            
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            all_files = os.listdir(src_path)
            raw_exts = ('.cr2', '.nef', '.arw', '.dng', '.orf', '.raf')
            
            found_count = 0
            missed_names = []
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, name in enumerate(names_to_find):
                # Cari file yang namanya sama (tanpa peduli ekstensi)
                matched_files = [f for f in all_files if f.lower().startswith(name.lower() + ".")]
                
                if matched_files:
                    for f in matched_files:
                        is_raw = f.lower().endswith(raw_exts)
                        
                        # Jika file RAW, hanya copy jika opsi dicentang
                        if is_raw and not include_raw:
                            continue
                            
                        shutil.copy(os.path.join(src_path, f), os.path.join(dest_path, f))
                    found_count += 1
                else:
                    missed_names.append(name)
                
                # Update progress
                progress_bar.progress((i + 1) / len(names_to_find))
            
            # Hasil Akhir
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.write(f"✅ **Selesai!** Berhasil menyalin **{found_count}** dari **{len(names_to_find)}** item yang diminta.")
            st.markdown('</div>', unsafe_allow_html=True)

            if missed_names:
                with st.expander("⚠️ Lihat file yang tidak ditemukan"):
                    st.write(", ".join(missed_names))
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer sederhana
st.markdown('<p class="text-center text-muted mt-3"><small>Hanya menyalin file | 100% Aman & Cepat</small></p>', unsafe_allow_html=True)