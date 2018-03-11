import os
import aiopg.sa
import sqlalchemy as sa

meta = sa.MetaData()


question = sa.Table(
    'questions', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_text', sa.String(200), nullable=False),
    sa.Column('pub_date', sa.Date, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='question_id_pkey'))

choice = sa.Table(
    'choices', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('question_id', sa.Integer, nullable=False),
    sa.Column('choice_text', sa.String(200), nullable=False),
    sa.Column('votes', sa.Integer, server_default="0", nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='choice_id_pkey'),
    sa.ForeignKeyConstraint(['question_id'], [question.c.id],
                            name='choice_question_id_fkey',
                            ondelete='CASCADE'),
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=os.environ.get('POLLS_DB_NAME'),
        user=os.environ.get('POLLS_DB_USER'),
        password=os.environ.get('POLLS_DB_PASSWORD'),
        host=os.environ.get('POLLS_DB_HOST'),
        port=os.environ.get('DB_PORT', '5432'),
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_question(conn, question_id):
    result = await conn.execute(
        question.select()
            .where(question.c.id == question_id)
    )

    question_record = await result.first()

    if not question_record:
        msg = "Question with id: {} does not exists"
        raise RecordNotFound(msg.format(question_id))

    result = await conn.execute(
        choice.select()
            .where(choice.c.question_id == question_id)
            .order_by(choice.c.id)
    )
    choice_records = await result.fetchall()
    return question_record, choice_records

async def vote(conn, question_id, choice_id):
    result = await conn.execute(
        choice.update()
        .returning(*choice.c)
        .where(choice.c.question_id == question_id)
        .where(choice.c.id == choice_id)
        .values(votes=choice.c.votes+1))
    record = await result.fetchone()
    if not record:
        msg = "Question with id: {} or choice id: {} does not exists"
        raise RecordNotFound(msg.format(question_id, choice_id))
