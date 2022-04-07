# DJV-Internship-Discovery-Tool #
A recommendation engine that identifies internship opportunities a student may be interested in during their search.

## Summary of the Internship Discovery Tool ##
The internship discovery tool gathers internship opportunities from various sources, produces personalized recommendations of off-the-radar but similar internships, and provides the user with the resources needed to take action. 

### How to use the tool ###
To use the internship discovery tool, clone this repo. Then run `'streamlit run student_demo.py'`.

This will open the Streamlit app, which serves as the user interface for the tool. The initial page will be the `'Launch'` page, press the `'Start'` button and allow the model to load. Once the model is loaded, updated the `'student_demo-state.json'` file to read, `'"visible_section": "welcome"'`. Refresh the webpage and the tool will be ready to use.

### Internship Discovery Tool Methodology ###
Polydelta collected internship opportunities from three separate sources, USA Jobs, Indeed.com, and the Texas A&M Rangeland, Wildlife, and Fisheries Management Job Board. We processed and transformed this data through distinct pipelines. During this time, the team experimented with a variety of natural language processing and machine learning approaches. The final model calculated the similarity between every internship in our dataset based on a variety of features.

These features include:
- Internship title
- Internship description
- Company name
