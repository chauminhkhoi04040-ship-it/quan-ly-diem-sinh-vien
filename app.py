import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Dữ liệu & Xử lý Pandas
# ---------------------------------------------------------
data = {
    'Họ và tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8.5, 9.0, 7.0, 9.5, 8.0, 6.5, 9.0, 7.5, 8.0, 9.5],
    'Giữa kỳ': [7.5, 8.5, 6.5, 9.0, 7.0, 5.5, 8.5, 6.5, 7.0, 9.0],
    'Cuối kỳ': [8.0, 8.5, 6.5, 9.0, 7.5, 6.0, 8.5, 7.0, 7.5, 9.0]
}

df = pd.DataFrame(data)
df['Tong_ket'] = (df['Chuyên cần'] * 0.2 + df['Giữa kỳ'] * 0.3 + df['Cuối kỳ'] * 0.5).round(2)

def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# ---------------------------------------------------------
# Giao diện Streamlit App
# ---------------------------------------------------------
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm tổng hợp")
st.dataframe(df, use_container_width=True)

# 2. Hiển thị thống kê
st.subheader("📊 Thống kê chung")
col1, col2, col3, col4 = st.columns(4)

dtb_lop = round(df['Tong_ket'].mean(), 2)
sv_cao = df.loc[df['Tong_ket'].idxmax()]
sv_thap = df.loc[df['Tong_ket'].idxmin()]
so_dat = (df['Tong_ket'] >= 5.0).sum()

col1.metric("ĐTB Lớp", dtb_lop)
col2.metric("Cao nhất", f"{sv_cao['Họ và tên']} ({sv_cao['Tong_ket']})")
col3.metric("Thấp nhất", f"{sv_thap['Họ và tên']} ({sv_thap['Tong_ket']})")
col4.metric("Số SV Đạt", f"{so_dat}/{len(df)}")

# 3. Tra cứu theo sinh viên
st.subheader("🔍 Tra cứu sinh viên")
selected_student = st.selectbox("Chọn sinh viên:", df['Họ và tên'])

student_info = df[df['Họ và tên'] == selected_student].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", student_info['Chuyên cần'])
c2.metric("Giữa kỳ", student_info['Giữa kỳ'])
c3.metric("Cuối kỳ", student_info['Cuối kỳ'])
c4.metric("Tổng kết", student_info['Tong_ket'])
c5.metric("Xếp loại", student_info['Xep_loai'])

# 4. Trực quan hóa dữ liệu
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='#4C72B0')
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.axhline(5, color='red', linestyle='--', label='Ngưỡng đạt')
ax.legend()

for i, val in enumerate(df['Tong_ket']):
    ax.text(i, val + 0.2, str(val), ha='center', va='bottom', fontsize=9)

st.pyplot(fig)

# 5. Thông tin tác giả ở chân trang
st.markdown("---")
st.caption("Người thực hiện: **[Châu Minh Khôi]** - MSSV: **[060208009485]**")
