import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import pandas as pd
import glob, os, json
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
@st.cache

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Data cleaning and wrangling
#Sleep Data
sleep_dir = 'Data/Sleep/'

sleep_pattern = os.path.join(sleep_dir, '*.json')
sleep_list = glob.glob(sleep_pattern)

dfs = []
for file in sleep_list:
    with open(file) as f:
        sleep_data = pd.json_normalize(json.loads(f.read()))
        sleep_data['user'] = file.rsplit("/", 1)[-1].split('.')[0].split('_')[1]
    dfs.append(sleep_data)
sleepdf = pd.concat(dfs)

sleepdf['resp_time'] = pd.to_datetime(sleepdf['resp_time'], unit='s')

#Remove columns
sleepdf = sleepdf.drop(columns=['null','resp_time','location'])

#Remove NA from rows
sleepdf = sleepdf.dropna(subset=['hour'])

#Rename data
sleepdf = sleepdf.rename(columns = {"hour": "How many hours did you sleep last night?",
                                  "rate": "How would rate your overall sleep last night?",
                                  "social": "How often did you have trouble staying awake yesterday while in class, eating meals or engaging in social activity?"})

#Change values
sleepdf['How would rate your overall sleep last night?'].replace(['1','2','3','4'],
                                                            ['Very Good','Fairly Good','Fairly Bad','Very Bad'], inplace=True)

sleepdf['How often did you have trouble staying awake yesterday while in class, eating meals or engaging in social activity?'].replace(['1','2','3','4'],
                                                            ['None','Once','Twice','Three or more times'], inplace=True)

sleepdf=sleepdf.reset_index()

#Stress Data
stress_dir = 'Data/Stress'

stress_pattern = os.path.join(stress_dir, '*.json')
stress_list = glob.glob(stress_pattern)

dfs = []
for file in stress_list:
    with open(file) as f:
        stress_data = pd.json_normalize(json.loads(f.read()))
        stress_data['user'] = file.rsplit("/", 1)[-1].split('.')[0].split('_')[1]
    dfs.append(stress_data)
stressdf = pd.concat(dfs)

stressdf['resp_time'] = pd.to_datetime(stressdf['resp_time'], unit='s')

#Remove columns
stressdf = stressdf.drop(columns=['null','resp_time','location'])

#Remove NA from rows
stressdf = stressdf.dropna(subset=['level'])

#Rename data
stressdf = stressdf.rename(columns = {"level": "Right now, I am..."})

#Change values
stressdf['Right now, I am...'].replace(['1','2','3','4','5'],
                                       ['A little stressed','Definitely stressed','Stressed out','Feeling good','Feeling great'], inplace=True)

#Social Data
social_dir = 'Data/Social/'

social_pattern = os.path.join(social_dir, '*.json')
social_list = glob.glob(social_pattern)

dfs = []
for file in social_list:
    with open(file) as f:
        social_data = pd.json_normalize(json.loads(f.read()))
        social_data['user'] = file.rsplit("/", 1)[-1].split('.')[0].split('_')[1]
    dfs.append(social_data)
socialdf = pd.concat(dfs)

socialdf['resp_time'] = pd.to_datetime(socialdf['resp_time'], unit='s')

#Remove columns
socialdf = socialdf.drop(columns=['null','resp_time','location'])

#Remove NA from rows
socialdf = socialdf.dropna(subset=['number'])

#Rename data
socialdf = socialdf.rename(columns = {"number": "Number of people you interact with:"})

#Change values
socialdf['Number of people you interact with:'].replace(['1','2','3','4','5','6'],
                                       ['0-4 people','5-9 people','10-19 people','20-49 people','50-99 people','Over 100 people'], inplace=True)

#Exercise Data
exercise_dir = 'Data/Exercise'

exercise_pattern = os.path.join(exercise_dir, '*.json')
exercise_list = glob.glob(exercise_pattern)

dfs = []
for file in exercise_list:
    with open(file) as f:
        exercise_data = pd.json_normalize(json.loads(f.read()))
        exercise_data['user'] = file.rsplit("/", 1)[-1].split('.')[0].split('_')[1]
    dfs.append(exercise_data)
exercisedf = pd.concat(dfs)

exercisedf['resp_time'] = pd.to_datetime(exercisedf['resp_time'], unit='s')

#Remove columns and null from data
exercisedf = exercisedf.reset_index(drop=True)
exercisedf = exercisedf.drop(columns=['resp_time','location'])
exercisedf['schedule'] = exercisedf['schedule'].replace(['null'],[np.nan])
exercisedf['have'] = exercisedf['have'].replace(['null'],[np.nan])
exercisedf = exercisedf.dropna()

#Rename data
exercisedf = exercisedf.rename(columns = {"exercise": "If you exercised, how long did you exercise for?",
                                  "have": "Did you do vigorous exercise today that does not include walking?",
                                  "schedule": "If no did you want to but couldn't because of your schedule?",
                                  "walk": "How long did you walk for today?"})

exercisedf['If you exercised, how long did you exercise for?'].replace(['1','2','3','4','5'],
                                                            ['None','>30 minutes','30-60 minutes','60-90 minutes','>90 minutes'], inplace=True)

exercisedf['Did you do vigorous exercise today that does not include walking?'].replace(['1','2'],
                                                            ['Yes','No'], inplace=True)

exercisedf["If no did you want to but couldn't because of your schedule?"].replace(['1','2'],
                                                            ['Yes','No'], inplace=True)

exercisedf['How long did you walk for today?'].replace(['1','2','3','4','5'],
                                                            ['None','>30 minutes','30-60 minutes','60-90 minutes','>90 minutes'], inplace=True)

#Big Five Data
bigfive = pd.read_csv('Data/BigFive_clean.csv')

#Flourishing Scale Data
flourish = pd.read_csv('Data/FlourishingScale_clean.csv')

#Loneliness Scale Data
loneliness = pd.read_csv('Data/LonelinessScale_clean.csv')

#Perceived Stress Data
pstress = pd.read_csv('Data/PerceivedStressScale_clean.csv')

#PHQ 9 Data
phq = pd.read_csv('Data/PHQ_9_clean.csv')

#Building the dashboard

#Navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('', ('Introduction',
                             'Student Lifestyle Indicator',
                             'Big Five Data',
                             'Flourishing Scale Data',
                             'Loneliness Scale Data',
                             'Perceived Stress Data',
                             'PHQ 9 Data'))

#Page 1 - Introduction
if page == "Introduction":
    st.header("Student Life Dashboard")

    lottie_url = "https://assets4.lottiefiles.com/packages/lf20_jmuq5aha.json"
    lottie_animation = load_lottieurl(lottie_url)
    st_lottie(lottie_animation, key="animation", height=500)

    st.markdown("The following dashboard contains data surrounding students’ lifestyle patterns and mental health. The data is derived from the StudentLife Dataset by Darthmouth University. StudentLife is the first study that uses passive and automatic sensing data from the phones of a class of 48 Dartmouth students over a 10 week term to assess their mental health (e.g., depression, loneliness, stress), academic performance (grades across all their classes, term GPA and cumulative GPA) and behavioral trends (e.g., how stress, sleep, visits to the gym, etc. change in response to college workload -- i.e., assignments, midterms, finals -- as the term progresses). For confidentiality purposes, details of the students’ profile are purposefully hidden. This dashboard also does not include mobile phone activity data and course data. It is hoped that the data in this dashboard can give an overview of insight to students’ mindset within a given time frame. Doing so will hopefully help us to make connections about students’ life patterns and it might also same surveys and approaches could be replicated in further studies. ")
    st.info('Use the navigation sidebar to browse the dashboard', icon="ℹ️")

    st.subheader("Read more about the study here:")
    st.caption(
        'Wang, Rui, Fanglin Chen, Zhenyu Chen, Tianxing Li, Gabriella Harari, Stefanie Tignor, Xia Zhou, Dror Ben-Zeev, and Andrew T. Campbell. "StudentLife: Assessing Mental Health, Academic Performance and Behavioral Trends of College Students using Smartphones." In Proceedings of the ACM Conference on Ubiquitous Computing. 2014.')

    resource1, resource2, resource3 = st.columns(3)

    with resource1:
        st.markdown(
            "[![Foo](https://styles.redditmedia.com/t5_2r97t/styles/communityIcon_ri05w19k4zh01.png)]"
            "(https://studentlife.cs.dartmouth.edu/dataset.html)")
        st.markdown('<div style="text-align: center;">Access Full Dataset</div>', unsafe_allow_html=True)

    with resource2:
        st.markdown(
            "[![Foo](https://static-00.iconduck.com/assets.00/research-icon-256x256-2m8g1agl.png)]"
            "(https://studentlife.cs.dartmouth.edu/)")
        st.markdown('<div style="text-align: center;">Background of Study</div>', unsafe_allow_html=True)

    with resource3:
        st.markdown(
            "[![Foo](https://www.andrew-consulting.com/wp-content/uploads/2018/09/qodob-mu-774x974.png)]"
            "(https://studentlife.cs.dartmouth.edu/studentlife.pdf)")
        st.markdown('<div style="text-align: center;">Read Full Paper</div>', unsafe_allow_html=True)


#Page 2 - Student Lifestyle Indicator
if page == "Student Lifestyle Indicator":
    st.header("Student Lifestyle Indicator")
    st.markdown("The following data are taken from the ecological momentary assessment (EMA) survey subset. During the course of the study, the survey are given to students in random times of day.")

    visualization = st.sidebar.selectbox('Select an indicator:',
                                     options=['Sleep Data',
                                              'Stress Data',
                                              'Social Data',
                                              'Exercise Data'])
    if visualization == 'Sleep Data':
        st.header("Sleep Data")

        st.subheader("On average, how many hours did you sleep last night?")
        sleepdf["How many hours did you sleep last night?"] = sleepdf["How many hours did you sleep last night?"].astype(int)
        sleepaggregate = sleepdf.groupby('user').agg({"How many hours did you sleep last night?":'mean'}).reset_index()
        sleepaggregate["How many hours did you sleep last night?"] = sleepaggregate["How many hours did you sleep last night?"].round(2)
        sleepfig1 = px.bar(sleepaggregate, x='user', y='How many hours did you sleep last night?')
        st.plotly_chart(sleepfig1)

        st.subheader("How would rate your overall sleep last night?")
        sleepfig2 = px.pie(sleepdf, names='How would rate your overall sleep last night?', width=500.0)
        st.plotly_chart(sleepfig2)

        st.subheader("How often did you have trouble staying awake yesterday while in class, eating meals or engaging in social activity?")
        sleepfig3 = px.pie(sleepdf, names='How often did you have trouble staying awake yesterday while in class, eating meals or engaging in social activity?', width=500.0)
        st.plotly_chart(sleepfig3)

    if visualization == 'Stress Data':
        st.header("Stress Data")

        st.subheader("Right now, I am...")
        stressfig = px.pie(stressdf, names='Right now, I am...', width=500.0)
        st.plotly_chart(stressfig)

    if visualization == 'Social Data':
        st.header("Social Data")

        st.subheader("Number of people you interact with:")
        socialfig = px.pie(socialdf, names='Number of people you interact with:', width=500.0)
        st.plotly_chart(socialfig)

    if visualization == 'Exercise Data':
        st.header("Exercise Data")

        st.subheader("If you exercised, how long did you exercise for?")
        exercisefig1 = px.pie(exercisedf, names='If you exercised, how long did you exercise for?', width=500.0)
        st.plotly_chart(exercisefig1)

        st.subheader("Did you do vigorous exercise today that does not include walking?")
        exercisefig2 = px.pie(exercisedf, names='Did you do vigorous exercise today that does not include walking?', width=500.0)
        st.plotly_chart(exercisefig2)

        st.subheader("If no did you want to but couldn't because of your schedule?")
        exercisefig3 = px.pie(exercisedf, names="If no did you want to but couldn't because of your schedule?", width=500.0)
        st.plotly_chart(exercisefig3)

        st.subheader("How long did you walk for today?")
        exercisefig4 = px.pie(exercisedf, names="How long did you walk for today?", width=500.0)
        st.plotly_chart(exercisefig4)

# Page 3 - Big Five

if page == "Big Five Data":
    st.header("Big Five Data")
    st.markdown("The following data were derived from the Big Five Personality Test (BFI). The five-factor model of personality, known as the Big Five Personality Traits, consists of extraversion, neuroticism, openness to experience (sometimes just called openness), agreeableness, and conscientiousness (Costa & McCrae, 1992). The survey were conducted before (pre) and after (post) the study.")
    visualization = st.sidebar.selectbox('I see myself as someone who...',
                                         options=['Is talkative',
                                                  'Tends to find fault with others',
                                                  'Is depressed, blue',
                                                  'Is helpful and unselfish with others',
                                                  'Remains calm in tense situations',
                                                  'Is curious about many different things',
                                                  'Tends to be disorganized',
                                                  'Worries a lot',
                                                  'Has an active imagination',
                                                  'Prefers work that is routine'])


    if visualization == 'Is talkative':
        st.subheader("I am someone who is talkative")
        bigfivetest = bigfive.groupby(['type','Is talkative']).agg({'uid':'size'}).reset_index()

        bigfivefig1 = px.histogram(bigfivetest, x="Is talkative", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig1)

    if visualization == 'Tends to find fault with others':
        st.subheader("I am someone who tends to find fault with others")
        bigfivetest = bigfive.groupby(['type','Tends to find fault with others']).agg({'uid':'size'}).reset_index()

        bigfivefig2 = px.histogram(bigfivetest, x="Tends to find fault with others", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig2)

    if visualization == 'Is depressed, blue':
        st.subheader("I am someone who is depressed, blue")
        bigfivetest = bigfive.groupby(['type','Is depressed, blue']).agg({'uid':'size'}).reset_index()

        bigfivefig3 = px.histogram(bigfivetest, x="Is depressed, blue", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig3)

    if visualization == 'Is helpful and unselfish with others':
        st.subheader("I am someone who is helpful and unselfish with others")
        bigfivetest = bigfive.groupby(['type','Is helpful and unselfish with others']).agg({'uid':'size'}).reset_index()

        bigfivefig4 = px.histogram(bigfivetest, x="Is helpful and unselfish with others", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig4)

    if visualization == 'Remains calm in tense situations':
        st.subheader("I am someone who remains calm in tense situations")
        bigfivetest = bigfive.groupby(['type','Remains calm in tense situations']).agg({'uid':'size'}).reset_index()

        bigfivefig5 = px.histogram(bigfivetest, x="Remains calm in tense situations", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig5)

    if visualization == 'Is curious about many different things':
        st.subheader("I am someone who is curious about many different things")
        bigfivetest = bigfive.groupby(['type','Is curious about many different things']).agg({'uid':'size'}).reset_index()

        bigfivefig6 = px.histogram(bigfivetest, x="Is curious about many different things", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig6)

    if visualization == 'Tends to be disorganized':
        st.subheader("I am someone who tends to be disorganized")
        bigfivetest = bigfive.groupby(['type','Tends to be disorganized']).agg({'uid':'size'}).reset_index()

        bigfivefig7 = px.histogram(bigfivetest, x="Tends to be disorganized", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig7)

    if visualization == 'Worries a lot':
        st.subheader("I am someone who worries a lot")
        bigfivetest = bigfive.groupby(['type','Worries a lot']).agg({'uid':'size'}).reset_index()

        bigfivefig8 = px.histogram(bigfivetest, x="Worries a lot", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig8)

    if visualization == 'Has an active imagination':
        st.subheader("I am someone who has an active imagination")
        bigfivetest = bigfive.groupby(['type','Has an active imagination']).agg({'uid':'size'}).reset_index()

        bigfivefig9 = px.histogram(bigfivetest, x="Has an active imagination", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig9)

    if visualization == 'Prefers work that is routine':
        st.subheader("I am someone who prefers work that is routine")
        bigfivetest = bigfive.groupby(['type','Prefers work that is routine']).agg({'uid':'size'}).reset_index()

        bigfivefig10 = px.histogram(bigfivetest, x="Prefers work that is routine", y="uid",
                           color='type', barmode='group',
                           height=400)
        st.plotly_chart(bigfivefig10)

# Page 4 - Flourishing Scale Data

if page == "Flourishing Scale Data":
    st.header("Flourishing Scale Data")
    st.markdown("The Flourishing Scale is a brief 8-item summary measure of the respondent's self-perceived success in important areas such as relationships, self-esteem, purpose, and optimism. In the actual study, the scale provides a single psychological well-being score.")
    visualization = st.sidebar.selectbox('Choose a statement:',
                                         options=['I lead a purposeful and meaningful life',
                                                  'My social relationships are supportive and rewarding',
                                                  'I am engaged and interested in my daily activities'])

    if visualization == 'I lead a purposeful and meaningful life':
        st.subheader("I lead a purposeful and meaningful life")
        flourishtest = flourish.groupby(['type', 'I lead a purposeful and meaningful life']).agg({'uid': 'size'}).reset_index()

        flourishfig1 = px.histogram(flourishtest, x="I lead a purposeful and meaningful life", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(flourishfig1)

    if visualization == 'My social relationships are supportive and rewarding':
        st.subheader("My social relationships are supportive and rewarding")
        flourishtest = flourish.groupby(['type', 'My social relationships are supportive and rewarding']).agg({'uid': 'size'}).reset_index()

        flourishfig2 = px.histogram(flourishtest, x="My social relationships are supportive and rewarding", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(flourishfig2)

    if visualization == 'I am engaged and interested in my daily activities':
        st.subheader("I am engaged and interested in my daily activities")
        flourishtest = flourish.groupby(['type', 'I am engaged and interested in my daily activities']).agg({'uid': 'size'}).reset_index()

        flourishfig3 = px.histogram(flourishtest, x="I am engaged and interested in my daily activities", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(flourishfig3)

# Page 5 - Loneliness Scale Data

if page == "Loneliness Scale Data":
    st.header("Loneliness Scale Data")
    st.markdown("Data presented in this page were inspired by the UCLA Loneliness Scale. This 20-item scale were designed to measure one’s subjective feelings of loneliness as well as feelings of social isolation. Participants rate each item as either O (“I often feel this way”),S (“I sometimes feel this way”), R (“I rarely feel this way”), N (“I never feel this way”). In this dashboard, the data were translated to a frequency scale.")
    visualization = st.sidebar.selectbox('Choose a statement:',
                                         options=['There is no one I can turn to',
                                                  'I do not feel alone',
                                                  'I have a lot in common with the people around me',
                                                  'My interests and ideas are not shared by those around me',
                                                  'There are people who really understand me'])

    if visualization == 'There is no one I can turn to':
        st.subheader("There is no one I can turn to")
        lonelinesstest = loneliness.groupby(['type', 'There is no one I can turn to']).agg({'uid': 'size'}).reset_index()

        lonelinessfig1 = px.histogram(lonelinesstest, x="There is no one I can turn to", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(lonelinessfig1)

    if visualization == 'I do not feel alone':
        st.subheader("I do not feel alone")
        lonelinesstest = loneliness.groupby(['type', 'I do not feel alone']).agg({'uid': 'size'}).reset_index()

        lonelinessfig2 = px.histogram(lonelinesstest, x="I do not feel alone", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(lonelinessfig2)

    if visualization == 'I have a lot in common with the people around me':
        st.subheader("I have a lot in common with the people around me")
        lonelinesstest = loneliness.groupby(['type', 'I have a lot in common with the people around me']).agg({'uid': 'size'}).reset_index()

        lonelinessfig3 = px.histogram(lonelinesstest, x="I have a lot in common with the people around me", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(lonelinessfig3)

    if visualization == 'My interests and ideas are not shared by those around me':
        st.subheader("My interests and ideas are not shared by those around me")
        lonelinesstest = loneliness.groupby(['type', 'My interests and ideas are not shared by those around me']).agg({'uid': 'size'}).reset_index()

        lonelinessfig4 = px.histogram(lonelinesstest, x="My interests and ideas are not shared by those around me", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(lonelinessfig4)

    if visualization == 'There are people who really understand me':
        st.subheader("There are people who really understand me")
        lonelinesstest = loneliness.groupby(['type', 'There are people who really understand me']).agg({'uid': 'size'}).reset_index()

        lonelinessfig5 = px.histogram(lonelinesstest, x="There are people who really understand me", y="uid",
                                    color='type', barmode='group',
                                    height=400)
        st.plotly_chart(lonelinessfig5)

# Page 6 - Perceived Stress Data

if page == "Perceived Stress Data":
    st.header("Perceived Stress Data")
    st.markdown("For stress, we used the Perceived Stress Scale (PSS) that includes ten items asking students’ feelings and perceived stress measured on a 5-point Likert scale from 0 (strongly disagree) to 4 (strongly agree) (Cohen et al., 1983). PSS scale was used in hundreds of studies and validated in many languages.")
    visualization = st.sidebar.selectbox('Choose a statement:',
                                         options=['How often have you been upset because of something that happened unexpectedly?',
                                                  'How often have you felt that you were unable to control the important things in your life?',
                                                  'How often have you felt confident about your ability to handle your personal problems?'])

    if visualization == 'How often have you been upset because of something that happened unexpectedly?':
       st.subheader("In the last month, how often have you been upset because of something that happened unexpectedly?")
       pstressfig1 = px.pie(pstress, names='In the last month, how often have you been upset because of something that happened unexpectedly?', width=500.0)
       st.plotly_chart(pstressfig1)

    if visualization == 'How often have you felt that you were unable to control the important things in your life?':
       st.subheader("In the last month, how often have you felt that you were unable to control the important things in your life?")
       pstressfig2 = px.pie(pstress, names='In the last month, how often have you felt that you were unable to control the important things in your life?', width=500.0)
       st.plotly_chart(pstressfig2)

    if visualization == 'How often have you felt confident about your ability to handle your personal problems?':
       st.subheader("In the last month, how often have you felt confident about your ability to handle your personal problems?")
       pstressfig3 = px.pie(pstress, names='In the last month, how often have you felt confident about your ability to handle your personal problems?', width=500.0)
       st.plotly_chart(pstressfig3)

# Page 7 - PHQ 9 Data

if page == "PHQ 9 Data":
    st.header("PHQ 9 Data")
    st.markdown("The 9-question Patient Health Questionnaire is a diagnostic tool introduced in 2001 to screen adult patients in a primary care setting for the presence and severity of depression. It rates depression based on the self-administered Patient Health Questionnaire.")

    st.subheader("Little interest or pleasure in doing things")
    phqfig1 = px.pie(phq, names='Little interest or pleasure in doing things', width=500.0)
    st.plotly_chart(phqfig1)

    st.subheader("Feeling down, depressed, hopeless")
    phqfig2 = px.pie(phq, names='Feeling down, depressed, hopeless.', width=500.0)
    st.plotly_chart(phqfig2)

    st.subheader("Feeling tired or having little energy")
    phqfig3 = px.pie(phq, names='Feeling tired or having little energy', width=500.0)
    st.plotly_chart(phqfig3)

    st.subheader("Poor appetite or overeating")
    phqfig4 = px.pie(phq, names='Poor appetite or overeating', width=500.0)
    st.plotly_chart(phqfig4)

    st.subheader("Thoughts that you would be better off dead, or of hurting yourself")
    phqfig5 = px.pie(phq, names='Thoughts that you would be better off dead, or of hurting yourself', width=500.0)
    st.plotly_chart(phqfig5)