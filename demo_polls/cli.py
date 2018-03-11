import click
import logging

from . import __version__
from . import server

logging.basicConfig(level=logging.ERROR)

log = logging.getLogger('polls')
log.setLevel(logging.INFO)

context_settings = {
    'auto_envvar_prefix': 'POLLS'
}

@click.group(context_settings=context_settings)
@click.version_option(message='Version: %s' % __version__)
@click.option('--debug', default=False, is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, debug):
    if debug:
        log.setLevel(logging.DEBUG)
        log.debug('Debug mode enabled')


@cli.command(context_settings=context_settings)
@click.option('--host', default='127.0.0.1', help='Http server host')
@click.option('--port', default='5000', help='Http server port')
@click.pass_context
def serve(ctx, host, port):
    log.info('Serve %s:%s' % (host, port))
    server.run_app(host, port)
