""" """
from .block import blockmap
class Pipeline:
    def __init__(self, production):
        self.specification_dict = production.meta['specification']
        self.production = production
        self.blocks = {}
        for spec in self.specification_dict['blocks']:
            self.blocks[spec['name']] = blockmap[spec['type']](spec, pipeline=self)
    
    def run(self):
        for name, block in self.blocks.items():
            if not block.ready:
                block.run()
            block.package()

    @property
    def specification(self):
        specification = self.specification_dict
        for name, block in self.blocks.items():
            specification['blocks'][name] = block.specification
        return specification

    def save_state(self):
        pass

    def report(self):
        """
        Produce a report for the entire pipeline.

        
        """
        report = otter.Otter(f"{self.production.webdir}/{self.production.name}.html", 
                             author="Olivaw", 
                             title="Gravitic Report", 
                             author_email="daniel.williams@ligo.org")


        for name, block in pipeline.blocks.items():
            if not block.ready:
                continue

            block_report = otter.Otter(f"{self.production.webdir}/{self.production.name}/{name}.html", 
                             author="Olivaw", 
                             title=f"{name} Report", 
                             author_email="daniel.williams@ligo.org")
            
            with block_report:
                block_report + f"# {block.name}"
                block_report + block.report()

            with report:
                report += f"<a href='{self.production.webdir}/{self.production.name}/{name}.html'>{name}</a>"
