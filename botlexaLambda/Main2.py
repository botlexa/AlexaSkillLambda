from getdata import getcustomername, getformdata, getformfields, getformname, saveformfields, getformNumber

CustomerID = '1'
FormList = {}
FormField = {}
Response_List = {}
CustomerName = ''
SelectedFormID = ''
FormNumber = 0
captureSpellValue = ''
lastFormValueEntered = ''

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
    return Operation0("")
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
    if currentOpCounter == 0:  # ask to select form/ask to re-select form
        return Operation0(user_input)
    if currentOpCounter == 1:  # form is selected by user - ask confirmation
        return Operation1(user_input)
    if currentOpCounter == 2:  # form confirmation received from user
        return Operation2(user_input)
    if currentOpCounter == 3:  # ask form field values to user
        return Operation3(user_input)
    if currentOpCounter == 4:  # form field value received from user - ask confirmation
        return Operation4(user_input)
    if currentOpCounter == 5:  # form field value confirmation received from user
        return Operation5(user_input)
    if currentOpCounter == 6:  # ask if user wants to input spelling - ask confirmation
        return Operation6(user_input)
    if currentOpCounter == 7:  # input spelling question's confirmation received from user
        return Operation7(user_input)
    if currentOpCounter == 8:  # ask user to spell
        return Operation8(user_input)
    if currentOpCounter == 9:  # capture spellings
        return Operation9(user_input)
    if currentOpCounter == 10:  # ask user to stop and exit
        return Operation10(user_input)
    else:
        return debugstop("Some error occurred.")


# ---------------------------Part3.1.2-------------------------------
# ask to select form
def Operation0(user_input):
    global currentOpCounter
    currentOpCounter = 1
    return returnMsg("Welcome to " + CustomerName + ", Select your form to " \
                                                  "Open : " + ', '.join(map(str, FormList)))
# ask to re-select form
def Operation0_1(user_input):
    global currentOpCounter
    currentOpCounter = 1
    return returnMsg("Select your form: " + ', '.join(map(str, FormList)))
# form is selected by user - ask confirmation
def Operation1(user_input):
    global currentOpCounter, SelectedFormID
    SelectedFormID = FormList[user_input]
    currentOpCounter = 2
    return returnMsg("You have selected: " + user_input + " form." + " Is That Correct?")
# form confirmation received from user
def Operation2(user_input):
    global currentOpCounter, counter, FormField, FormNumber
    if user_input == 'YES':
        FormNumber = getformNumber(SelectedFormID)
        FormField = getformfields(SelectedFormID)
        return Operation3(user_input)
    elif user_input == 'NO':
        return Operation0_1(user_input)
# ask form field values to user
def Operation3(user_input):
    global currentOpCounter, counter
    wrongname_MSG = "Please tell your " + str(FormField[str(list(FormField)[counter])])
    currentOpCounter = 4
    return returnMsg(wrongname_MSG)
# form field value received from user - ask confirmation
def Operation4(user_input):
    global currentOpCounter, lastFormValueEntered
    currentOpCounter = 5
    lastFormValueEntered = user_input
    return returnMsg("You have entered " + user_input + " Is That Correct?")
# form field value confirmation received from user
def Operation5(user_input):
    global currentOpCounter, counter, Response_List
    if user_input == 'YES':
        Response_List[list(FormField)[counter]] = lastFormValueEntered
        #you can save entered data here
        counter = counter + 1
        if counter >= len(FormField):
            return Operation10(user_input)
        else:
            return Operation3(user_input)
    elif user_input == 'NO':
        currentOpCounter = 6  # ask if user wants to input spelling
        return Operation6(user_input)
# ask if user wants to input spelling - ask confirmation
def Operation6(user_input):
    global currentOpCounter
    currentOpCounter = 7
    return returnMsg("Do you want to spell "
                     "your " + str(FormField[str(list(FormField)[counter])]))
# input spelling question's confirmation received from user
def Operation7(user_input):
    global currentOpCounter, counter
    if user_input == 'YES':
        return Operation8(user_input)#start spell from here
    elif user_input == 'NO':
        if counter > 0:
            counter = counter - 1
        return Operation3(user_input)
# ask user to spell
def Operation8(user_input):
    global currentOpCounter
    currentOpCounter = 9
    return returnMsg("Please start spelling "
        "your " + str(FormField[str(list(FormField)[counter-1])]) + ". "
        "Once completed, say DONE. To remove last character entered, say REMOVE. You can start now.")
# capture spellings
def Operation9(user_input):
    global captureSpellValue
    if user_input == 'DONE':
        fieldvalue = captureSpellValue
        captureSpellValue = ''
        return Operation4(fieldvalue)
    elif user_input == 'REMOVE':
        # remove last char from captureSpellValue
        tempstr = captureSpellValue[-1:]
        captureSpellValue = captureSpellValue[:-1]
        return returnMsg("Removed Character: " + str(tempstr))
    else:
        captureSpellValue = captureSpellValue + user_input
        return returnMsg(user_input)
# ask user to stop and exit
def Operation10(user_input):
    global currentOpCounter
    currentOpCounter = 10

    return returnMsg("Your Form Number is: " + str(FormNumber) + ". All form fields are updated successfully. Please say stop to save and exit.")

# ---------------------------Part3.1.2-------------------------------
def returnMsg(msgtext):
    wrongname_MSG = str(msgtext)
    reprompt_MSG = str(msgtext)
    card_TEXT = str(msgtext)
    card_TITLE = str(msgtext)
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def debugstop(user_input):
    wrongname_MSG = "debug point hit: " + str(user_input)
    reprompt_MSG = "debug point hit: " + str(user_input)
    card_TEXT = "debug point hit: " + str(user_input)
    card_TITLE = "debug point hit: " + str(user_input)
    return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
def stop_the_skill(event):
    stop_MSG = "You have entered: " + ', '.join(map(str, Response_List)) + ". Thank you."
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
