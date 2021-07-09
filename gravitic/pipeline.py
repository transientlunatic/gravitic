""" """
import pathlib
import os
import networkx as nx
from .block import blockmap
class Pipeline:
    def __init__(self, production):
        self.specification_dict = production.meta['specification']
        self.production = production

        self.run_location = os.path.relpath(pathlib.Path(self.production.event.ledger.location).parents[0],
                                            os.getcwd())
        # compose computational graph
        self.graph = nx.DiGraph()
        
        self.blocks = {}
        for spec in self.specification_dict['blocks']:
            block = self.blocks[spec['name']] = blockmap[spec['type']](spec, pipeline=self)
            self.graph.add_node(block)
            if block.dependencies:
                dependencies = [depblock for name, depblock in self.blocks.items()
                                if name in block.dependencies]
                for dependency in dependencies:
                    self.graph.add_edge(dependency, block)
    
    def run(self):
        for block in self.get_all_latest():
            if not block.ready:
                print(f"Running {block.name}")
                block.run()
                self.save_state()
            block.package()
        if len(self.get_all_latest())>0:
            self.run()

    def get_all_latest(self):
        """
        Get all of the blocks which are not blocked by an unfinished block
        further back in their history.

        Returns
        -------
        set
            A set of independent blocks which are not finished execution.
        """
        unfinished = self.graph.subgraph([block for block in self.blocks.values()
                                          if block.finished == False])
        ends = [x for x in unfinished.reverse().nodes() if unfinished.reverse().out_degree(x)==0]
        return set(ends) # only want to return one version of each block!
            
    @property
    def specification(self):
        specification = self.specification_dict
        for name, block in self.blocks.items():
            specification['blocks'][name] = block.specification
        return specification

    def save_state(self):
        self.specification_dict['blocks'] = []
        for name, block in self.blocks.items():
            self.specification_dict['blocks'].append(
                block.specification)
        self.production.meta['specification'] = self.specification_dict
        self.production.update_ledger()

    @property
    def locations(self):
        return self.production.locations
        
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
