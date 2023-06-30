import click

from gravitic.schedulers import Schedule

@click.option("--start")
@click.option("--end")
@click.command
@Schedule
def download_data(start, end):
    print("start", start, "end", end)
    from gravitic.data import DetectorData
    data = DetectorData(start, end)


download_data()
