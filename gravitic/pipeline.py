""" """
from .block import blockmap
class Pipeline:
    def __init__(self, specification):
        self.blocks = {}
        for spec in specification['blocks']:
            self.blocks[spec['name']] = blockmap[spec['type']](spec, pipeline=self)
    
    def run(self):
        for name, block in self.blocks.items():
            if not block.ready:
                block.run()
