import click

from gravitic.schedulers import Schedule

@click.option("--start")
@click.option("--end")
@click.command
@Schedule(cpus=1, name="datadownload")
def download_data(start, end):
    from gravitic.data import DetectorData
    data = DetectorData(start, end)


download_data()
