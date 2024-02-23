import os
import click
import class_recognise as recog

@click.group()
def cli():
    pass


@click.command(help="Register a song or a directory of songs")
@click.argument("path")
def register(path):
	Rec = recog.Recognise(path)
	Rec.register_song()



@click.command(help="Recognise a song at a filename or using the microphone")
@click.argument("path", required=False)
@click.option("--listen", is_flag=True,
				help="Use the microphone to listen for a song")
def recognise(path, listen):
#	if listen:
#		result = recog.listen_to_song()
#		click.echo(result)
#		if result[3] is not None:
#			path_new = os.path.normpath(result[3])
#			recog.play_song(path_new, play_duration=2000)
#	else:
	try:
		Rec = recog.Recognise(path)
		result = Rec.recognise_song()
		click.echo(Rec.song_data())
		path = Rec.listen_to_song()
		if path:
			path_new = os.path.join( ".", os.path.normpath(path))
			Rec.play_song(path_new, play_duration = 10000)
	except Exception as e:
		click.echo(f"Error: {e}")

#@click.command(
#    help="Initialise the DB, needs to be done before other commands")
#def initialise():
#    storage.()
#    click.echo("Initialised DB")


cli.add_command(register)
cli.add_command(recognise)
#cli.add_command(initialise)

if __name__ == "__main__":
    cli()
