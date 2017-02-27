"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AddMessageIntent":
        return process_intent("add", intent, session)
    elif intent_name == "SearchMessageIntent":
        return process_intent("search", intent, session)
    elif intent_name == "ReadMessageIntent":
        return process_intent("read", intent, session)
    elif intent_name == "DeleteMessageIntent":
        return process_intent("delete", intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Team11 Notepad. " \
                    "You can add, search, read and delete notes"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can add, search, read and delete notes." \
					"For example , you can tell: add some note or search some keyword or read oldest or delete newest"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Team11 Notepad. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def GetData(session, userId):
    if session.get('attributes', {}) and "notepad" in session.get('attributes', {}):
        data = session['attributes']['notepad']
    else:
        data = None
    
    #bucket = GetBucket()
    #k = Key(bucket)
    #k.key = userId

    #data = k.get_contents_as_string()
       
    return data

def GetClient():
    #client = boto3.client('s3', aws_access_key_id='AKIAI4BDFFNQNN24626Q', aws_secret_access_key='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')

    #try:
    #    bucket = conn.get_bucket('Team11Notepad')
    #except S3ResponseError:
    #    bucket = conn.create_bucket('Team11Notepad')

    return client

def SaveData(data, userId):
    #k = Key(bucket)
    #k.key = userId
    #k.set_contents_from_string(data)

    return

def process_intent(intent_type, intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if intent_type == "add" or intent_type == "search" or intent_type == "read" or intent_type == "delete":
        data = GetData(session, "xxx")		
        if 'Message' in intent['slots']:
            new_data, response = parser(data, intent_type + " " + intent['slots']['Message']['value'])
        elif 'Selector' in intent['slots']:
            print("!!!! Selector: " + str(intent['slots']['Selector']));
            if 'value' in intent['slots']['Selector']:
                new_data, response = parser(data, intent_type + " " + intent['slots']['Selector']['value'])
            else:
                new_data = None
                response = "Please repeat."
        if new_data is not None:
            print("!!!!!!!!!!!!!!!!")
            print("New data in session: " + new_data)
            session_attributes = {"notepad" : new_data}
            SaveData(new_data, "xxx")
        else:
            session_attributes = {"notepad" : data}
            
        speech_output = response
        reprompt_text = response
    else:
        speech_output = "I'm not sure what your are trying to do. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your are trying to do. " \
                        "For example , you can tell: add some note or search some keyword or read oldest or delete newest"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def parser(data, command):
    # defaults
    new_data = None
    response = "command not supported"

    # decompose data
    if data is not None:
        lines = data.split('\n')
        del lines[-1]
    else:
        lines = []

    # decompose command
    tokens = command.split(' ')
    action = tokens[0]
    del tokens[0]

    if action == "add":
        if len(tokens) == 0:
            response = "no note to add"
            return new_data, response
        lines.append(" ".join(tokens))
        new_data = "\n".join(lines) + "\n"
        response = "note added"

    elif action == "search":
        if len(lines) == 0:
            response = "no data to search"
        else:
            if len(tokens) == 0:
                response = "no keywords to search"
                return new_data, response
            response = ""
            for l in lines:
                match = True
                for t in tokens:
                    if l.find(t) == -1:
                        match = False
                        break
                if match is True:
                    if response == "":
                        response = l
                    else:
                        response += ". " + l
            if response == "":
                response = "nothing found"

    elif action == "read":
        if len(lines) == 0:
            response = "no data to read"
        else:
            if len(tokens) == 0:
                return new_data, response #defaults
            if tokens[0] == "all":
                response = ". ".join(lines)
            elif tokens[0] == "oldest":
                response = lines[0]
            elif tokens[0] == "latest" or tokens[0] == "newest":
                response = lines[-1]
            else:
                return new_data, response # defaults

    elif action == "delete":
        if len(lines) == 0:
            response = "no data to delete"
        else:
            if len(tokens) == 0:
                return new_data, response #defaults
            if tokens[0] == "all":
                lines = []
            elif tokens[0] == "oldest":
                del lines[0]
            elif tokens[0] == "latest" or tokens[0] == "newest":
                del lines[-1]
            else:
                return new_data, response # defaults
            response = "data deleted"
            if len(lines) == 0:
                new_data = ""
            else:
                new_data = "\n".join(lines) + "\n"

    return new_data, response
