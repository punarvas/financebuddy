## Inspiration
As an international student in the USA, it is very easy to run off the money when you are balancing your day-to-day life. From groceries to books and from Spotify to car rentals, with no family around, most students struggle with allocating money wisely. It turns out that budget planning helps most adults, regardless of their profession, to manage their expenses up to a mark. With advancements in AI, this task can be left in the hands of software to automatically plan your budget based on your expenditures.

## What it does
Finance Buddy assesses your last month's expenses, and based on that, it will create money-saving challenges for you. These challenges will be highly engaging, and the fun part? They will always be a surprise for us, too! Why? Because it is powered by AI which will automatically create challenges for you, two challenges at a time. You will earn points (XP) if you complete each of the challenges. The more XPs you earn, the more levels you will open. 

## How we built it
Finance Buddy is technically a Streamlit app that runs on a web browser. It relies on various APIs, among which Splitwise Expense API and OpenAI API are prominent. Upon authorization, Finance Buddy fetches your last month's records from Splitwise's servers and processes them with advanced analytics in Python. The resulting JSON file contains analytics results that will be used by an underlying Large Language Model (LLM) to generate two challenges along with hints to save money. The model is prompt-engineered in such a way that it will make use of your budget plan and analytics on the statement to create new challenges every time you click "Advise me".

## Challenges we ran into
The first and foremost challenge was to collect bank statements or expense data. We had limited access to APIs available, which were not compatible with our idea or at least had no sufficient input parameters. We got an idea to use Splitwise API, but the integration is non-trivial. In addition to that, it is highly difficult to prompt-engineered powerful models like GPT-4. The additional challenge is there is no or limited discipline to achieve a perfectly working model with prompt engineering.

## Accomplishments that we're proud of
It was our first attempt to integrate multiple APIs and programs related to expense data, AI, and data analysis to solve one single problem. From the top, this problem looks extremely simple to solve. The extra challenge is introduced by the integration of AI models and steering its outcomes to develop the proof-of-concept for Finance Buddy. We are proud of this achievement.

## What we learned
On the way, we learned a lot of things. As we aspire to become software engineers in the future, we learned a bunch of useful tools that we can use during our full-time roles to solve many similar problems. Since this hackathon is highly time-sensitive, we as a team planned things and managed sleep schedules accordingly taking our teamwork skills to the next level. 


## What's next for Finance Buddy
We see Finance Buddy as a mobile app in the future with live communication with Splitwise to track the user's expenditure behavior silently and suggest new fun challenges on demand. Due to its gamified nature for such an important topic of financial literacy, we aim to make this app more fun and have levels to unlock each time a user earns XPs for their success in a challenge. In the fast-forward future, every college student will be on Finance Buddy's social network to take on challenges with friends to save money for, for example, a week-long trip to Mackinaw Islands in the up-north!