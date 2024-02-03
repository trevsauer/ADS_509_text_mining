import streamlit as st
import pandas as pd
import numpy as np
import ast

st.title("arXiv.org Summarizer")
st.write("This app provides a summary of arXiv.org preprint activity in the subdomain of your choice")


tab1, tab2, tab3 = st.tabs(['User Input', 'Summary', 'Papers'])

################################################################
#### USER SELECTION OF CATEGORIES ##############################
################################################################

field_choice = tab1.selectbox(
	"Please select a field:",
	('Math','Physics'))

category_dict = {
	"Math" : { "None": "none",
				"Number Theory (math.NT)": "math.NT",
				"Mathematical Physics (math.MP)": "math.MP"},
	"Physics" : { "None ": "none",
				"Astrophysics of Galaxies (astro-ph.GA)": "astro-ph.GA",
				"Mathematical Physics (math-PH)": "math-PH"}
}


category_choice = tab1.selectbox(
	"Choose a category:", category_dict[field_choice].keys())


subcategory = " ".join(category_choice.split()[:-1])

tab1.write(f"You have chosen the {field_choice} field: {subcategory}")

#st.write(category_dict[field_choice][category_choice])
tab1.markdown('**Choose a date range**')

tab1.radio("Number of Days",['180 days','90 days', '30 days', '7 days'])
tab1.date_input("Choose a starting date", format="YYYY-MM-DD")


tab1.button("Pull arXiv.org info")
st.divider()


################################################################
#### ARXIV API QUERY        ####################################
################################################################

#temporary example
df = pd.read_csv('data/example_output.csv')


################################################################
#### HUGGINGFACE MODEL TO SUMMARIZE ARTICLES ###################
################################################################

summary_text = """It has been said that astronomy is a humbling and character-building experience. \
There is perhaps no better demonstration of the folly of human conceits than this distant image of our tiny world. \
To me, it underscores our responsibility to deal more kindly with one another, and to preserve and cherish the pale blue dot, \
the only home we've ever known.

— Carl Sagan, Pale Blue Dot, 1994
"""

################################################################
#### SUMMARY OUTPUTS        ###############################
################################################################

tab2.header(f"arXiv.org - {subcategory}")

col1, col2 = tab2.columns(2)
col1.metric("Number of Papers", "1000")
col2.metric("Avg. Length", '500 words')

tab2.write(f"Summary of topics:\n\n{summary_text}")

#### EXAMPLE HISTOGRAM
from bokeh.plotting import figure
from bokeh.io import show, output_file

histogram_data = [500 + 100 * (np.random.normal()) for i in range(1000)]
hist, edges = np.histogram(histogram_data, density=True, bins=50)
p = figure(title=f"Lengths of Papers",
            x_axis_label="Tokens",width=100, height=200)
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")

tab2.bokeh_chart(p,use_container_width=True)

#### EXAMPLE TOPIC IMPORTANCE
topic_importance = {
	'black hole': 30,
	'quasar' : 25,
	"nuclei": 15,
	'energy': 50,
	'gravity': 20,
	"eigen": 4
}

topic_df = pd.DataFrame(topic_importance.items(), columns=['topic','frequency'])
topic_df = topic_df.sort_values(by='frequency', ascending=False)

tab2.bar_chart(data= topic_df, x='topic', y='frequency')

tab2.caption('NOTE TO STEPHEN: CREATE A WORDCLOUD')


################################################################
#### SUMMARY OUTPUTS        ###############################
################################################################

tab3.header("Notable Papers")
tab3.caption('NOTE TO STEPHEN: BIBLIOGRAPHIC INFO')

#light string editing
df['Summary'] = df['Summary'].str.replace('\n',' ') # removing line breaks
df['Title'] = df['Title'].str.replace('\n','') # removing line breaks

df['Author'] = df['Author'].str.replace("\\n', '\\n","', \n'")
df['Author'] = df['Author'].apply(ast.literal_eval)

for paper in range(len(df)):
	tab3.markdown(f"##### {df['Title'][paper]}") #print the title
	tab3.markdown(f"**Summary**:  {df['Summary'][paper]}") # abstract / summary

	tab3.caption('**Authors**:')
	auth_list = [f"{i}\n" for i in (df['Author'][paper])]
	tab3.caption('\n'.join(auth_list))
	tab3.write(f"Link: {df['ID'][paper]}")
	tab3.divider()



####################


