from __future__ import print_function
import boto3
import json

TABLE_NAME = 'test_db'
dynamodb = boto3.resource('dynamodb')

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Einfochips  " \
                    "May i know your name please ? "
    reprompt_text = "Please, Can you tell me your name again ? "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for coming to Einfochips " \
                    "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_visitor_name_attributes(visitor_name):
    return {"visitorName": visitor_name}


def set_visitor_name_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Visitor' in intent['slots']:
        visitor_name = intent['slots']['Visitor']['value']
        session_attributes = create_visitor_name_attributes(visitor_name)
        speech_output = "Thank you for telling your name " \
                        + visitor_name + \
                        " To whome you want to Meet?  "

        reprompt_text = "Hey " \
                        + visitor_name + \
                        ". Can you tell me to whome you want to Meet? "
    else:
        speech_output = "I'm not sure about the name " \
                        " Can you tell me your name again ? "

        reprompt_text = "Can you please tell me.  What is  your name? "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_emp_name_attributes(emp_name):
    return {"empName": emp_name}


def set_emp_name_in_session(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Emp' in intent['slots']:
        emp_name = intent['slots']['Emp']['value']
        session_attributes = create_emp_name_attributes(emp_name)
        availability_output = get_availability_from_session(emp_name)

        speech_output = "Thank you for telling employee's name. " \
                        " So you want to meet "+ emp_name + \
                        ". Let me check  " + emp_name +" 's availability. "\
						" Meanwhile you can have a Sit near reception."\
						"                                                                              I just checked availability of " +emp_name+ "."\
						+ availability_output + "."

        reprompt_text = "Hey, " \
                        " So you want to meet "+ emp_name + "?"\
                        " Let me check  " + emp_name +" 's availability."\
						" Uptil you can have a Sit."\
						"                                                                             "\
						" I just checked availability of " +emp_name+ "."\
						+ availability_output + "."

    else:
        speech_output = "I'm not sure whome you want to Meet. " \
                        "Can you tell me to whome you want to Meet? "

        reprompt_text =  "Can you repeat the name whome you want to Meet? "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def get_availability_from_session(emp_name):

    presence = get_availability(emp_name)

    if presence is True:
        response_output = " "+emp_name+" is available in office today. "\
        "You can go to  " + emp_name +\
        " 's desk"

    elif presence is False:
        response_output = " Sorry, But " +emp_name+"  is not available in office today"\
        "Can you please call " + emp_name +\
        " and get your appointment"

    else:
        response_output = " Sorry, But " + emp_name + \
        " is not employee of Einfochips office"

    return response_output
#---- dynamo code---

def get_availability(responder_color):

    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'username': responder_color})
    if 'Item' in response.keys():
        presence = response['Item']['presence']
    else:
        presence = "Employee Not Found"
    return presence

# --------------- Events ------------------

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
    if intent_name == "VisitorNameIsIntent":
        return set_visitor_name_in_session(intent, session)
    elif intent_name == "EmpNameIsIntent":
        return set_emp_name_in_session(intent, session)
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


# --------------- Main handler ------------------

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
