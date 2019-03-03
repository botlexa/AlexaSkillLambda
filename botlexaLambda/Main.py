from getdata import getcustomername, getformdata, getformfields, getformname, saveformfields, getformNumber

CustomerID = '1'
FormList = {}
FormField = {}
Response_List = []
CustomerName = ''
SelectedFormID = ''
FormNumber = 0
captureSpellValue = ''

currentOpCounter = 0
confirmFlag = 0
spellFlag = 0
counter = 0


def confirm_tester(event, context):
    global FormField
    FormField = getformfields(2)
    return FormField["5"]
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
    # call code to get CustomerName, FormList
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
    global confirmFlag, spellFlag
    name = event['request']['intent']['slots']['player']['value']
    user_input = name.upper()
    if spellFlag == 1:
        if user_input == 'DONE':
            user_input = captureSpell(user_input)
        else:
            return captureSpell(user_input)

    if confirmFlag == 1:
        confirm_yesno(user_input)

    if currentOpCounter == 0:  # ask to select form
        confirmFlag = 0
        return form_list()
    if currentOpCounter == 1:  # form is selected by user - confirm yes/no
        global SelectedFormID
        SelectedFormID = FormList[user_input]
        confirmFlag = 1
        return confirm_formlist(str(SelectedFormID))
    if currentOpCounter == 2:  # form is confirmed. Ask Questions
        confirmFlag = 1
        return get_form_attribute()
    if currentOpCounter == 3:  # user gave attribute value - Confirm yes/no
        confirmFlag = 0
        return confirm_form_attribute(user_input)
    if currentOpCounter == 4:  # user wants to enter spelling
        if spellFlag == 1: #User confirmed that it wants to spell
            return instruct_userhowtospell()
        else:
            confirmFlag = 1
            return confirm_userwanttospell()
# ---------------------------Part3.1.2-------------------------------
def form_list():
    global currentOpCounter, confirmFlag
    currentOpCounter = 1
    confirmFlag = 0
    onlunch_MSG = " Welcome to " + CustomerName + ", Select your form to " \
                                                  "Open : " + ', '.join(map(str, FormList))
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
    global currentOpCounter, counter
    # return debugstop(str(list(FormField)[counter]))
    wrongname_MSG = "Please tell your " + str(FormField[str(list(FormField)[counter])])
    reprompt_MSG = "Please tell your " + str(FormField[str(list(FormField)[counter])])
    card_TEXT = "Please tell your " + str(FormField[str(list(FormField)[counter])])
    card_TITLE = "Please tell your " + str(FormField[str(list(FormField)[counter])])
    counter = counter + 1
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_form_attribute(user_input):
    wrongname_MSG = "You have entered " + user_input + " Is That Correct?"
    reprompt_MSG = "You have entered " + user_input + " Is That Correct?"
    card_TEXT = "You have entered " + user_input + " Is That Correct?"
    card_TITLE = "You have entered " + user_input + " Is That Correct?"
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_yesno(user_input):
    global currentOpCounter, counter, FormField, FormNumber, spellFlag
    if user_input == 'YES' or user_input == 'NO':
        if user_input == 'YES':
            if currentOpCounter == 0: # ask to select form
                return
            if currentOpCounter == 1: # form is selected by user - confirm yes/no
                FormNumber = getformNumber(SelectedFormID)
                FormField = getformfields(SelectedFormID)
                currentOpCounter = currentOpCounter + 1
                return
            if currentOpCounter == 2:  # form is confirmed. Ask Questions
                currentOpCounter = currentOpCounter + 1
                return
            if currentOpCounter == 3:  # user gave attribute value - Confirm yes
                currentOpCounter = 2 #continue asking question
                return
            if currentOpCounter == 4:  # user wants to enter spelling
                spellFlag = 1
                return
        elif user_input == 'NO':
            if currentOpCounter == 0: # ask to select form
                return
            if currentOpCounter == 1: # form is selected by user - confirm no
                currentOpCounter = currentOpCounter - 1
                return
            if currentOpCounter == 2:  # form is confirmed. Ask Questions
                return
            if currentOpCounter == 3:  # user gave attribute value - Confirm no
                currentOpCounter = 4 #ask if user wants to input spelling
                if counter > 0:
                    counter = counter - 1
                return
            if currentOpCounter == 4:  # user doesn't wants to enter spelling
                currentOpCounter = 2
                return
        return currentOpCounter
def captureSpell(user_input):
    global captureSpellValue, counter, FormField, spellFlag, currentOpCounter
    if user_input == 'DONE':
        FormField[str(list(FormField)[counter])] = captureSpellValue
        captureSpellValue = ''
        spellFlag = 0
        currentOpCounter = 3
        #to confirm the captured value
        return FormField[str(list(FormField)[counter])]
    else:
        captureSpellValue = captureSpellValue + user_input
        wrongname_MSG = user_input
        reprompt_MSG = captureSpellValue
        card_TEXT = captureSpellValue
        card_TITLE = captureSpellValue
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def confirm_userwanttospell():
    wrongname_MSG = "Do you want to spell your " + str(FormField[str(list(FormField)[counter])])
    reprompt_MSG = "Do you want to spell your " + str(FormField[str(list(FormField)[counter])])
    card_TEXT = "Do you want to spell your " + str(FormField[str(list(FormField)[counter])])
    card_TITLE = "Do you want to spell your " + str(FormField[str(list(FormField)[counter])])
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def instruct_userhowtospell():
    wrongname_MSG = "please start spelling you " + \
                    str(FormField[str(list(FormField)[counter])]) + " Once completed say DONE"
    reprompt_MSG = "please start spelling you " + \
                    str(FormField[str(list(FormField)[counter])]) + " Once completed say DONE"
    card_TEXT = "please start spelling you " + \
                    str(FormField[str(list(FormField)[counter])]) + " Once completed say DONE"
    card_TITLE = "please start spelling you " + \
                    str(FormField[str(list(FormField)[counter])]) + " Once completed say DONE"
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)


# ---------------------------Part3.1.2-------------------------------
def debugstop(user_input):
    wrongname_MSG = "debug point hit: " + str(user_input)
    reprompt_MSG = "debug point hit: " + str(user_input)
    card_TEXT = "debug point hit: " + str(user_input)
    card_TITLE = "debug point hit: " + str(user_input)
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
def stop_the_skill(event):
    stop_MSG = "You have entered: " + ', '.join(map(str, FormField)) + ". Thank you."
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
def assistance(event):
    assistance_MSG = "Please respond with you personal details like you name, surname, date of birth."
    reprompt_MSG = "Please respond with you personal details like you name, surname, date of birth."
    card_TEXT = "Please respond with you personal details like you name, surname, date of birth."
    card_TITLE = "Please respond with you personal details like you name, surname, date of birth."
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
def fallback_call(event):
    assistance_MSG = "Please repond with you personal details like you name, surname, date of birth."
    reprompt_MSG = "Please repond with you personal details like you name, surname, date of birth."
    card_TEXT = "Please repond with you personal details like you name, surname, date of birth."
    card_TITLE = "Please repond with you personal details like you name, surname, date of birth."
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
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
