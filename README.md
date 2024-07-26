# DuoHablo
_Any resemblance of the name to green owls is wholly intentional and will be changed for legal reasons if this ever gets large enough to need it_

## Raison d'être
After a while plugging away at Duolingo, wanted something more than mini-games. 

This project is an attempt to set up and encourage speaking practice sessions, with data monitoring and a hook-up to the Google Translate API to leave or review tricky words before and after the session.

## Technologies/practices used
✨ = new; 👨‍‍🏫 = learning; 🤝 = familiar
- `streamlit` 🤝
- `streamlit.AppTest` for streamlit testing ✨
- `pytest` for general testing 👨‍‍🏫
- Google Translate API/SDK ✨
- Test-driven development as a general approach ✨
  - (_mostly_ adhered to)
- `bump2version` for version management ✨

## 'Roadmap'
### Chores
- [ ] Finish Google Translate API instructions
- [ ] Write tests for the Google Translate API translation util
- [ ] Containerise
- [ ] Complete the session state maintenance when moving between pages 
  - (Only did the pre-session components as the ones most likely to be interrupted by a page change)

### Features
- [ ] Add option in settings to set languages
  - [ ] And add this to the saved data
  - [ ] And let the data view be filterable by the languages
- [ ] Add notes for each session to the data saved
  - [ ] This could take the form of words that have been translated

## Running locally

### Google Translate API
Unfortunately, you need to deal with Google authentication - 'unfortunately' because Google's docs are labrynthine. 
[More details coming].

### Set-up files
Create an `.env` file in the root directory, following the template in `.env.example`

Create `user_data.csv` and `user_categories.csv` files in the `data` folder, following the template in that folder's 
`README.md`.

### Everything else
Run `pytest .` to check that everything is working (and that, if anything breaks, it's not you who did it).

---
---

## Useful Streamlit links and notes
### Session state
Session state is important and/but something with some quirks in Streamlit. Thankfully, they have some specific 
pages about this in their documentation.

There's a section about [using buttons to modify or reset other widgets here](https://docs.streamlit.io/develop/concepts/design/buttons#buttons-to-modify-or-reset-other-widgets), which is really useful as buttons are one of the most frequent, most simple aspects you can use.

Another important concept is widget state and the ways it can interact with session state. On a multi-page app, widgets (according to my understanding) get torn down when you switch page, which means that their value will be reset. The way around this is documented in [this section about session state and widget state](https://docs.streamlit.io/develop/concepts/architecture/session-state#session-state-and-widget-state-association).


### Testing
The testing framework is a fantastic addition to Streamlit. It is relatively well-documented in the [App testing section of the docs here](https://docs.streamlit.io/develop/api-reference/app-testing). 

There are a couple of main quirks that I think it's worth being aware of:
- You can call `st.<widget_type>` within a test and it will return a list of all of the widgets of that type. As far 
  as I can tell, you then reference specific instances by their index in this list - it might be useful if you could 
  reference by the widget key.
- The `st.write` widget, which is 'magic' and smart about how it outputs what is passed to it, will depend based on 
  said input. Written text is output as st.markdown. This wasn't obvious to me from the testing docs but makes sense 
  when reading the [`st.write` page itself](https://docs.streamlit.io/develop/api-reference/write-magic/st.write). 
- Each instance of a widget (e.g. the 0th item in the `st.write` list) will be a Streamlit element class. As far as 
  I can tell, these aren't documented, although using an IDE like Pycharm will help you find the attributes you need.
  Generally, looking for `.value` will be enough.

### Making a timer in Streamlit
The timer/stopwatch component was a crucial one of this idea, and I thought this would be an easy plug and play. I wasn't sure _how_, but assumed there'd be either a native or third-party solution. Not quite. 

There wasn't one of either. My mind then went to use an `st.html` block (as I was aware they existed and it seemed like a task ChatGPT could bash out), but that didn't work because `st.html` didn't allow javascript to be executable.

Fortunately, others have had similar questions on the Streamlit Discuss community. [This question](https://discuss.streamlit.io/t/how-to-make-a-timer/22675/2) supplied a base that kinda worked, but not really for my uses; more of a timer than a stopwatch, and I wanted more of a stopwatch
Then, [this comment on another question](https://discuss.streamlit.io/t/issue-with-asyncio-run-in-streamlit/7745/7) and the subsequent comments further down, led me to the working version that I have now. The main difference between my version and the code derived from those comments is that I decided to maintain a version of the output when the function was paused.

## App functionality design thoughts
The app is very simple but there were a few deliberate choices that I wanted to note.

### Confidence scale
Some days you don't feel good and some days you feel great! 

I think having this at the top is a nice, implicit acknowledgement of that which actually makes me more likely to give it a go even if I'm not feeling confident.

Part of that is because I figured the 'target time' should be linked to that confidence level. How you're feeling is going to have an effect on what 'success' looks like, and I think the changing limits of the target time make it a better incentive.

Also, the seven-point scale. I like seven-point scales. Everyone knows that people shy away from the extremes of scales, and I reckon this is particularly going to be the case when talking about confidence at speaking in a foreign language. Also, really, if you're feeling at the negative extreme you're probably not going to be doing a speaking session in the first place.

### Google Translate integration
The integration _before_ and _after_ the speaking session was deliberate. 

I've found, personally, that trying to speak while sat in front of the Google Translate website leads to me relying on it more and more. Part of speaking a foreign language is needing to navigate around your ability in it in the moment, and having a dictionary in front of you makes it tempting to start 'translating' rather than speaking.

It also meshes quite nicely with the 'focus topic' idea. The topic helps make it clearer what you might need to translate ahead of time, while a completely open speaking session may make the pre-session translation overwhelming.
