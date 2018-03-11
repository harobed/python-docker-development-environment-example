import aiohttp_jinja2
from aiohttp import web

from . import db


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.question.select())

    return {
        'questions': [dict(q) for q in await cursor.fetchall()]
    }


@aiohttp_jinja2.template('detail.html')
async def get_poll(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']
        try:
            question, choices = await db.get_question(conn, question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return {
            'question': question,
            'choices': choices
        }



async def post_poll(request):
    async with request.app['db'].acquire() as conn:
        question_id = int(request.match_info['question_id'])
        data = await request.post()
        try:
            choice_id = int(data['choice'])
        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='You have not specified choice value') from e
        try:
            await db.vote(conn, question_id, choice_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return web.HTTPSeeOther(
            request.app.router['poll_results'].url_for(
                question_id=str(question_id)
            )
        )


@aiohttp_jinja2.template('results.html')
async def poll_results(request):
    async with request.app['db'].acquire() as conn:
        question_id = request.match_info['question_id']

        try:
            question, choices = await db.get_question(conn, question_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        return {
            'question': question,
            'choices': choices
        }