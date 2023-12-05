from gettext import npgettext
import streamlit as st
import function as fc
from PIL import Image


image = Image.open('./static/fabicon.png')
st.set_page_config(
    page_title = "Densuke analyzer",
    page_icon = image
)


st.title('Densuke analyzer')

url = st.text_input('伝助のURLを入力してください。')
#url = 'https://densuke.biz/list?cd=wJvhvR5fACWJVWAm'

if url:
    soup = fc.get_data_soup(url)
    names, header_items = fc.get_data_header(soup)
    st.sidebar.write(fc.get_expl(soup))
    x_undisp = st.sidebar.checkbox('× の行を表示しない')
    disp_name = st.sidebar.multiselect('表示する名前', names, default=names)
    st.sidebar.markdown('**コメント**')
    comments = fc.get_comment(soup)
    for i in range(0, len(comments), 2):
        with st.sidebar.expander(comments[i]):
            comments[i+1]
    df_sc = fc.get_data_schedule(soup, names, header_items)
    data = df_sc[disp_name]
    if x_undisp:
        data = data[disp_name and df_sc[disp_name] != '×'].dropna(how='any')
    st.table(data)  #dataframeで表示するとスマホで名前が見えなくなるため、tableにした
    st.sidebar.write('Made by Sano @20220901')
