import streamlit
import pandas

streamlit.title('My Parents New Healhy Diner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 and Blueberry oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie.')
streamlit.text(' 🐔 Jard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado on toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load List.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
fruits_to_show = my_fruits_list.loc[fruits_selected]
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

