import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import streamlit_wordcloud as st_wordcloud
from pywaffle import Waffle
from matplotlib import pyplot as plt


header_container = st.container()
wordcloud_container = st.container()
dataset_container =  st.container()
role_container = st.container()
social_cues_input_container = st.container()
social_cues_output_container = st.container()

survey_df = pd.read_excel("miro_dataset.xlsx", sheet_name="Sheet1")
#### TODO
# remove Warm Up: Round table datas
# Create a container per category, role, task, look and feel , eye

##########
#### Session directory
s_desired_role = "Ses. 2 -Task 1: Desired Tasks and Social Roles"
s_learning_challenges = "Ses. 1 -Task 1: Learning Challenges"
s_interaction_mode = "Ses. 2 -Task 2: Interaction Modes"
s_apperance = "Ses. 2 -Task 3: Appearance"
s_eye_for = "Ses. 3 -Task 1: Eye(s) for?"
s_eye_like = "Ses. 3 -Task 2: Eyes like?"

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


with header_container:
    st.title("Social Drone in Education Brainwriting Analysis")
    st.text("""This webpage is meant to navigate and search the data collected via Miro in 6 workshops on about designing social drones for education
    """)



with dataset_container:
    st.header('Loading the dataset')
  
    selection = aggrid_interactive_table(df=survey_df)

    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
    

with role_container:
    st.header('Role Analysis')
    role_df = survey_df[survey_df["Task"] == s_desired_role]
    count_table = role_df.role.value_counts()
    count_table = pd.DataFrame(count_table)
    
    data = count_table['role']
    fig = plt.figure(
        FigureClass=Waffle, 
        rows=5, 
        values=data, 
        title={'label': 'role', 'loc': 'left'},
        labels=["{0} ({1})".format(k, v) for k, v in data.items()],
        legend={'loc': 'lower left', 'bbox_to_anchor': (0, -1), 'ncol': 2, 'framealpha': 0}
    )
    st.pyplot(fig)

    option = st.selectbox(
     'Explore verbatim for each category',
     count_table.index)
     
    verbatim_df = role_df[role_df['role'] == option]
    verbatim_list = verbatim_df['Postit'].values
    st.write(verbatim_list)

with social_cues_input_container:
    st.header('Social Cues Input')
    role_df = survey_df[survey_df["Task"] == s_interaction_mode]
    count_table = role_df['Social cues - input'].value_counts()
    count_table = pd.DataFrame(count_table)
    
    data = count_table['Social cues - input']
    fig = plt.figure(
        FigureClass=Waffle, 
        rows=5, 
        values=data, 
        title={'label': 'Social cues - input', 'loc': 'left'},
        labels=["{0} ({1})".format(k, v) for k, v in data.items()],
        legend={'loc': 'lower left', 'bbox_to_anchor': (0, -0.5), 'ncol': 2, 'framealpha': 0}
    )
    st.pyplot(fig)

    option = st.selectbox(
     'Explore verbatim for each category',
     count_table.index)
     
    verbatim_df = role_df[role_df['Social cues - input'] == option]
    verbatim_list = verbatim_df['Postit'].values
    st.write(verbatim_list)
  

st.write()