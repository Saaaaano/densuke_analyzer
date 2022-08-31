from gettext import npgettext
import streamlit as st
import function as fc

st.title('Densuke analyzer')

url = st.text_input('伝助のURLを入力してください。')
#url = 'https://densuke.biz/list?cd=wJvhvR5fACWJVWAm'

if url:
    soup = fc.get_data_soup(url)
    names, header_items = fc.get_data_header(soup)
    # disp_mark = st.sidebar.multiselect(
    #     '表示するマーク', header_items, default=header_items)
    st.sidebar.write(fc.get_expl(soup))
    disp_name = st.sidebar.multiselect('表示する名前', names, default=names)
    st.sidebar.markdown('コメント')
    comment = fc.get_comment(soup)
    for i in comment:
        st.sidebar.write(i)
    df_sc = fc.get_data_schedule(soup, names, header_items)
    data = df_sc[disp_name]
    st.dataframe(data, height=1122)
