import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
#streamlit.header('Breakfast Menu')
#streamlit.text('Omega 3 & Blueberry Oatmeal')
#streamlit.text('Kale, Spinach & Rocket Smoothie')
#streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#setting index
my_fruit_list = my_fruit_list.set_index('Fruit')

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
if fruits_selected:
  #filter fruits
  fruits_to_show = my_fruit_list.loc[fruits_selected]
  streamlit.dataframe(fruits_to_show)
else:
  streamlit.dataframe(my_fruit_list)
  
streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{get_fruit_details}")
  # converting json data into flat table
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
#get fruit details
try:
  get_fruit_details = streamlit.text_input('What fruit would you like information?')
  if not get_fruit_details:
    streamlit.error('Please select a fruit to get information.')
  else:
    fruityvice_response = get_fruityvice_data(get_fruit_details)
    # converting json data into flat table
    #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # converting flat table into row-column table
    streamlit.dataframe(fruityvice_response)
except URLError as e:
  streamlit.error()
#streamlit.stop()

#taking user input
streamlit.header("The Fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
if streamlit.button('Get Fruit Load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)
  my_cnx.close()

#allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into FRUIT_LOAD_LIST values('{new_fruit}')")
    return "Thanks for adding: "+new_fruit
     
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
  my_cnx.close()
