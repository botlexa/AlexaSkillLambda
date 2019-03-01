from getdata import getcustomername, getformdata, getformfields, getformname, saveformfields
CustomerID = '1'
FormList = []
FormField = {}
Response_List = []
CustomerName = ''
SelectedFormID = ''

currentOpCounter = 0
confirmFlag = 0
spellFlag = 0
counter = 1
# ------------------------------Part2--------------------------------
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
# ------------------------------Part3--------------------------------
def on_start():
    #call code to get CustomerName, FormList
    global CustomerName, FormList
    CustomerName = getcustomername(CustomerID)
    FormList = getformname(CustomerID)
    print("Session Started.")
def on_launch(event):
    return form_list()
def on_end():
    print("Session Ended.")
# -----------------------------Part3.1-------------------------------
def intent_scheme(event):
    intent_name = event['request']['intent']['name']
    if intent_name == "playerBio":
        return application_Operation(event)
    if intent_name in ["AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
    else:
        return application_Operation(event)
# ---------------------------Part3.1.1-------------------------------
def application_Operation(event):
    global confirmFlag
    name = event['request']['intent']['slots']['player']['value']
    user_input = name.upper()
    if confirmFlag == 1:
        confirm_yesno(user_input)

    if currentOpCounter == 0:#ask to select form
        confirmFlag = 0
        return form_list()
    if currentOpCounter == 1:#form is selected by user - confirm yes/no
        global SelectedFormID
        SelectedFormID = FormList[user_input]
        confirmFlag = 1
        return confirm_formlist(user_input)
    if currentOpCounter == 2:#form is confirmed. Ask Questions
        confirmFlag = 0
        return get_form_attribute(user_input)
    if currentOpCounter == 3:#user gave attribute value - Confirm yes/no
            confirmFlag = 1
            return confirm_form_attribute(user_input)
# ---------------------------Part3.1.2-------------------------------
def form_list():
    global currentOpCounter
    global confirmFlag
    currentOpCounter = 1
    confirmFlag = 0
    onlunch_MSG = " Welcome to " + CustomerName + ", Select your form to Open : " + ', '.join(map(str, FormList))
    reprompt_MSG = "Application Assistant"
    card_TEXT = "Pick an application."
    card_TITLE = "Choose one by giving the name."
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_formlist(user_input):
    global confirmFlag
    confirmFlag = 1
    wrongname_MSG = "You have selected: " + user_input + " form." + " Is That Correct?"
    reprompt_MSG = "You've picked " + user_input
    card_TEXT = "You've picked " + user_input
    card_TITLE = "You've picked " + user_input
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def get_form_attribute():
    global currentOpCounter
    currentOpCounter = currentOpCounter + 1
    global counter
    wrongname_MSG = "Please tell your " + list(FormField)[counter]
    reprompt_MSG = "Please tell your " + list(FormField)[counter]
    card_TEXT = "Please tell your " + list(FormField)[counter]
    card_TITLE = "Please tell your " + list(FormField)[counter]
    counter = counter + 1
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_form_attribute(user_input):
    wrongname_MSG = "You have entered " + user_input + " Is That Correct?"
    reprompt_MSG = "You have entered " + user_input + " Is That Correct?"
    card_TEXT = "You have entered " + user_input + " Is That Correct?"
    card_TITLE = "You have entered " + user_input + " Is That Correct?"
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_yesno(user_input):
    global currentOpCounter, FormField, counter
    if user_input == 'YES':
        if currentOpCounter == 1:
            FormField = getformfields(SelectedFormID)

        currentOpCounter = currentOpCounter + 1
    elif user_input == 'NO':
        currentOpCounter = currentOpCounter - 1
        if counter > 1:
            counter = counter - 1
    return currentOpCounter

# ---------------------------Part3.1.2-------------------------------
def stop_the_skill(event):
    stop_MSG = "You have entered: " + ', '.join(map(str, Player_LIST)) + ". Thank you."
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
def assistance(event):
    assistance_MSG = "Please repond with you personal details like you name, surname, date of birth."
    reprompt_MSG = "Please repond with you personal details like you name, surname, date of birth."
    card_TEXT = "Please repond with you personal details like you name, surname, date of birth."
    card_TITLE = "Please repond with you personal details like you name, surname, date of birth."
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def fallback_call(event):
    assistance_MSG = "Please repond with you personal details like you name, surname, date of birth."
    reprompt_MSG = "Please repond with you personal details like you name, surname, date of birth."
    card_TEXT = "Please repond with you personal details like you name, surname, date of birth."
    card_TITLE = "Please repond with you personal details like you name, surname, date of birth."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
# ------------------------------Part4--------------------------------
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict
def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict
def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict
def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title,
                                                                              reprompt_text, value)
    return response_dict
