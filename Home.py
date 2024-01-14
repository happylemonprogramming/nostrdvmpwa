# Homepage
import streamlit as st
from getevent import getevent

st.set_page_config(
    page_title='Beep Boop',
    page_icon=':robot_face:'
)

# Front Page
st.title(":robot_face: AI Image Generator")
st.info('''
        Data vending machine for image generation.\n
        Enter prompt, pay lowest bidder, get content.
        ''')

user_prompt = st.text_input('Put ideas here:')
if st.button(':rocket:'):
    events = getevent(kinds=[6100])
    i = 0
    for event in events:
        i+=1
        # Get prompt
        for tag in event[1]['tags']:
            if tag[0] == 'i':
                prompt = tag[1]
        if 'http' in event[1]['content']:
            # st.text(prompt)
            st.link_button(prompt, event[1]['content'])
        if i>20:
            break

# if st.button('Donate :lightning:'):
#     st.image('lightningaddress.png')
#     st.code('lemonlemons@strike.me')