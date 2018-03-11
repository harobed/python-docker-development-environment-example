from requests_html import HTML

async def test_index(http_client, questions_fixtures):
    resp = await http_client.get('/')
    assert resp.status == 200

    html = HTML(html=await resp.text())
    assert html.find("a", first=True).text == "What's new?"
    assert html.find("a", first=True).attrs['href'] == '/poll/1'


async def test_get_poll(http_client, choices_fixtures):
    resp = await http_client.get('/poll/1')
    assert resp.status == 200
    html = HTML(html=await resp.text())
    assert html.xpath("//label[@for='choice1']", first=True).text == 'Not much'
    assert html.xpath("//label[@for='choice2']", first=True).text == 'The sky'
    assert html.xpath("//label[@for='choice3']", first=True).text == 'Just hacking again'


async def test_post_poll(http_client, choices_fixtures):
    resp = await http_client.post(
        '/poll/1',
        data={
            'choice': 2
        }
    )

    assert resp.status == 200
    html = HTML(html=await resp.text())
    assert 'Not much - 0 vote(s)' in html.html
    assert 'The sky - 1 vote(s)' in html.html
    assert 'Just hacking again - 3 vote(s)' in html.html

async def test_poll_results(http_client, choices_fixtures):
    resp = await http_client.get('/poll/1/results')
    assert resp.status == 200
    html = HTML(html=await resp.text())
    assert 'Not much - 0 vote(s)' in html.html
    assert 'The sky - 0 vote(s)' in html.html
    assert 'Just hacking again - 3 vote(s)' in html.html
