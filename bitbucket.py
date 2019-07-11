import json


def handle_bitbucket_event(request):
    event = request.get_json(silent=True)
    headers = request.headers

    event_key = headers.get('X-Event-Key')
    if 'pullrequest:' in event_key:
        response = handle_pull_request(event, headers)
    elif 'repo: commit_status_' in event_key:
        response = handle_commit_status(event, headers)
    else:
        response = handle_unknown(event, headers)

    return json.dumps(response, indent=2)


def handle_pull_request(event, headers):
    pr_id = event.get('pullrequest').get('id')
    pr_title = event.get('pullrequest').get('title')
    pr_link = event.get('pullrequest').get('links').get('html').get('href')
    pr_state = event.get('pullrequest').get('state')
    pr_actor = event.get('actor').get('display_name')
    pr_source_branch = event.get('pullrequest').get('source').get('branch').get('name')
    pr_destination_branch = event.get('pullrequest').get('destination').get('branch').get('name')

    text = 'PR#{} {} {} {} by {}. {}->{}'.format(pr_id, pr_title, pr_link, pr_state, pr_actor, pr_source_branch, pr_destination_branch)

    response = {
        'text': text
    }

    return response


def handle_commit_status(event, headers):
    cs_name = event.get('commit_status').get('name')
    cs_state = event.get('commit_status').get('state')
    cs_link = event.get('commit_status').get('url')

    text = '{} {} {}.'.format(cs_name, cs_link, cs_state)

    response = {
        'text': text
    }

    return response


def handle_unknown(event, headers):
    response = {
        'text': 'I know nothing about this kind of event.'
    }
    return response
