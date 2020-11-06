import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from pymongo import MongoClient
import base64
import dnspython
s = "bW9uZ29kYitzcnY6Ly9ndWVzdDpndWVzdEBsaXN0aW5ncy5ncnU0ci5tb25nb2RiLm5ldC9idXNpbmVzcz9yZXRyeVdyaXRlcz10cnVlJnc9bWFqb3JpdHk="
client = MongoClient(base64.b64decode(s.encode('ascii')).decode('ascii'))
db = client.business

st.sidebar.title('Hey there!')
st.sidebar.header('Quick webpage info')
explanation = st.sidebar.beta_expander("What's the point?", True)
explanation.write("Finding subleases is a pain. I didn't like looking through Facebook pages and I assumed more people didn't either. So now you can put your sublease information in here, and easily search/filter for certain standardzed information.")
how = st.sidebar.beta_expander("How does it work?", True)
how.write("First decide what action you want to do; advertise your sublease, delete your sublease listing, or find an apartment. To add a listing, simply fill out the fields and press the button. To delete one, enter your secret key and again, press the button. To find an apartment, use the different input methods to set the key filtering information  and then simply click the button to display all the subleases that match your criteria. (Once you have the table, you can sort by clicking on any column heading.)")

value = ''
add_apt = st.beta_expander("Add a Listing")
add_apt.header('Fill out the fields.')
add_apt.subheader('Leaser Information')
left, middle, right = add_apt.beta_columns(3)
name = left.text_input('Name')
phone = middle.text_input('Number')
email = right.text_input('Email')
password = add_apt.text_input('Secret Key (for deleting listings)', type='password')
add_apt.subheader('Apartment Information')
left, right = add_apt.beta_columns([3, 1])
address = left.text_input('Address')
apt = right.text_input('Apt/Bldg/Etc')
leftequal, rightequal = add_apt.beta_columns(2)
complex = leftequal.text_input('Complex Name')
semester = rightequal.multiselect(
'Semester(s) available',
['Spring 2021', 'Summer 2021', 'Fall 2021', 'Spring 2022'])
lleft, lmid, rmid, rright = add_apt.beta_columns(4)
cost = lleft.number_input('Cost', 100, 2000, 100, 1)
bed = lmid.number_input('Bedrooms', 1, 7, 1, 1)
bath = rmid.number_input('Bathrooms', 1, 7, 1, 1)
util = rright.selectbox(
'Are utilities included?',
('Yes', 'No'))

listing = {
		'Leaser Name' : name,
		'Phone' : phone,
		'Email' : email,
		'Address 1' : address,
		'Address 2' : apt,
		'Semester' : semester,
		'Complex' : complex,
		'Bedrooms' : bed,
		'Bathrooms' : bath,
		'Cost' : cost,
		'Utilities' : util,
        'key': password
}
if add_apt.button('Send information'):
    obj = db.listings.insert_one(listing)
    st.success('Your listing has been added!')


del_apt = st.beta_expander("Delete a Listing")
passw = del_apt.text_input('Secret Key', type='password')
if del_apt.button('Delete your listing'):
    result = db.listings.delete_many({"key": passw})



view_apt = st.beta_expander("Find an Apartment", True)

view_apt.header('Choose your filters:')



all_listings = db.listings.find({})

leasers = []
phones = []
emails = []
add1 = []
add2 = []
semesters = []
complexes = []
bedrooms = []
bathrooms = []
costs = []
utilities = []


cost_filter = view_apt.slider('Select your price range',100, 1500, (500, 900))
left_column, right_column = view_apt.beta_columns(2)

bed_filter = left_column.slider('Select bedroom range', 1, 7, (2, 5))
bath_filter = right_column.slider('Select bathroom range', 1, 7, (2, 5))
utilities_filter = view_apt.checkbox('Utilities included?')
if utilities_filter:
	utilities_filter = "yes"
else:
	utilities_filter = "no"
complex_filter = title = view_apt.text_input('Apartment name, leave blank otherwise')

if view_apt.button("Find apartments!"):
	with st.spinner('Filtering out your apartments!'):
		for listing in all_listings:
			if listing['Cost'] >= cost_filter[0] and listing['Cost'] <= cost_filter[1]:
				if listing['Bedrooms'] >= bed_filter[0] and listing['Bedrooms'] <= bed_filter[1]:
					if listing['Bathrooms'] >= bath_filter[0] and listing['Bathrooms'] <= bath_filter[1]:
						if listing['Utilities'].lower() == utilities_filter:
							if complex_filter.lower() in listing['Complex'].lower():
								leasers.append(listing['Leaser Name'])
								phones.append(listing['Phone'])
								emails.append(listing['Email'])
								add1.append(listing['Address 1'])
								add2.append(listing['Address 2'])
								semesters.append(listing['Semester'])
								complexes.append(listing['Complex'])
								bedrooms.append(listing['Bedrooms'])
								bathrooms.append(listing['Bathrooms'])
								costs.append(listing['Cost'])
								utilities.append(listing['Utilities'])
	view_apt.write(pd.DataFrame({
		'Leaser Name': leasers,
		'Phone': phones,
		'Email': emails,
		'Address 1': add1,
		'Address 2': add2,
		'Semester': semesters,
		'Complex': complexes,
		'Bedrooms': bedrooms,
		'Bathrooms': bathrooms,
		'Cost': costs,
		'Utilities': utilities
		}))
