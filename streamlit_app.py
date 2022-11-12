import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
fruits_to_show = my_fruit_list.loc[fruits_selected]
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Take the json version of the reponse and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
                        
#New section to display Fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get more information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # Out to the screen as a table
    streamlit.dataframe(back_from_function)

except URLError as e:
    strealit.errror()
    
streamlit.write('The user entered ', fruit_choice)

#streamlit.text(fruityvice_response.json())

#streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):    
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#my_data_row = my_cur.fetchone()
#streamlit.header("The fruit load list contacis:")
#streamlit.dataframe(my_data_rows)

#streamlit.stop()
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
            return "Thanks for adding " + new_fruit + " to the fruit list."
        
add_my_fruit = streamlit.text_input('What fruit would you like add?')
# Add a button to add the fruit
if streamlit.button('Add a Fruit to the List'):    
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
